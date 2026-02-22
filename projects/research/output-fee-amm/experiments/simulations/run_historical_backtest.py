#!/usr/bin/env python3
"""
Run historical backtest using real ETH/USDC swap data.
Uses data from experiments/data/eth_usdc_swaps_june2024.json
"""

import json
import sys
from dataclasses import dataclass
from typing import List, Tuple, Dict
from pathlib import Path

# Token decimals for ETH/USDC pool
TOKEN0_DECIMALS = 6   # USDC
TOKEN1_DECIMALS = 18  # WETH

@dataclass
class PoolState:
    """LP position state."""
    reserve0: float  # USDC
    reserve1: float  # ETH
    fees0: float = 0.0
    fees1: float = 0.0
    num_swaps: int = 0
    
    @property
    def k(self) -> float:
        return self.reserve0 * self.reserve1
    
    @property
    def price_eth_usdc(self) -> float:
        """ETH price in USDC."""
        return self.reserve0 / self.reserve1 if self.reserve1 > 0 else 0
    
    def value_in_usdc(self) -> float:
        """Total LP value in USDC."""
        return self.reserve0 + self.reserve1 * self.price_eth_usdc + \
               self.fees0 + self.fees1 * self.price_eth_usdc

def apply_input_fee_swap(state: PoolState, amount0_in: float, amount1_in: float, 
                         fee_rate: float) -> PoolState:
    """Apply swap with Uniswap-style input fee."""
    new = PoolState(state.reserve0, state.reserve1, state.fees0, state.fees1, state.num_swaps + 1)
    
    if amount0_in > 0:  # Selling USDC for ETH
        effective_in = amount0_in * (1 - fee_rate)
        amount_out = (new.reserve1 * effective_in) / (new.reserve0 + effective_in)
        new.reserve0 += amount0_in
        new.reserve1 -= amount_out
        new.fees0 += amount0_in * fee_rate
    else:  # Selling ETH for USDC
        amount1_in = abs(amount1_in)
        effective_in = amount1_in * (1 - fee_rate)
        amount_out = (new.reserve0 * effective_in) / (new.reserve1 + effective_in)
        new.reserve1 += amount1_in
        new.reserve0 -= amount_out
        new.fees1 += amount1_in * fee_rate
    
    return new

def apply_output_fee_swap(state: PoolState, amount0_in: float, amount1_in: float,
                          fee_rate: float) -> PoolState:
    """Apply swap with output-based fee."""
    new = PoolState(state.reserve0, state.reserve1, state.fees0, state.fees1, state.num_swaps + 1)
    
    if amount0_in > 0:  # Selling USDC for ETH - fee on ETH out
        gross_out = (new.reserve1 * amount0_in) / (new.reserve0 + amount0_in)
        net_out = gross_out * (1 - fee_rate)
        new.reserve0 += amount0_in
        new.reserve1 -= net_out
        new.fees1 += gross_out * fee_rate  # Fee in ETH
    else:  # Selling ETH for USDC - fee on USDC out
        amount1_in = abs(amount1_in)
        gross_out = (new.reserve0 * amount1_in) / (new.reserve1 + amount1_in)
        net_out = gross_out * (1 - fee_rate)
        new.reserve1 += amount1_in
        new.reserve0 -= net_out
        new.fees0 += gross_out * fee_rate  # Fee in USDC
    
    return new

