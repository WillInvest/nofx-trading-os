#!/usr/bin/env python3
"""
Monte Carlo simulation: Output-Fee vs Input-Fee AMMs under Concentrated Liquidity.

Extends base simulation to Uniswap v3-style concentrated liquidity pools.
Key question: Does the output fee advantage persist (or strengthen) with concentrated liquidity?

Author: OpenClaw Research Agent
Date: 2026-02-07
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Optional
import json
import sys


@dataclass
class ConcentratedPosition:
    """A single concentrated liquidity position."""
    tick_lower: int
    tick_upper: int
    liquidity: float  # L value
    
    def in_range(self, tick: int) -> bool:
        return self.tick_lower <= tick < self.tick_upper


@dataclass
class CLAMMState:
    """State of a Concentrated Liquidity AMM pool."""
    sqrt_price: float  # √P (Y per X)
    tick: int
    liquidity: float  # Active liquidity at current tick
    fee_collected_x: float = 0.0
    fee_collected_y: float = 0.0
    
    # For tracking virtual reserves at current liquidity
    @property
    def price(self) -> float:
        return self.sqrt_price ** 2
    
    def virtual_reserves(self) -> Tuple[float, float]:
        """Virtual x, y at current liquidity."""
        L = self.liquidity
        sqrt_p = self.sqrt_price
        x = L / sqrt_p
        y = L * sqrt_p
        return x, y
    
    def copy(self) -> 'CLAMMState':
        return CLAMMState(
            self.sqrt_price, self.tick, self.liquidity,
            self.fee_collected_x, self.fee_collected_y
        )


def price_to_tick(price: float, tick_spacing: int = 60) -> int:
    """Convert price to nearest tick."""
    tick = int(np.log(price) / np.log(1.0001))
    return (tick // tick_spacing) * tick_spacing


def tick_to_price(tick: int) -> float:
    """Convert tick to price."""
    return 1.0001 ** tick


def tick_to_sqrt_price(tick: int) -> float:
    """Convert tick to √price."""
    return 1.0001 ** (tick / 2)


def swap_cl_input_fee(state: CLAMMState, delta_x: float, phi: float,
                      tick_lower: int, tick_upper: int) -> Tuple[float, CLAMMState]:
    """
    Concentrated liquidity swap with INPUT-based fee.
    Simplified: assumes swap stays within current range.
    """
    new_state = state.copy()
    L = state.liquidity
    sqrt_p = state.sqrt_price
    
    if delta_x > 0:  # Selling X for Y
        # Apply fee to input
        effective_dx = phi * delta_x
        
        # New sqrt_price: 1/sqrt_p_new = 1/sqrt_p + dx/L
        new_sqrt_p_inv = (1 / sqrt_p) + (effective_dx / L)
        new_sqrt_p = 1 / new_sqrt_p_inv
        
        # Check bounds
        sqrt_p_lower = tick_to_sqrt_price(tick_lower)
        sqrt_p_upper = tick_to_sqrt_price(tick_upper)
        new_sqrt_p = max(sqrt_p_lower, min(sqrt_p_upper, new_sqrt_p))
        
        # delta_y = L * (sqrt_p - sqrt_p_new)
        delta_y = L * (sqrt_p - new_sqrt_p)
        
        new_state.sqrt_price = new_sqrt_p
        new_state.tick = price_to_tick(new_sqrt_p ** 2)
        new_state.fee_collected_x = state.fee_collected_x + (1 - phi) * delta_x
        
        return delta_y, new_state
    else:  # Selling Y for X
        delta_x_out = -delta_x
        
        # Need delta_y_in to get delta_x_out
        # sqrt_p_new = sqrt_p + dy/L → dy = L * (sqrt_p_new - sqrt_p)
        # 1/sqrt_p_new - 1/sqrt_p = -dx/L → dx = L * (1/sqrt_p - 1/sqrt_p_new)
        
        new_sqrt_p_inv = (1 / sqrt_p) - (delta_x_out / L)
        new_sqrt_p = 1 / new_sqrt_p_inv
        
        sqrt_p_lower = tick_to_sqrt_price(tick_lower)
        sqrt_p_upper = tick_to_sqrt_price(tick_upper)
        new_sqrt_p = max(sqrt_p_lower, min(sqrt_p_upper, new_sqrt_p))
        
        delta_y_in = L * (new_sqrt_p - sqrt_p)
        total_y_in = delta_y_in / phi  # Gross input with fee
        fee_y = total_y_in - delta_y_in
        
        new_state.sqrt_price = new_sqrt_p
        new_state.tick = price_to_tick(new_sqrt_p ** 2)
        new_state.fee_collected_y = state.fee_collected_y + fee_y
        
        return -total_y_in, new_state


def swap_cl_output_fee(state: CLAMMState, delta_x: float, phi: float,
                       tick_lower: int, tick_upper: int) -> Tuple[float, CLAMMState]:
    """
    Concentrated liquidity swap with OUTPUT-based fee.
    Simplified: assumes swap stays within current range.
    """
    new_state = state.copy()
    L = state.liquidity
    sqrt_p = state.sqrt_price
    
    if delta_x > 0:  # Selling X for Y
        # Full swap (no fee on input)
        new_sqrt_p_inv = (1 / sqrt_p) + (delta_x / L)
        new_sqrt_p = 1 / new_sqrt_p_inv
        
        sqrt_p_lower = tick_to_sqrt_price(tick_lower)
        sqrt_p_upper = tick_to_sqrt_price(tick_upper)
        new_sqrt_p = max(sqrt_p_lower, min(sqrt_p_upper, new_sqrt_p))
        
        delta_y_gross = L * (sqrt_p - new_sqrt_p)
        delta_y_net = phi * delta_y_gross
        fee_y = delta_y_gross - delta_y_net
        
        new_state.sqrt_price = new_sqrt_p
        new_state.tick = price_to_tick(new_sqrt_p ** 2)
        new_state.fee_collected_y = state.fee_collected_y + fee_y
        
        return delta_y_net, new_state
    else:  # Selling Y for X
        delta_x_out_gross = -delta_x
        
        # Compute Y needed for gross X output
        new_sqrt_p_inv = (1 / sqrt_p) - (delta_x_out_gross / L)
        new_sqrt_p = 1 / new_sqrt_p_inv
        
        sqrt_p_lower = tick_to_sqrt_price(tick_lower)
        sqrt_p_upper = tick_to_sqrt_price(tick_upper)
        new_sqrt_p = max(sqrt_p_lower, min(sqrt_p_upper, new_sqrt_p))
        
        delta_y_in = L * (new_sqrt_p - sqrt_p)
        
        # Fee on output (X)
        delta_x_net = phi * delta_x_out_gross
        fee_x = delta_x_out_gross - delta_x_net
        
        new_state.sqrt_price = new_sqrt_p
        new_state.tick = price_to_tick(new_sqrt_p ** 2)
        new_state.fee_collected_x = state.fee_collected_x + fee_x
        
        return -delta_y_in, new_state


def compute_cl_arbitrage_trade(amm_price: float, external_price: float,
                               liquidity: float, gamma: float,
                               sqrt_p_lower: float, sqrt_p_upper: float) -> float:
    """
    Compute optimal arbitrage trade size for concentrated liquidity.
    """
    sqrt_p = np.sqrt(amm_price)
    sqrt_p_ext = np.sqrt(external_price)
    
    # No arb if prices within fee band
    if abs(external_price - amm_price) / amm_price < gamma:
        return 0.0
    
    # Bound target price
    sqrt_p_target = max(sqrt_p_lower, min(sqrt_p_upper, sqrt_p_ext))
    
    if abs(sqrt_p_target - sqrt_p) < 1e-10:
        return 0.0
    
    # delta_x = L * (1/sqrt_p_new - 1/sqrt_p)
    delta_x = liquidity * (1/sqrt_p_target - 1/sqrt_p)
    
    # Account for fee approximately
    phi = 1 - gamma
    if delta_x > 0:
        delta_x = delta_x / phi
    else:
        delta_x = delta_x * phi
    
    return delta_x


def simulate_price_path(p0: float, sigma: float, n_blocks: int,
                        seed: int = None) -> np.ndarray:
    """Simulate GBM price path."""
    if seed is not None:
        np.random.seed(seed)
    
    log_returns = np.random.normal(0, sigma, n_blocks)
    log_prices = np.log(p0) + np.cumsum(log_returns)
    
    return np.exp(log_prices)


def run_cl_simulation(
    initial_price: float = 2000.0,  # USDC per ETH
    liquidity: float = 1e8,  # L value
    range_width: float = 0.2,  # ±10% around initial price
    fee_rate: float = 0.003,
    sigma: float = 0.01,
    n_blocks: int = 10000,
    seed: int = None
) -> dict:
    """
    Run concentrated liquidity comparison simulation.
    """
    phi = 1 - fee_rate
    
    # Set up range
    tick_spacing = 60
    center_tick = price_to_tick(initial_price, tick_spacing)
    tick_range = int(np.log(1 + range_width) / np.log(1.0001) / tick_spacing) * tick_spacing
    tick_lower = center_tick - tick_range
    tick_upper = center_tick + tick_range
    
    sqrt_p_lower = tick_to_sqrt_price(tick_lower)
    sqrt_p_upper = tick_to_sqrt_price(tick_upper)
    
    # Initialize pools
    sqrt_p0 = np.sqrt(initial_price)
    input_fee_pool = CLAMMState(sqrt_p0, center_tick, liquidity)
    output_fee_pool = CLAMMState(sqrt_p0, center_tick, liquidity)
    
    # Virtual reserves at start
    x0 = liquidity / sqrt_p0
    y0 = liquidity * sqrt_p0
    initial_value = x0 * initial_price + y0
    
    # Rebalancing portfolio
    rebal_x = x0
    rebal_y = y0
    
    # Generate price path
    prices = simulate_price_path(initial_price, sigma, n_blocks, seed)
    
    # Track out-of-range blocks
    blocks_in_range = 0
    
    for t, external_price in enumerate(prices):
        # Check if price is in range
        if sqrt_p_lower <= np.sqrt(external_price) <= sqrt_p_upper:
            blocks_in_range += 1
            
            # Arbitrage input-fee pool
            delta_x_input = compute_cl_arbitrage_trade(
                input_fee_pool.price, external_price,
                input_fee_pool.liquidity, fee_rate,
                sqrt_p_lower, sqrt_p_upper
            )
            if abs(delta_x_input) > 0.0001:
                _, input_fee_pool = swap_cl_input_fee(
                    input_fee_pool, delta_x_input, phi, tick_lower, tick_upper
                )
            
            # Arbitrage output-fee pool
            delta_x_output = compute_cl_arbitrage_trade(
                output_fee_pool.price, external_price,
                output_fee_pool.liquidity, fee_rate,
                sqrt_p_lower, sqrt_p_upper
            )
            if abs(delta_x_output) > 0.0001:
                _, output_fee_pool = swap_cl_output_fee(
                    output_fee_pool, delta_x_output, phi, tick_lower, tick_upper
                )
        
        # Update rebalancing portfolio
        total_value = rebal_x * external_price + rebal_y
        rebal_x = total_value / (2 * external_price)
        rebal_y = total_value / 2
    
    # Final valuations
    final_price = prices[-1]
    
    def cl_pool_value(state: CLAMMState, price: float) -> float:
        x, y = state.virtual_reserves()
        return (x + state.fee_collected_x) * price + y + state.fee_collected_y
    
    input_fee_value = cl_pool_value(input_fee_pool, final_price)
    output_fee_value = cl_pool_value(output_fee_pool, final_price)
    rebal_value = rebal_x * final_price + rebal_y
    hodl_value = x0 * final_price + y0
    
    return {
        "initial_price": initial_price,
        "final_price": final_price,
        "price_return": (final_price - initial_price) / initial_price,
        "initial_value": initial_value,
        "range": {
            "lower": tick_to_price(tick_lower),
            "upper": tick_to_price(tick_upper),
            "width": range_width,
        },
        "blocks_in_range_pct": blocks_in_range / n_blocks,
        
        "input_fee": {
            "final_value": input_fee_value,
            "return": (input_fee_value - initial_value) / initial_value,
            "lvr": (rebal_value - input_fee_value) / initial_value,
            "fees_x": input_fee_pool.fee_collected_x,
            "fees_y": input_fee_pool.fee_collected_y,
        },
        
        "output_fee": {
            "final_value": output_fee_value,
            "return": (output_fee_value - initial_value) / initial_value,
            "lvr": (rebal_value - output_fee_value) / initial_value,
            "fees_x": output_fee_pool.fee_collected_x,
            "fees_y": output_fee_pool.fee_collected_y,
        },
        
        "rebalancing": {"final_value": rebal_value},
        "hodl": {"final_value": hodl_value},
    }


def monte_carlo_cl(n_simulations: int = 100, **sim_kwargs) -> dict:
    """Run Monte Carlo for concentrated liquidity."""
    results = []
    
    for i in range(n_simulations):
        sim_kwargs['seed'] = i
        try:
            results.append(run_cl_simulation(**sim_kwargs))
        except Exception as e:
            print(f"Sim {i} failed: {e}", file=sys.stderr)
            continue
    
    if not results:
        return {"error": "All simulations failed"}
    
    input_returns = [r['input_fee']['return'] for r in results]
    output_returns = [r['output_fee']['return'] for r in results]
    input_lvr = [r['input_fee']['lvr'] for r in results]
    output_lvr = [r['output_fee']['lvr'] for r in results]
    in_range_pcts = [r['blocks_in_range_pct'] for r in results]
    
    return {
        "n_simulations": len(results),
        "parameters": sim_kwargs,
        "avg_in_range_pct": np.mean(in_range_pcts),
        
        "input_fee_stats": {
            "mean_return": np.mean(input_returns),
            "std_return": np.std(input_returns),
            "mean_lvr": np.mean(input_lvr),
        },
        
        "output_fee_stats": {
            "mean_return": np.mean(output_returns),
            "std_return": np.std(output_returns),
            "mean_lvr": np.mean(output_lvr),
        },
        
        "comparison": {
            "output_minus_input_return": np.mean(output_returns) - np.mean(input_returns),
            "lvr_reduction_pct": (np.mean(input_lvr) - np.mean(output_lvr)) / np.mean(input_lvr) * 100 if np.mean(input_lvr) > 0 else 0,
            "output_better_pct": sum(1 for i in range(len(results))
                                     if output_returns[i] > input_returns[i]) / len(results) * 100,
        }
    }


def run_range_width_sensitivity() -> dict:
    """Test how range width affects output fee advantage."""
    widths = [0.05, 0.1, 0.2, 0.5, 1.0]  # ±2.5% to ±50%
    results = {}
    
    for w in widths:
        print(f"Testing range width {w*100:.0f}%...")
        mc = monte_carlo_cl(n_simulations=100, range_width=w)
        results[f"±{w*50:.1f}%"] = {
            "lvr_reduction_pct": mc["comparison"]["lvr_reduction_pct"],
            "output_better_pct": mc["comparison"]["output_better_pct"],
            "avg_in_range": mc["avg_in_range_pct"],
        }
    
    return results


if __name__ == "__main__":
    print("Concentrated Liquidity: Output-Fee vs Input-Fee Comparison")
    print("=" * 60)
    
    # Single simulation
    print("\nSingle simulation (range ±10%)...")
    result = run_cl_simulation(range_width=0.2, seed=42)
    print(f"  Price: {result['initial_price']:.0f} → {result['final_price']:.0f}")
    print(f"  Range: {result['range']['lower']:.0f} - {result['range']['upper']:.0f}")
    print(f"  In range: {result['blocks_in_range_pct']*100:.1f}%")
    print(f"  Input fee return: {result['input_fee']['return']*100:.3f}%")
    print(f"  Output fee return: {result['output_fee']['return']*100:.3f}%")
    print(f"  Input LVR: {result['input_fee']['lvr']*100:.3f}%")
    print(f"  Output LVR: {result['output_fee']['lvr']*100:.3f}%")
    
    # Monte Carlo
    print("\n" + "=" * 60)
    print("Monte Carlo (100 simulations, ±10% range)...")
    mc = monte_carlo_cl(n_simulations=100, range_width=0.2)
    print(f"  Mean input return: {mc['input_fee_stats']['mean_return']*100:.3f}%")
    print(f"  Mean output return: {mc['output_fee_stats']['mean_return']*100:.3f}%")
    print(f"  Mean input LVR: {mc['input_fee_stats']['mean_lvr']*100:.3f}%")
    print(f"  Mean output LVR: {mc['output_fee_stats']['mean_lvr']*100:.3f}%")
    print(f"  LVR reduction: {mc['comparison']['lvr_reduction_pct']:.1f}%")
    print(f"  Output wins: {mc['comparison']['output_better_pct']:.0f}%")
    
    # Range width sensitivity
    print("\n" + "=" * 60)
    print("Range width sensitivity analysis...")
    sensitivity = run_range_width_sensitivity()
    print("\nResults by range width:")
    for width, data in sensitivity.items():
        print(f"  {width}: LVR reduction {data['lvr_reduction_pct']:.1f}%, "
              f"Output wins {data['output_better_pct']:.0f}%, "
              f"In-range {data['avg_in_range']*100:.0f}%")
    
    # Save results
    output = {
        "single_sim": result,
        "monte_carlo": mc,
        "sensitivity": sensitivity,
    }
    
    with open("../results/concentrated_liquidity_2026-02-07.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\nResults saved to experiments/results/concentrated_liquidity_2026-02-07.json")
