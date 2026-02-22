"""CLI for Hyperliquid ETH Executor."""
import argparse
import json
import logging
import sys

from config import HL_PRIVATE_KEY, HL_WALLET_ADDRESS, HL_TESTNET, LOG_FORMAT, LOG_LEVEL
from executor import HyperliquidExecutor
from strategies import StrategyDispatcher

# Setup logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Hyperliquid ETH Executor")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # execute command
    exec_parser = subparsers.add_parser("execute", help="Execute trading strategy from decision.json")
    exec_parser.add_argument("--decision", "-d", help="Path to decision.json", default=None)
    
    # status command
    subparsers.add_parser("status", help="Show current status")
    
    # close command
    subparsers.add_parser("close", help="Close current position")
    
    # cancel command
    subparsers.add_parser("cancel", help="Cancel all orders")
    
    args = parser.parse_args()
    
    # Validate credentials
    if not HL_PRIVATE_KEY or not HL_WALLET_ADDRESS:
        logger.error("Missing HL_PRIVATE_KEY or HL_WALLET_ADDRESS")
        print("Error: Set HL_PRIVATE_KEY and HL_WALLET_ADDRESS environment variables")
        sys.exit(1)
    
    # Initialize executor
    try:
        executor = HyperliquidExecutor(
            private_key=HL_PRIVATE_KEY,
            wallet_address=HL_WALLET_ADDRESS,
            testnet=HL_TESTNET
        )
    except Exception as e:
        logger.error(f"Failed to initialize executor: {e}")
        print(f"Error: {e}")
        sys.exit(1)
    
    # Route command
    if args.command == "execute":
        execute_strategy(executor, args.decision)
    elif args.command == "status":
        show_status(executor)
    elif args.command == "close":
        close_position(executor)
    elif args.command == "cancel":
        cancel_orders(executor)
    else:
        parser.print_help()


def execute_strategy(executor: HyperliquidExecutor, decision_path: str = None):
    """Execute trading strategy."""
    dispatcher = StrategyDispatcher(executor)
    result = dispatcher.execute(decision_path)
    
    print(json.dumps(result, indent=2, default=str))
    
    if result.get("success"):
        logger.info("Strategy executed successfully")
    else:
        logger.error(f"Strategy execution failed: {result.get('error')}")
        sys.exit(1)


def show_status(executor: HyperliquidExecutor):
    """Show current account status."""
    balance = executor.get_balance()
    position = executor.get_position()
    price = executor.get_market_price()
    orders = executor.get_open_orders()
    
    status = {
        "market_price": price,
        "balance": balance,
        "position": position,
        "open_orders": len(orders)
    }
    
    print(json.dumps(status, indent=2, default=str))


def close_position(executor: HyperliquidExecutor):
    """Close current position."""
    result = executor.close_position()
    print(json.dumps(result, indent=2, default=str))
    
    if result.get("success"):
        logger.info("Position closed successfully")
    else:
        logger.error(f"Failed to close position: {result.get('error')}")
        sys.exit(1)


def cancel_orders(executor: HyperliquidExecutor):
    """Cancel all orders."""
    executor.cancel_all_orders()
    print(json.dumps({"success": True, "message": "All orders cancelled"}, indent=2))


if __name__ == "__main__":
    main()
