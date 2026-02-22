#!/usr/bin/env python3
"""
Run backtest on real ETH/USDC swap data.
Loads the JSON from RPC data and runs both fee models.
"""

import json
import sys
from dataclasses import dataclass
from typing import List, Tuple

# ============ Data Structures ============

@dataclass
class PoolState:
    """Tracks LP state under a fee model."""
    reserve0: float  # USDC
    reserve1: float  # ETH
    fees_collected0: float = 0.0  # USDC fees
    fees_collected1: float = 0.0  # ETH fees
    
    def copy(self) -> 'PoolState':
        return PoolState(self.reserve0, self.reserve1, 
                        self.fees_collected0, self.fees_collected1)
    
    @property
    def price(self) -> float:
        """USDC per ETH."""
        return self.reserve0 / self.reserve1 if self.reserve1 > 0 else 0
    
    def total_value_usdc(self, eth_price: float) -> float:
        """Total value in USDC."""
        return self.reserve0 + self.reserve1 * eth_price + \
               self.fees_collected0 + self.fees_collected1 * eth_price


def apply_swap_input_fee(state: PoolState, amount0: float, amount1: float, 
                         fee_rate: float = 0.003) -> PoolState:
    """Apply swap with INPUT-based fees."""
    new_state = state.copy()
    
    if amount0 > 0:  # Trader sells USDC, buys ETH
        effective_in = amount0 * (1 - fee_rate)
        amount_out = (new_state.reserve1 * effective_in) / (new_state.reserve0 + effective_in)
        new_state.reserve0 += amount0
        new_state.reserve1 -= amount_out
        new_state.fees_collected0 += amount0 * fee_rate
    else:  # Trader sells ETH, buys USDC (amount1 > 0)
        effective_in = amount1 * (1 - fee_rate)
        amount_out = (new_state.reserve0 * effective_in) / (new_state.reserve1 + effective_in)
        new_state.reserve1 += amount1
        new_state.reserve0 -= amount_out
        new_state.fees_collected1 += amount1 * fee_rate
    
    return new_state


def apply_swap_output_fee(state: PoolState, amount0: float, amount1: float,
                          fee_rate: float = 0.003) -> PoolState:
    """Apply swap with OUTPUT-based fees."""
    new_state = state.copy()
    
    if amount0 > 0:  # Trader sells USDC, buys ETH
        gross_out = (new_state.reserve1 * amount0) / (new_state.reserve0 + amount0)
        net_out = gross_out * (1 - fee_rate)
        new_state.reserve0 += amount0
        new_state.reserve1 -= net_out
        new_state.fees_collected1 += gross_out * fee_rate  # Fee in ETH (output)
    else:  # Trader sells ETH, buys USDC
        gross_out = (new_state.reserve0 * amount1) / (new_state.reserve1 + amount1)
        net_out = gross_out * (1 - fee_rate)
        new_state.reserve1 += amount1
        new_state.reserve0 -= net_out
        new_state.fees_collected0 += gross_out * fee_rate  # Fee in USDC (output)
    
    return new_state


