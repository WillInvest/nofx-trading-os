#!/usr/bin/env python3
"""
Historical Backtest: Input-Fee vs Output-Fee AMMs on Real Uniswap Data

Uses Uniswap v3 ETH/USDC pool swap events to replay under both fee models
and compare LP returns empirically.

Author: OpenClaw Research Agent
Date: 2026-02-07

Data Sources:
- Uniswap v3 Subgraph (The Graph)
- Dune Analytics (alternative)
- Direct RPC with event logs (for full data)

Usage:
    python historical_backtest.py --pool 0x88e6... --start 2024-01-01 --days 30
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import requests


# ============ Data Structures ============

@dataclass
class Swap:
    """Represents a single swap event."""
    block_number: int
    timestamp: int
    amount0: float  # Token 0 amount (negative = sold by pool)
    amount1: float  # Token 1 amount (negative = sold by pool)
    sqrt_price_x96_after: int
    liquidity: int
    tick: int
    
    @property
    def is_buy_token0(self) -> bool:
        """True if trader is buying token0 (selling token1)."""
        return self.amount0 < 0


@dataclass
class PoolState:
    """Tracks LP state under a fee model."""
    reserve0: float
    reserve1: float
    fees_collected0: float = 0.0
    fees_collected1: float = 0.0
    total_volume0: float = 0.0
    total_volume1: float = 0.0
    num_swaps: int = 0
    lvr_loss: float = 0.0  # Cumulative LVR
    
    def copy(self) -> 'PoolState':
        return PoolState(
            self.reserve0, self.reserve1,
            self.fees_collected0, self.fees_collected1,
            self.total_volume0, self.total_volume1,
            self.num_swaps, self.lvr_loss
        )
    
    @property
    def price(self) -> float:
        """Token1 per Token0."""
        return self.reserve1 / self.reserve0 if self.reserve0 > 0 else 0
    
    def lp_value_in_token1(self, external_price: float) -> float:
        """Value of LP position in token1 terms."""
        return self.reserve0 * external_price + self.reserve1 + \
               self.fees_collected0 * external_price + self.fees_collected1


# ============ Fee Models ============

def apply_swap_input_fee(state: PoolState, amount_in: float, is_token0_in: bool, 
                         fee_rate: float, external_price: float) -> PoolState:
    """
    Apply a swap with INPUT-based fees (Uniswap standard).
    
    Args:
        state: Current pool state
        amount_in: Amount of input token (positive)
        is_token0_in: True if token0 is being sold
        fee_rate: Fee rate (e.g., 0.003 for 0.3%)
        external_price: External market price for LVR calculation
    """
    new_state = state.copy()
    fee_multiplier = 1 - fee_rate
    
    if is_token0_in:
        # Trader sells token0, buys token1
        effective_in = amount_in * fee_multiplier
        amount_out = (new_state.reserve1 * effective_in) / (new_state.reserve0 + effective_in)
        
        new_state.reserve0 += amount_in
        new_state.reserve1 -= amount_out
        new_state.fees_collected0 += amount_in * fee_rate
        new_state.total_volume0 += amount_in
    else:
        # Trader sells token1, buys token0
        effective_in = amount_in * fee_multiplier
        amount_out = (new_state.reserve0 * effective_in) / (new_state.reserve1 + effective_in)
        
        new_state.reserve1 += amount_in
        new_state.reserve0 -= amount_out
        new_state.fees_collected1 += amount_in * fee_rate
        new_state.total_volume1 += amount_in
    
    # Calculate LVR component
    amm_price = new_state.price
    if abs(amm_price - external_price) > 0:
        lvr = abs(amm_price - external_price) * min(abs(amount_out if is_token0_in else amount_in), 
                                                     new_state.reserve0 * 0.01)
        new_state.lvr_loss += lvr * 0.5  # Simplified LVR estimate
    
    new_state.num_swaps += 1
    return new_state


def apply_swap_output_fee(state: PoolState, amount_in: float, is_token0_in: bool,
                          fee_rate: float, external_price: float) -> PoolState:
    """
    Apply a swap with OUTPUT-based fees (our proposed model).
    
    Key difference: Fee is charged on what trader receives, not what they pay.
    """
    new_state = state.copy()
    fee_multiplier = 1 - fee_rate
    
    if is_token0_in:
        # Trader sells token0, buys token1
        # First compute gross output (no fee on input)
        gross_out = (new_state.reserve1 * amount_in) / (new_state.reserve0 + amount_in)
        net_out = gross_out * fee_multiplier
        
        new_state.reserve0 += amount_in
        new_state.reserve1 -= net_out  # Trader gets less
        new_state.fees_collected1 += gross_out * fee_rate  # Fee in output token
        new_state.total_volume0 += amount_in
    else:
        # Trader sells token1, buys token0
        gross_out = (new_state.reserve0 * amount_in) / (new_state.reserve1 + amount_in)
        net_out = gross_out * fee_multiplier
        
        new_state.reserve1 += amount_in
        new_state.reserve0 -= net_out
        new_state.fees_collected0 += gross_out * fee_rate
        new_state.total_volume1 += amount_in
    
    # Calculate LVR component (output fee taxes arb profit directly)
    amm_price = new_state.price
    if abs(amm_price - external_price) > 0:
        # Output fee reduces LVR because it taxes arbitrageur's received tokens
        lvr = abs(amm_price - external_price) * min(abs(net_out), new_state.reserve0 * 0.01)
        new_state.lvr_loss += lvr * 0.5 * fee_multiplier  # Reduced by fee
    
    new_state.num_swaps += 1
    return new_state


# ============ Data Fetching ============

UNISWAP_V3_SUBGRAPH = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

# Well-known pool addresses
POOLS = {
    "ETH-USDC-0.3%": "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8",
    "ETH-USDC-0.05%": "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
    "ETH-USDT-0.3%": "0x4e68ccd3e89f51c3074ca5072bbac773960dfa36",
}


def fetch_swaps_from_subgraph(pool_address: str, start_timestamp: int, 
                               end_timestamp: int, limit: int = 1000) -> List[Swap]:
    """Fetch swap events from Uniswap v3 subgraph."""
    
    query = """
    query GetSwaps($pool: String!, $start: Int!, $end: Int!, $skip: Int!, $limit: Int!) {
        swaps(
            where: {
                pool: $pool,
                timestamp_gte: $start,
                timestamp_lte: $end
            }
            orderBy: timestamp
            orderDirection: asc
            skip: $skip
            first: $limit
        ) {
            id
            timestamp
            amount0
            amount1
            sqrtPriceX96
            tick
            transaction {
                blockNumber
            }
        }
    }
    """
    
    swaps = []
    skip = 0
    
    while True:
        response = requests.post(
            UNISWAP_V3_SUBGRAPH,
            json={
                "query": query,
                "variables": {
                    "pool": pool_address.lower(),
                    "start": start_timestamp,
                    "end": end_timestamp,
                    "skip": skip,
                    "limit": limit
                }
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break
        
        data = response.json()
        if "errors" in data:
            print(f"GraphQL errors: {data['errors']}")
            break
        
        batch = data.get("data", {}).get("swaps", [])
        if not batch:
            break
        
        for s in batch:
            swaps.append(Swap(
                block_number=int(s["transaction"]["blockNumber"]),
                timestamp=int(s["timestamp"]),
                amount0=float(s["amount0"]),
                amount1=float(s["amount1"]),
                sqrt_price_x96_after=int(s["sqrtPriceX96"]),
                liquidity=0,  # Not needed for this analysis
                tick=int(s["tick"])
            ))
        
        if len(batch) < limit:
            break
        skip += limit
        print(f"Fetched {len(swaps)} swaps...")
    
    return swaps


def load_sample_data() -> List[Swap]:
    """Load sample swap data for testing (when subgraph unavailable)."""
    # Generate synthetic data mimicking real swap patterns
    import random
    random.seed(42)
    
    swaps = []
    base_price = 2000.0  # ETH in USDC
    current_time = int(datetime(2024, 1, 1).timestamp())
    
    for i in range(10000):
        # Random price movement (GBM-like)
        base_price *= (1 + random.gauss(0, 0.001))
        
        # Random swap direction and size
        is_buy_eth = random.random() > 0.5
        size_eth = random.expovariate(1/0.5)  # Average 0.5 ETH
        
        if is_buy_eth:
            amount0 = -size_eth  # Pool sells ETH
            amount1 = size_eth * base_price * (1 + random.uniform(0, 0.003))
        else:
            amount0 = size_eth
            amount1 = -size_eth * base_price * (1 - random.uniform(0, 0.003))
        
        swaps.append(Swap(
            block_number=18000000 + i,
            timestamp=current_time + i * 12,  # ~12 sec blocks
            amount0=amount0,
            amount1=amount1,
            sqrt_price_x96_after=0,
            liquidity=0,
            tick=0
        ))
    
    return swaps


# ============ Backtest Engine ============

@dataclass
class BacktestResult:
    """Results from running a backtest."""
    model: str
    initial_value: float
    final_value: float
    total_fees_token0: float
    total_fees_token1: float
    total_volume_token0: float
    total_volume_token1: float
    num_swaps: int
    lvr_estimate: float
    returns_pct: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "model": self.model,
            "initial_value": self.initial_value,
            "final_value": self.final_value,
            "returns_pct": self.returns_pct,
            "total_fees_token0": self.total_fees_token0,
            "total_fees_token1": self.total_fees_token1,
            "lvr_estimate": self.lvr_estimate,
            "num_swaps": self.num_swaps
        }


def run_backtest(swaps: List[Swap], initial_reserve0: float, initial_reserve1: float,
                 fee_rate: float = 0.003) -> Tuple[BacktestResult, BacktestResult]:
    """
    Run parallel backtest with input-fee and output-fee models.
    
    Returns:
        (input_fee_result, output_fee_result)
    """
    
    # Initialize both pools identically
    input_state = PoolState(initial_reserve0, initial_reserve1)
    output_state = PoolState(initial_reserve0, initial_reserve1)
    
    initial_price = initial_reserve1 / initial_reserve0
    initial_value = initial_reserve0 * initial_price + initial_reserve1
    
    for swap in swaps:
        # Determine swap direction and size
        if swap.amount0 > 0:
            # Trader is selling token0 (ETH) to pool
            amount_in = swap.amount0
            is_token0_in = True
        else:
            # Trader is selling token1 (USDC) to pool
            amount_in = abs(swap.amount1)
            is_token0_in = False
        
        # Use post-swap price as external price proxy
        # (In real backtest, would use CEX price)
        external_price = abs(swap.amount1 / swap.amount0) if swap.amount0 != 0 else input_state.price
        
        # Apply swap to both models
        input_state = apply_swap_input_fee(input_state, amount_in, is_token0_in, 
                                            fee_rate, external_price)
        output_state = apply_swap_output_fee(output_state, amount_in, is_token0_in,
                                              fee_rate, external_price)
    
    # Calculate final values
    final_price = output_state.price  # Use one price (should be similar)
    
    input_final = input_state.lp_value_in_token1(final_price)
    output_final = output_state.lp_value_in_token1(final_price)
    
    input_result = BacktestResult(
        model="input_fee",
        initial_value=initial_value,
        final_value=input_final,
        total_fees_token0=input_state.fees_collected0,
        total_fees_token1=input_state.fees_collected1,
        total_volume_token0=input_state.total_volume0,
        total_volume_token1=input_state.total_volume1,
        num_swaps=input_state.num_swaps,
        lvr_estimate=input_state.lvr_loss,
        returns_pct=(input_final / initial_value - 1) * 100
    )
    
    output_result = BacktestResult(
        model="output_fee",
        initial_value=initial_value,
        final_value=output_final,
        total_fees_token0=output_state.fees_collected0,
        total_fees_token1=output_state.fees_collected1,
        total_volume_token0=output_state.total_volume0,
        total_volume_token1=output_state.total_volume1,
        num_swaps=output_state.num_swaps,
        lvr_estimate=output_state.lvr_loss,
        returns_pct=(output_final / initial_value - 1) * 100
    )
    
    return input_result, output_result


def run_fee_sensitivity(swaps: List[Swap], fee_rates: List[float]) -> Dict[float, Dict]:
    """Run backtest across multiple fee rates to find sweet spot."""
    results = {}
    
    for fee_rate in fee_rates:
        print(f"Testing fee rate: {fee_rate*100:.2f}%")
        input_r, output_r = run_backtest(swaps, 100.0, 200000.0, fee_rate)
        
        results[fee_rate] = {
            "input_return": input_r.returns_pct,
            "output_return": output_r.returns_pct,
            "difference": output_r.returns_pct - input_r.returns_pct,
            "output_wins": output_r.returns_pct > input_r.returns_pct,
            "lvr_reduction": (input_r.lvr_estimate - output_r.lvr_estimate) / input_r.lvr_estimate * 100
                if input_r.lvr_estimate > 0 else 0
        }
    
    return results


# ============ Main ============

def main():
    parser = argparse.ArgumentParser(description="Historical backtest: Input vs Output fee AMMs")
    parser.add_argument("--pool", type=str, default="ETH-USDC-0.3%",
                        help="Pool to backtest (or custom address)")
    parser.add_argument("--start", type=str, default="2024-01-01",
                        help="Start date (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=30,
                        help="Number of days to backtest")
    parser.add_argument("--sample", action="store_true",
                        help="Use synthetic sample data (for testing)")
    parser.add_argument("--sensitivity", action="store_true",
                        help="Run fee sensitivity analysis")
    parser.add_argument("--output", type=str, default=None,
                        help="Output JSON file for results")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Historical Backtest: Input-Fee vs Output-Fee AMM")
    print("=" * 60)
    
    # Load swap data
    if args.sample:
        print("\nUsing synthetic sample data...")
        swaps = load_sample_data()
    else:
        pool_address = POOLS.get(args.pool, args.pool)
        start_dt = datetime.strptime(args.start, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=args.days)
        
        print(f"\nFetching swaps from {args.start} for {args.days} days...")
        print(f"Pool: {pool_address}")
        
        try:
            swaps = fetch_swaps_from_subgraph(
                pool_address,
                int(start_dt.timestamp()),
                int(end_dt.timestamp())
            )
        except Exception as e:
            print(f"Failed to fetch data: {e}")
            print("Falling back to sample data...")
            swaps = load_sample_data()
    
    print(f"\nLoaded {len(swaps)} swap events")
    
    if args.sensitivity:
        print("\n" + "=" * 60)
        print("Fee Sensitivity Analysis")
        print("=" * 60)
        
        fee_rates = [0.001, 0.002, 0.003, 0.005, 0.01]
        results = run_fee_sensitivity(swaps, fee_rates)
        
        print("\nResults:")
        print("-" * 60)
        print(f"{'Fee Rate':>10} | {'Input Return':>12} | {'Output Return':>13} | {'Δ':>8} | {'LVR Red.':>8}")
        print("-" * 60)
        
        for fee, r in sorted(results.items()):
            print(f"{fee*100:>9.2f}% | {r['input_return']:>11.3f}% | {r['output_return']:>12.3f}% | "
                  f"{r['difference']:>7.3f}% | {r['lvr_reduction']:>7.1f}%")
        
        # Find optimal fee rate
        best_fee = max(results.keys(), key=lambda f: results[f]['difference'])
        print(f"\nOptimal fee rate (max output advantage): {best_fee*100:.2f}%")
        print(f"LVR reduction at optimal: {results[best_fee]['lvr_reduction']:.1f}%")
        
    else:
        # Single backtest
        print("\nRunning backtest with 0.3% fee...")
        input_result, output_result = run_backtest(swaps, 100.0, 200000.0, 0.003)
        
        print("\n" + "=" * 60)
        print("Results")
        print("=" * 60)
        
        print("\nInput-Fee Model:")
        print(f"  Initial Value: ${input_result.initial_value:,.2f}")
        print(f"  Final Value:   ${input_result.final_value:,.2f}")
        print(f"  Return:        {input_result.returns_pct:+.3f}%")
        print(f"  Fees (token0): {input_result.total_fees_token0:.4f}")
        print(f"  Fees (token1): ${input_result.total_fees_token1:,.2f}")
        print(f"  LVR Estimate:  ${input_result.lvr_estimate:,.2f}")
        
        print("\nOutput-Fee Model:")
        print(f"  Initial Value: ${output_result.initial_value:,.2f}")
        print(f"  Final Value:   ${output_result.final_value:,.2f}")
        print(f"  Return:        {output_result.returns_pct:+.3f}%")
        print(f"  Fees (token0): {output_result.total_fees_token0:.4f}")
        print(f"  Fees (token1): ${output_result.total_fees_token1:,.2f}")
        print(f"  LVR Estimate:  ${output_result.lvr_estimate:,.2f}")
        
        print("\n" + "-" * 60)
        diff = output_result.returns_pct - input_result.returns_pct
        winner = "OUTPUT" if diff > 0 else "INPUT" if diff < 0 else "TIE"
        print(f"Difference: {diff:+.4f}% ({winner} wins)")
        
        if input_result.lvr_estimate > 0:
            lvr_reduction = (input_result.lvr_estimate - output_result.lvr_estimate) / input_result.lvr_estimate * 100
            print(f"LVR Reduction: {lvr_reduction:.1f}%")
    
    # Save results
    if args.output:
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "num_swaps": len(swaps),
            "parameters": {
                "pool": args.pool,
                "start": args.start,
                "days": args.days
            }
        }
        
        if args.sensitivity:
            output_data["sensitivity"] = {str(k): v for k, v in results.items()}
        else:
            output_data["input_fee"] = input_result.to_dict()
            output_data["output_fee"] = output_result.to_dict()
        
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nResults saved to: {args.output}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
