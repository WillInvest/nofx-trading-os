#!/usr/bin/env python3
"""
Monte Carlo simulation comparing Input-Fee vs Output-Fee AMMs.

Research question: How do LP returns differ under different fee structures?

Author: OpenClaw Research Agent
Date: 2026-02-07
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, List
import json


@dataclass
class AMMState:
    """State of an AMM pool."""
    x: float  # Reserve of token X (e.g., ETH)
    y: float  # Reserve of token Y (e.g., USDC)
    fee_collected_x: float = 0.0  # Fees collected in X
    fee_collected_y: float = 0.0  # Fees collected in Y
    
    @property
    def price(self) -> float:
        """Spot price: Y per X."""
        return self.y / self.x
    
    @property
    def k(self) -> float:
        """Invariant."""
        return self.x * self.y
    
    def copy(self) -> 'AMMState':
        return AMMState(self.x, self.y, self.fee_collected_x, self.fee_collected_y)


def swap_input_fee(state: AMMState, delta_x: float, phi: float) -> Tuple[float, AMMState]:
    """
    Swap with INPUT-based fee (standard Uniswap style).
    
    Args:
        state: Current AMM state
        delta_x: Amount of X being sold (positive) or bought (negative)
        phi: Fee multiplier (0.997 for 0.3% fee)
    
    Returns:
        (delta_y, new_state): Amount of Y received and new state
    """
    new_state = state.copy()
    
    if delta_x > 0:  # Selling X for Y
        effective_input = phi * delta_x
        delta_y = (state.y * effective_input) / (state.x + effective_input)
        
        new_state.x = state.x + delta_x
        new_state.y = state.y - delta_y
        new_state.fee_collected_x = state.fee_collected_x + (1 - phi) * delta_x
        
        return delta_y, new_state
    else:  # Selling Y for X (delta_x negative means buying X)
        # Need to solve for delta_y that gives us delta_x out
        delta_x_out = -delta_x
        delta_y_in = (state.y * delta_x_out) / (state.x - delta_x_out)
        effective_input = delta_y_in / phi  # Total Y needed
        fee_y = effective_input - delta_y_in
        
        new_state.x = state.x - delta_x_out
        new_state.y = state.y + effective_input
        new_state.fee_collected_y = state.fee_collected_y + fee_y
        
        return -effective_input, new_state


def swap_output_fee(state: AMMState, delta_x: float, phi: float) -> Tuple[float, AMMState]:
    """
    Swap with OUTPUT-based fee.
    
    Args:
        state: Current AMM state
        delta_x: Amount of X being sold (positive)
        phi: Fee multiplier (0.997 for 0.3% fee)
    
    Returns:
        (delta_y_net, new_state): Net amount of Y received and new state
    """
    new_state = state.copy()
    
    if delta_x > 0:  # Selling X for Y
        # Full swap calculation (no fee on input)
        delta_y_gross = (state.y * delta_x) / (state.x + delta_x)
        delta_y_net = phi * delta_y_gross
        fee_y = delta_y_gross - delta_y_net
        
        new_state.x = state.x + delta_x
        new_state.y = state.y - delta_y_net  # Only net amount leaves pool
        new_state.fee_collected_y = state.fee_collected_y + fee_y
        
        return delta_y_net, new_state
    else:  # Selling Y for X
        delta_x_out = -delta_x
        delta_y_in = (state.y * delta_x_out) / (state.x - delta_x_out)
        
        # Fee on output (X)
        delta_x_net = phi * delta_x_out
        fee_x = delta_x_out - delta_x_net
        
        new_state.x = state.x - delta_x_net
        new_state.y = state.y + delta_y_in
        new_state.fee_collected_x = state.fee_collected_x + fee_x
        
        return -delta_y_in, new_state


def compute_arbitrage_trade(amm_price: float, external_price: float, 
                            x: float, y: float, gamma: float) -> float:
    """
    Compute optimal arbitrage trade size.
    
    Args:
        amm_price: Current AMM price (Y per X)
        external_price: External market price (Y per X)
        x, y: Current reserves
        gamma: Fee rate (e.g., 0.003 for 0.3%)
    
    Returns:
        Optimal trade size in X (positive = sell X, negative = buy X)
    """
    if abs(external_price - amm_price) / amm_price < gamma:
        return 0.0  # No arbitrage opportunity
    
    # Simplified: trade to move AMM price toward external price
    # Target: y_new / x_new = external_price
    # With constant product: x_new * y_new = x * y
    
    target_x = np.sqrt(x * y / external_price)
    target_y = np.sqrt(x * y * external_price)
    
    delta_x = target_x - x
    
    # Account for fee (approximately)
    phi = 1 - gamma
    if delta_x > 0:
        delta_x = delta_x / phi  # Need to send more to account for fee
    else:
        delta_x = delta_x * phi  # Receive less due to fee
    
    return delta_x


def simulate_price_path(p0: float, sigma: float, n_blocks: int, 
                        seed: int = None) -> np.ndarray:
    """
    Simulate GBM price path.
    
    Args:
        p0: Initial price
        sigma: Volatility per block
        n_blocks: Number of blocks
        seed: Random seed
    
    Returns:
        Array of prices
    """
    if seed is not None:
        np.random.seed(seed)
    
    log_returns = np.random.normal(0, sigma, n_blocks)
    log_prices = np.log(p0) + np.cumsum(log_returns)
    
    return np.exp(log_prices)


def run_simulation(
    initial_x: float = 100.0,
    initial_y: float = 200000.0,  # ~2000 USDC per ETH
    fee_rate: float = 0.003,
    sigma: float = 0.01,  # ~1% per block
    n_blocks: int = 10000,
    seed: int = None
) -> dict:
    """
    Run comparison simulation.
    
    Returns:
        Dictionary with results for both fee types
    """
    phi = 1 - fee_rate
    
    # Initialize identical pools
    input_fee_pool = AMMState(initial_x, initial_y)
    output_fee_pool = AMMState(initial_x, initial_y)
    
    # Rebalancing portfolio baseline
    rebal_x = initial_x
    rebal_y = initial_y
    
    # Generate external price path
    p0 = initial_y / initial_x
    prices = simulate_price_path(p0, sigma, n_blocks, seed)
    
    # Track metrics
    input_fee_lvr = 0.0
    output_fee_lvr = 0.0
    
    for t, external_price in enumerate(prices):
        # Compute and execute arbitrage for input-fee pool
        delta_x_input = compute_arbitrage_trade(
            input_fee_pool.price, external_price,
            input_fee_pool.x, input_fee_pool.y, fee_rate
        )
        if abs(delta_x_input) > 0.0001:
            _, input_fee_pool = swap_input_fee(input_fee_pool, delta_x_input, phi)
        
        # Compute and execute arbitrage for output-fee pool
        delta_x_output = compute_arbitrage_trade(
            output_fee_pool.price, external_price,
            output_fee_pool.x, output_fee_pool.y, fee_rate
        )
        if abs(delta_x_output) > 0.0001:
            _, output_fee_pool = swap_output_fee(output_fee_pool, delta_x_output, phi)
        
        # Update rebalancing portfolio (tracks external price)
        # Value = x * p + y, want to maintain 50/50
        total_value = rebal_x * external_price + rebal_y
        rebal_x = total_value / (2 * external_price)
        rebal_y = total_value / 2
    
    # Final valuations at final external price
    final_price = prices[-1]
    
    def pool_value(state: AMMState, price: float) -> float:
        return (state.x + state.fee_collected_x) * price + state.y + state.fee_collected_y
    
    input_fee_value = pool_value(input_fee_pool, final_price)
    output_fee_value = pool_value(output_fee_pool, final_price)
    rebal_value = rebal_x * final_price + rebal_y
    hodl_value = initial_x * final_price + initial_y
    
    initial_value = initial_x * p0 + initial_y
    
    return {
        "initial_price": p0,
        "final_price": final_price,
        "price_return": (final_price - p0) / p0,
        "initial_value": initial_value,
        
        "input_fee": {
            "final_value": input_fee_value,
            "return": (input_fee_value - initial_value) / initial_value,
            "lvr": (rebal_value - input_fee_value) / initial_value,
            "vs_hodl": (input_fee_value - hodl_value) / initial_value,
            "fees_x": input_fee_pool.fee_collected_x,
            "fees_y": input_fee_pool.fee_collected_y,
            "final_x": input_fee_pool.x,
            "final_y": input_fee_pool.y,
        },
        
        "output_fee": {
            "final_value": output_fee_value,
            "return": (output_fee_value - initial_value) / initial_value,
            "lvr": (rebal_value - output_fee_value) / initial_value,
            "vs_hodl": (output_fee_value - hodl_value) / initial_value,
            "fees_x": output_fee_pool.fee_collected_x,
            "fees_y": output_fee_pool.fee_collected_y,
            "final_x": output_fee_pool.x,
            "final_y": output_fee_pool.y,
        },
        
        "rebalancing": {
            "final_value": rebal_value,
        },
        
        "hodl": {
            "final_value": hodl_value,
        }
    }


def monte_carlo(n_simulations: int = 1000, **sim_kwargs) -> dict:
    """Run Monte Carlo simulation."""
    results = []
    
    for i in range(n_simulations):
        sim_kwargs['seed'] = i
        results.append(run_simulation(**sim_kwargs))
    
    # Aggregate statistics
    input_returns = [r['input_fee']['return'] for r in results]
    output_returns = [r['output_fee']['return'] for r in results]
    input_lvr = [r['input_fee']['lvr'] for r in results]
    output_lvr = [r['output_fee']['lvr'] for r in results]
    
    return {
        "n_simulations": n_simulations,
        "parameters": sim_kwargs,
        
        "input_fee_stats": {
            "mean_return": np.mean(input_returns),
            "std_return": np.std(input_returns),
            "mean_lvr": np.mean(input_lvr),
            "std_lvr": np.std(input_lvr),
        },
        
        "output_fee_stats": {
            "mean_return": np.mean(output_returns),
            "std_return": np.std(output_returns),
            "mean_lvr": np.mean(output_lvr),
            "std_lvr": np.std(output_lvr),
        },
        
        "comparison": {
            "output_minus_input_return": np.mean(output_returns) - np.mean(input_returns),
            "output_minus_input_lvr": np.mean(output_lvr) - np.mean(input_lvr),
            "output_better_pct": sum(1 for i in range(len(results)) 
                                     if output_returns[i] > input_returns[i]) / len(results),
        }
    }


if __name__ == "__main__":
    print("Running single simulation...")
    result = run_simulation(seed=42)
    print(json.dumps(result, indent=2))
    
    print("\n" + "="*50)
    print("Running Monte Carlo (100 simulations)...")
    mc_result = monte_carlo(n_simulations=100)
    print(json.dumps(mc_result, indent=2))