def main():
    # Load data
    data_path = "../data/eth_usdc_swaps_june2024.json"
    print(f"Loading {data_path}...")
    
    with open(data_path) as f:
        data = json.load(f)
    
    swaps = data["swaps"]
    print(f"Loaded {len(swaps)} swaps")
    
    # Convert amounts (USDC: 6 decimals, ETH: 18 decimals)
    # Note: In this pool, token0 = USDC, token1 = WETH
    parsed_swaps = []
    for s in swaps:
        usdc_amount = s["amount0"] / 1e6
        eth_amount = s["amount1"] / 1e18
        parsed_swaps.append((usdc_amount, eth_amount))
    
    # Get initial price from first swap
    first_usdc, first_eth = parsed_swaps[0]
    if first_eth != 0:
        initial_price = abs(first_usdc / first_eth)
    else:
        initial_price = 3500  # Fallback June 2024 price
    
    print(f"Initial price estimate: ${initial_price:.2f}/ETH")
    
    # Initialize pools with realistic liquidity
    # ETH/USDC 0.3% pool typically has ~$50M+ TVL
    initial_eth = 5000.0
    initial_usdc = initial_eth * initial_price
    
    input_state = PoolState(initial_usdc, initial_eth)
    output_state = PoolState(initial_usdc, initial_eth)
    
    initial_value = input_state.total_value_usdc(initial_price)
    print(f"Initial pool value: ${initial_value:,.0f}")
    
    # Run simulation
    print("\nProcessing swaps...")
    skipped = 0
    processed = 0
    
    for usdc_amt, eth_amt in parsed_swaps:
        # Determine direction
        if usdc_amt > 0 and eth_amt < 0:
            # Trader sells USDC, buys ETH
            try:
                input_state = apply_swap_input_fee(input_state, usdc_amt, 0)
                output_state = apply_swap_output_fee(output_state, usdc_amt, 0)
                processed += 1
            except:
                skipped += 1
        elif usdc_amt < 0 and eth_amt > 0:
            # Trader sells ETH, buys USDC
            try:
                input_state = apply_swap_input_fee(input_state, 0, eth_amt)
                output_state = apply_swap_output_fee(output_state, 0, eth_amt)
                processed += 1
            except:
                skipped += 1
        else:
            skipped += 1
    
    print(f"Processed: {processed}, Skipped: {skipped}")
    
    # Get final price
    final_price = input_state.price
    print(f"Final price: ${final_price:.2f}/ETH")
    
    # Calculate results
    input_final = input_state.total_value_usdc(final_price)
    output_final = output_state.total_value_usdc(final_price)
    
    input_return = (input_final / initial_value - 1) * 100
    output_return = (output_final / initial_value - 1) * 100
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    print("\n📊 Input-Fee Model (Standard):")
    print(f"   Final Value:     ${input_final:,.2f}")
    print(f"   Return:          {input_return:+.4f}%")
    print(f"   USDC Fees:       ${input_state.fees_collected0:,.2f}")
    print(f"   ETH Fees:        {input_state.fees_collected1:.4f} ETH")
    
    print("\n📊 Output-Fee Model (Proposed):")
    print(f"   Final Value:     ${output_final:,.2f}")
    print(f"   Return:          {output_return:+.4f}%")
    print(f"   USDC Fees:       ${output_state.fees_collected0:,.2f}")
    print(f"   ETH Fees:        {output_state.fees_collected1:.4f} ETH")
    
    print("\n" + "-" * 60)
    diff = output_return - input_return
    winner = "🏆 OUTPUT" if diff > 0 else "INPUT" if diff < 0 else "TIE"
    print(f"Difference:         {diff:+.4f}%")
    print(f"Winner:             {winner}")
    
    # Fee comparison
    input_fees_usdc = input_state.fees_collected0 + input_state.fees_collected1 * final_price
    output_fees_usdc = output_state.fees_collected0 + output_state.fees_collected1 * final_price
    print(f"\nTotal fees (input):  ${input_fees_usdc:,.2f}")
    print(f"Total fees (output): ${output_fees_usdc:,.2f}")
    print(f"Fee difference:      ${output_fees_usdc - input_fees_usdc:+,.2f}")
    
    # Save results
    results = {
        "swaps_processed": processed,
        "initial_price": initial_price,
        "final_price": final_price,
        "input_fee": {
            "return_pct": input_return,
            "final_value": input_final,
            "fees_usdc": input_state.fees_collected0,
            "fees_eth": input_state.fees_collected1
        },
        "output_fee": {
            "return_pct": output_return,
            "final_value": output_final,
            "fees_usdc": output_state.fees_collected0,
            "fees_eth": output_state.fees_collected1
        },
        "difference_pct": diff,
        "output_wins": diff > 0
    }
    
    with open("../results/real_backtest_june2024.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Results saved to results/real_backtest_june2024.json")


if __name__ == "__main__":
    main()