def run_backtest(swaps: List[Dict], fee_rate: float = 0.003) -> Tuple[Dict, Dict]:
    """Run backtest with both fee models."""
    
    # Initialize with approximate pool reserves at start of period
    # ETH/USDC 0.3% pool typically has ~$50M+ TVL
    # Starting with ~10k ETH and ~35M USDC as representative
    initial_eth = 10000.0
    initial_usdc = 35_000_000.0
    
    input_state = PoolState(initial_usdc, initial_eth)
    output_state = PoolState(initial_usdc, initial_eth)
    
    initial_value = input_state.value_in_usdc()
    
    for swap in swaps:
        # Convert from raw amounts to decimal
        amount0 = swap["amount0"] / (10 ** TOKEN0_DECIMALS)  # USDC
        amount1 = swap["amount1"] / (10 ** TOKEN1_DECIMALS)  # ETH
        
        # Determine trade direction from signs
        # Positive amount0 = USDC flowing IN (selling USDC for ETH)
        # Negative amount1 = ETH flowing OUT
        
        if amount0 > 0:  # Buying ETH with USDC
            input_state = apply_input_fee_swap(input_state, amount0, 0, fee_rate)
            output_state = apply_output_fee_swap(output_state, amount0, 0, fee_rate)
        else:  # Buying USDC with ETH
            input_state = apply_input_fee_swap(input_state, 0, amount1, fee_rate)
            output_state = apply_output_fee_swap(output_state, 0, amount1, fee_rate)
    
    input_final = input_state.value_in_usdc()
    output_final = output_state.value_in_usdc()
    
    input_result = {
        "model": "input_fee",
        "initial_value": initial_value,
        "final_value": input_final,
        "return_pct": (input_final / initial_value - 1) * 100,
        "fees_usdc": input_state.fees0,
        "fees_eth": input_state.fees1,
        "num_swaps": input_state.num_swaps,
        "final_price": input_state.price_eth_usdc
    }
    
    output_result = {
        "model": "output_fee",
        "initial_value": initial_value,
        "final_value": output_final,
        "return_pct": (output_final / initial_value - 1) * 100,
        "fees_usdc": output_state.fees0,
        "fees_eth": output_state.fees1,
        "num_swaps": output_state.num_swaps,
        "final_price": output_state.price_eth_usdc
    }
    
    return input_result, output_result


def main():
    data_path = Path(__file__).parent.parent / "data" / "eth_usdc_swaps_june2024.json"
    
    print("=" * 70)
    print("Historical Backtest: Input-Fee vs Output-Fee AMM")
    print("Data: ETH/USDC 0.3% Pool, June 2024")
    print("=" * 70)
    
    with open(data_path) as f:
        data = json.load(f)
    
    swaps = data["swaps"]
    print(f"\nLoaded {len(swaps):,} swaps from blocks {data['start_block']:,} to {data['end_block']:,}")
    
    # Run main backtest at 0.3% fee
    print("\n" + "-" * 70)
    print("STANDARD BACKTEST (0.3% fee)")
    print("-" * 70)
    
    input_r, output_r = run_backtest(swaps, 0.003)
    
    print(f"\nInput-Fee Model (Uniswap standard):")
    print(f"  Initial:  ${input_r['initial_value']:,.0f}")
    print(f"  Final:    ${input_r['final_value']:,.0f}")
    print(f"  Return:   {input_r['return_pct']:+.4f}%")
    print(f"  Fees:     {input_r['fees_usdc']:,.0f} USDC + {input_r['fees_eth']:.4f} ETH")
    
    print(f"\nOutput-Fee Model (proposed):")
    print(f"  Initial:  ${output_r['initial_value']:,.0f}")
    print(f"  Final:    ${output_r['final_value']:,.0f}")
    print(f"  Return:   {output_r['return_pct']:+.4f}%")
    print(f"  Fees:     {output_r['fees_usdc']:,.0f} USDC + {output_r['fees_eth']:.4f} ETH")
    
    diff = output_r['return_pct'] - input_r['return_pct']
    winner = "OUTPUT-FEE" if diff > 0 else "INPUT-FEE" if diff < 0 else "TIE"
    
    print(f"\n{'='*70}")
    print(f"RESULT: {winner} WINS by {abs(diff):.4f}%")
    print(f"{'='*70}")
    
    # Fee sensitivity analysis
    print("\n" + "-" * 70)
    print("FEE SENSITIVITY ANALYSIS")
    print("-" * 70)
    print(f"{'Fee Rate':>10} | {'Input Return':>14} | {'Output Return':>14} | {'Difference':>12}")
    print("-" * 70)
    
    for fee in [0.001, 0.003, 0.005, 0.01, 0.02]:
        in_r, out_r = run_backtest(swaps, fee)
        d = out_r['return_pct'] - in_r['return_pct']
        print(f"{fee*100:>9.2f}% | {in_r['return_pct']:>+13.4f}% | {out_r['return_pct']:>+13.4f}% | {d:>+11.4f}%")
    
    # Save results
    results_path = Path(__file__).parent.parent / "results" / "historical_backtest_results.json"
    results_path.parent.mkdir(exist_ok=True)
    
    results = {
        "data_source": str(data_path),
        "swap_count": len(swaps),
        "start_block": data["start_block"],
        "end_block": data["end_block"],
        "main_result": {
            "fee_rate": 0.003,
            "input_fee": input_r,
            "output_fee": output_r,
            "winner": winner,
            "advantage_pct": diff
        }
    }
    
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()
