#!/usr/bin/env python3
"""
ETH Trading Decision Executor
Reads decision.json and executes trades on Hyperliquid
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add executor directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "executor"))

from executor import HyperliquidExecutor
from config import HL_PRIVATE_KEY, HL_WALLET_ADDRESS, HL_TESTNET, DEFAULT_LEVERAGE

# Configuration
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
DECISION_FILE = DATA_DIR / "decision.json"
TRADE_LOG_FILE = DATA_DIR / "trade-log.jsonl"
POSITION_STATE_FILE = DATA_DIR / "position-state.json"


def load_json_file(filepath: Path, default=None):
    """Load JSON file."""
    try:
        if filepath.exists():
            with open(filepath) as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
    return default


def save_json_file(filepath: Path, data: dict):
    """Save JSON file."""
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False


def log_trade(trade_data: dict):
    """Log trade to trade-log.jsonl."""
    try:
        with open(TRADE_LOG_FILE, "a") as f:
            f.write(json.dumps(trade_data) + "\n")
        return True
    except Exception as e:
        print(f"Error logging trade: {e}")
        return False


def update_position_state(executor: HyperliquidExecutor):
    """Update position-state.json."""
    try:
        position = executor.get_position()
        balance = executor.get_balance()
        open_orders = executor.get_open_orders()
        
        state = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "position": position,
            "balance": balance,
            "open_orders": open_orders,
            "eth_price": executor.get_market_price()
        }
        
        save_json_file(POSITION_STATE_FILE, state)
        return state
    except Exception as e:
        print(f"Error updating position state: {e}")
        return {}


def execute_decision(decision: dict, executor: HyperliquidExecutor) -> dict:
    """Execute a trading decision."""
    
    strategy = decision.get("strategy", "").lower()
    direction = decision.get("direction", "neutral").lower()
    size_usd = decision.get("size_usd", 25.0)
    leverage = decision.get("leverage", DEFAULT_LEVERAGE)
    entry_price = decision.get("entry_price")  # None for market, float for limit
    stop_loss = decision.get("stop_loss")
    take_profit = decision.get("take_profit")
    reasoning = decision.get("reasoning", "")
    confidence = decision.get("confidence", 50)
    
    print(f"\n=== Executing Decision ===")
    print(f"Strategy: {strategy}")
    print(f"Direction: {direction}")
    print(f"Size: ${size_usd} @ {leverage}x leverage")
    print(f"Entry: {'Market' if entry_price is None else entry_price}")
    print(f"SL: {stop_loss}, TP: {take_profit}")
    print(f"Confidence: {confidence}%")
    print(f"Reasoning: {reasoning}")
    
    # Get current position
    current_position = executor.get_position()
    print(f"\nCurrent position: {current_position}")
    
    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "strategy": strategy,
        "direction": direction,
        "size_usd": size_usd,
        "leverage": leverage,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "reasoning": reasoning,
        "confidence": confidence,
        "trades": [],
        "success": False,
        "error": None
    }
    
    try:
        # Handle different strategies
        if strategy == "close_all":
            # Close any existing position
            if current_position:
                close_result = executor.close_position()
                result["trades"].append({
                    "action": "close_position",
                    "side": current_position.get("side"),
                    "result": close_result
                })
                print(f"Closed position: {close_result}")
            else:
                print("No position to close")
            
            # Cancel all orders
            executor.cancel_all_orders()
            result["success"] = True
            
        elif strategy == "open_long":
            # Close existing position first
            if current_position:
                close_result = executor.close_position()
                result["trades"].append({
                    "action": "close_position",
                    "side": current_position.get("side"),
                    "result": close_result
                })
                print(f"Closed existing position: {close_result}")
            
            # Open long
            if entry_price is None:
                open_result = executor.open_long(size_usd, leverage)
            else:
                # Place limit order
                size_eth = size_usd / entry_price
                open_result = executor.place_limit_order("long", size_eth, entry_price)
            
            result["trades"].append({"action": "open_long", "result": open_result})
            print(f"Opened long: {open_result}")
            
            # Set SL/TP
            if stop_loss:
                sl_result = executor.set_stop_loss(stop_loss)
                result["trades"].append({"action": "set_stop_loss", "price": stop_loss, "result": sl_result})
                print(f"Set SL: {sl_result}")
            
            if take_profit:
                tp_result = executor.set_take_profit(take_profit)
                result["trades"].append({"action": "set_take_profit", "price": take_profit, "result": tp_result})
                print(f"Set TP: {tp_result}")
            
            result["success"] = open_result.get("success", False)
            
        elif strategy == "open_short":
            # Close existing position first
            if current_position:
                close_result = executor.close_position()
                result["trades"].append({
                    "action": "close_position",
                    "side": current_position.get("side"),
                    "result": close_result
                })
                print(f"Closed existing position: {close_result}")
            
            # Open short
            if entry_price is None:
                open_result = executor.open_short(size_usd, leverage)
            else:
                # Place limit order
                size_eth = size_usd / entry_price
                open_result = executor.place_limit_order("short", size_eth, entry_price)
            
            result["trades"].append({"action": "open_short", "result": open_result})
            print(f"Opened short: {open_result}")
            
            # Set SL/TP (note: for shorts, SL is above entry, TP is below)
            if stop_loss:
                sl_result = executor.set_stop_loss(stop_loss)
                result["trades"].append({"action": "set_stop_loss", "price": stop_loss, "result": sl_result})
                print(f"Set SL: {sl_result}")
            
            if take_profit:
                tp_result = executor.set_take_profit(take_profit)
                result["trades"].append({"action": "set_take_profit", "price": take_profit, "result": tp_result})
                print(f"Set TP: {tp_result}")
            
            result["success"] = open_result.get("success", False)
            
        elif strategy == "grid_trading":
            # Grid trading - implement via executor
            from grid import create_grid_from_market
            
            grid_params = decision.get("grid_params", {})
            num_levels = grid_params.get("levels", 5)
            range_pct = grid_params.get("range_pct", 0.03)  # 3% default
            
            if current_position:
                close_result = executor.close_position()
                result["trades"].append({"action": "close_position", "result": close_result})
            
            # Create and execute grid
            grid = create_grid_from_market(
                executor,
                num_grids=num_levels,
                total_usd=size_usd,
                range_pct=range_pct
            )
            grid_result = grid.sync_orders()
            result["trades"].append({"action": "grid_trading", "result": grid_result})
            result["success"] = True
            print(f"Grid trading: {grid_result}")
            
        elif strategy == "scale_in":
            # Scale into position - add to existing or start new
            if current_position and current_position.get("side") == direction:
                # Add to existing position
                if direction == "long":
                    open_result = executor.open_long(size_usd, leverage)
                else:
                    open_result = executor.open_short(size_usd, leverage)
                result["trades"].append({"action": "scale_in", "result": open_result})
                result["success"] = open_result.get("success", False)
            else:
                # Start new position
                if direction == "long":
                    open_result = executor.open_long(size_usd, leverage)
                else:
                    open_result = executor.open_short(size_usd, leverage)
                result["trades"].append({"action": "scale_in_new", "result": open_result})
                result["success"] = open_result.get("success", False)
                
        elif strategy == "reduce_exposure":
            # Reduce exposure - close partial or tighten SL/TP
            if current_position:
                # Close half position
                half_size = current_position.get("size", 0) / 2
                if half_size > 0:
                    # Close by trading opposite
                    is_buy = current_position.get("side") == "short"
                    current_price = executor.get_market_price()
                    close_result = executor.hl.order(
                        executor.wallet_address,
                        "ETH",
                        is_buy=is_buy,
                        size=half_size,
                        price=round(current_price, 5)
                    )
                    result["trades"].append({"action": "reduce_exposure", "result": close_result})
                    
                # Tighten SL if provided
                if stop_loss:
                    executor.set_stop_loss(stop_loss)
                    result["trades"].append({"action": "tighten_stop_loss", "price": stop_loss})
                    
                result["success"] = True
            else:
                print("No position to reduce")
                result["success"] = True
                
        elif strategy in ["mean_reversion", "funding_harvest"]:
            # Similar to open_long/short but with specific rationale
            if current_position:
                close_result = executor.close_position()
                result["trades"].append({"action": "close_position", "result": close_result})
            
            if direction == "long":
                open_result = executor.open_long(size_usd, leverage)
            elif direction == "short":
                open_result = executor.open_short(size_usd, leverage)
            else:
                open_result = {"success": False, "error": "No direction specified"}
                
            result["trades"].append({"action": strategy, "result": open_result})
            
            if stop_loss:
                executor.set_stop_loss(stop_loss)
            if take_profit:
                executor.set_take_profit(take_profit)
                
            result["success"] = open_result.get("success", False)
            
        else:
            result["error"] = f"Unknown strategy: {strategy}"
            print(f"ERROR: {result['error']}")
            
    except Exception as e:
        result["error"] = str(e)
        print(f"ERROR during execution: {e}")
    
    return result


def main():
    """Main execution function."""
    print("=== ETH Trading Decision Executor ===")
    
    # Load decision
    if not DECISION_FILE.exists():
        print(f"ERROR: Decision file not found: {DECISION_FILE}")
        sys.exit(1)
    
    decision = load_json_file(DECISION_FILE)
    if not decision:
        print("ERROR: Could not load decision.json")
        sys.exit(1)
    
    print(f"Loaded decision: {decision.get('strategy')} - {decision.get('direction')}")
    
    # Initialize executor
    try:
        executor = HyperliquidExecutor(HL_PRIVATE_KEY, HL_WALLET_ADDRESS, HL_TESTNET)
        print(f"Initialized executor for wallet: {HL_WALLET_ADDRESS[:10]}...")
    except Exception as e:
        print(f"ERROR initializing executor: {e}")
        sys.exit(1)
    
    # Get balance before trade
    balance_before = executor.get_balance()
    print(f"Balance before: {balance_before}")
    
    # Execute decision
    result = execute_decision(decision, executor)
    
    # Log trade
    trade_record = {
        "timestamp": result["timestamp"],
        "strategy": result["strategy"],
        "direction": result["direction"],
        "size_usd": result["size_usd"],
        "leverage": result["leverage"],
        "stop_loss": result["stop_loss"],
        "take_profit": result["take_profit"],
        "confidence": result["confidence"],
        "reasoning": result["reasoning"],
        "success": result["success"],
        "error": result["error"],
        "balance_before": balance_before.get("equity", 0),
        "trades": result["trades"]
    }
    log_trade(trade_record)
    print(f"\nTrade logged to {TRADE_LOG_FILE}")
    
    # Update position state
    update_position_state(executor)
    
    # Get balance after trade
    balance_after = executor.get_balance()
    print(f"Balance after: {balance_after}")
    
    # Print summary
    print("\n=== Execution Summary ===")
    print(f"Strategy: {result['strategy']}")
    print(f"Success: {result['success']}")
    if result.get("error"):
        print(f"Error: {result['error']}")
    print(f"Trades executed: {len(result['trades'])}")
    
    if not result["success"]:
        sys.exit(1)
    
    print("\n=== Complete ===")


if __name__ == "__main__":
    main()
