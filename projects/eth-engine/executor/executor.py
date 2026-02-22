"""Hyperliquid ETH Executor - Main trading class."""
import logging
import time
from typing import Optional, Dict, List, Any

from hyperliquid import HyperliquidSync

logger = logging.getLogger(__name__)

# ETH trading pair on Hyperliquid
ETH_SYMBOL = "ETH"
ETH_CCXT = "ETH/USDC:USDC"


class HyperliquidExecutor:
    """Executor for ETH-only trading on Hyperliquid.
    
    Uses agent wallet pattern: private key for signing, 
    separate wallet address holds funds.
    """
    
    def __init__(self, private_key: str, wallet_address: str, testnet: bool = False):
        """Initialize executor with wallet credentials.
        
        Args:
            private_key: Agent wallet private key (hex string, 0x prefix)
            wallet_address: Wallet address that holds funds (0x...)
            testnet: Whether to use testnet (default: False)
        """
        self.wallet_address = wallet_address
        self.testnet = testnet
        
        # Initialize Hyperliquid sync
        self.hl = HyperliquidSync(
            private_key=private_key,
            wallet_address=wallet_address,
            testnet=testnet
        )
        
        logger.info(f"Initialized Hyperliquid executor for {wallet_address[:10]}... (testnet={testnet})")
    
    def get_balance(self) -> Dict[str, float]:
        """Get account balance information.
        
        Returns:
            dict: {equity, available, unrealized_pnl, wallet_balance} in USD
        """
        try:
            user_state = self.hl.get_user_state(self.wallet_address)
            if not user_state:
                logger.warning("No user state returned")
                return {"equity": 0.0, "available": 0.0, "unrealized_pnl": 0.0, "wallet_balance": 0.0}
            
            # Parse margin summary
            margin_summary = user_state.get("marginSummary", {})
            equity = float(margin_summary.get("totalValue", 0))
            available = float(margin_summary.get("available", 0))
            wallet_balance = float(margin_summary.get("walletBalance", 0))
            unrealized_pnl = float(margin_summary.get("unrealizedPnl", 0))
            
            return {
                "equity": equity,
                "available": available,
                "unrealized_pnl": unrealized_pnl,
                "wallet_balance": wallet_balance
            }
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return {"equity": 0.0, "available": 0.0, "unrealized_pnl": 0.0, "wallet_balance": 0.0}
    
    def get_position(self) -> Optional[Dict[str, Any]]:
        """Get current ETH position.
        
        Returns:
            dict: {side, size, entry_price, unrealized_pnl, leverage} or None
        """
        try:
            positions = self.hl.get_positions(self.wallet_address)
            if not positions:
                return None
            
            # Find ETH position
            for pos in positions:
                if pos.get("coin") == ETH_SYMBOL:
                    size = float(pos.get("size", 0))
                    if size == 0:
                        return None
                    
                    entry_price = float(pos.get("entryPrice", 0))
                    unrealized_pnl = float(pos.get("unrealizedPnl", 0))
                    leverage = float(pos.get("leverage", {"value": 0}).get("value", 0))
                    
                    # Determine side
                    side = "long" if size > 0 else "short"
                    size_usd = abs(size * entry_price)
                    
                    return {
                        "side": side,
                        "size": abs(size),
                        "size_usd": size_usd,
                        "entry_price": entry_price,
                        "unrealized_pnl": unrealized_pnl,
                        "leverage": leverage
                    }
            
            return None
        except Exception as e:
            logger.error(f"Error getting position: {e}")
            return None
    
    def get_market_price(self) -> float:
        """Get current ETH market price (mid price).
        
        Returns:
            float: ETH mid price in USDC
        """
        try:
            info = self.hl.get_info(self.wallet_address)
            asset_contexts = info.get("assetContexts", [])
            
            for ctx in asset_contexts:
                if ctx.get("coin") == ETH_SYMBOL:
                    mark_price = float(ctx.get("markPrice", 0))
                    oracle_price = float(ctx.get("oraclePrice", 0))
                    # Use oracle price as it's more accurate
                    return oracle_price if oracle_price > 0 else mark_price
            
            logger.warning("Could not find ETH price, returning 0")
            return 0.0
        except Exception as e:
            logger.error(f"Error getting market price: {e}")
            return 0.0
    
    def open_long(self, size_usd: float, leverage: int = 3) -> Dict[str, Any]:
        """Open a long position.
        
        Args:
            size_usd: Position size in USD
            leverage: Leverage multiplier (default: 3)
            
        Returns:
            dict: Order result with status
        """
        return self._open_position("long", size_usd, leverage)
    
    def open_short(self, size_usd: float, leverage: int = 3) -> Dict[str, Any]:
        """Open a short position.
        
        Args:
            size_usd: Position size in USD
            leverage: Leverage multiplier (default: 3)
            
        Returns:
            dict: Order result with status
        """
        return self._open_position("short", size_usd, leverage)
    
    def _open_position(self, side: str, size_usd: float, leverage: int) -> Dict[str, Any]:
        """Internal method to open a position.
        
        Args:
            side: "long" or "short"
            size_usd: Position size in USD
            leverage: Leverage multiplier
            
        Returns:
            dict: Order result
        """
        try:
            # First set leverage
            self._set_leverage(leverage)
            
            # Get current price and calculate size
            current_price = self.get_market_price()
            if current_price == 0:
                return {"success": False, "error": "Could not get market price"}
            
            size_eth = size_usd / current_price
            
            # Determine order side for Hyperliquid
            is_buy = side == "long"
            
            # Place market order
            order_result = self.hl.order(
                self.wallet_address,
                ETH_SYMBOL,
                is_buy=is_buy,
                size=size_eth,
                # Use 5 sig figs for price precision
                price=round(current_price, 5)
            )
            
            logger.info(f"Opened {side} position: {size_usd} USD @ {current_price}")
            return {"success": True, "side": side, "size_usd": size_usd, "price": current_price, "order": order_result}
            
        except Exception as e:
            logger.error(f"Error opening {side} position: {e}")
            return {"success": False, "error": str(e)}
    
    def close_position(self) -> Dict[str, Any]:
        """Close current position (market order).
        
        Returns:
            dict: Order result
        """
        try:
            position = self.get_position()
            if not position:
                return {"success": False, "error": "No position to close"}
            
            current_price = self.get_market_price()
            if current_price == 0:
                return {"success": False, "error": "Could not get market price"}
            
            # Close by trading opposite side
            is_buy = position["side"] == "short"
            
            order_result = self.hl.order(
                self.wallet_address,
                ETH_SYMBOL,
                is_buy=is_buy,
                size=position["size"],
                price=round(current_price, 5)
            )
            
            logger.info(f"Closed {position['side']} position: {position['size_usd']} USD")
            return {"success": True, "closed_side": position["side"], "order": order_result}
            
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return {"success": False, "error": str(e)}
    
    def _set_leverage(self, leverage: int) -> bool:
        """Set account leverage.
        
        Args:
            leverage: Leverage multiplier
            
        Returns:
            bool: Success status
        """
        try:
            self.hl.update_leverage(self.wallet_address, ETH_SYMBOL, leverage)
            logger.info(f"Set leverage to {leverage}x")
            return True
        except Exception as e:
            logger.error(f"Error setting leverage: {e}")
            return False
    
    def set_stop_loss(self, price: float) -> Dict[str, Any]:
        """Set stop loss order.
        
        Args:
            price: Stop loss trigger price
            
        Returns:
            dict: Order result
        """
        return self._set_trigger_order(price, "stop_loss")
    
    def set_take_profit(self, price: float) -> Dict[str, Any]:
        """Set take profit order.
        
        Args:
            price: Take profit trigger price
            
        Returns:
            dict: Order result
        """
        return self._set_trigger_order(price, "take_profit")
    
    def _set_trigger_order(self, price: float, order_type: str) -> Dict[str, Any]:
        """Set trigger order (stop loss or take profit).
        
        Args:
            price: Trigger price
            order_type: "stop_loss" or "take_profit"
            
        Returns:
            dict: Order result
        """
        try:
            position = self.get_position()
            if not position:
                return {"success": False, "error": "No position to set trigger on"}
            
            # Determine trigger side (opposite of position)
            is_buy = position["side"] == "short"
            
            # For stop loss: sell if long, buy if short
            # For take profit: same logic
            trigger_result = self.hl.trigger_order(
                self.wallet_address,
                ETH_SYMBOL,
                is_buy=is_buy,
                size=position["size"],
                trigger_price=round(price, 5),
                is_market=True
            )
            
            logger.info(f"Set {order_type} at {price}")
            return {"success": True, "type": order_type, "price": price, "order": trigger_result}
            
        except Exception as e:
            logger.error(f"Error setting {order_type}: {e}")
            return {"success": False, "error": str(e)}
    
    def cancel_all_orders(self) -> None:
        """Cancel all open orders."""
        try:
            self.hl.cancel_all(self.wallet_address)
            logger.info("Cancelled all orders")
        except Exception as e:
            logger.error(f"Error cancelling orders: {e}")
    
    def get_open_orders(self) -> List[Dict[str, Any]]:
        """Get list of open orders.
        
        Returns:
            list: List of open orders
        """
        try:
            orders = self.hl.get_open_orders(self.wallet_address)
            return orders if orders else []
        except Exception as e:
            logger.error(f"Error getting open orders: {e}")
            return []
    
    def get_recent_trades(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent trade fills.
        
        Args:
            limit: Maximum number of trades to return
            
        Returns:
            list: List of recent fills
        """
        try:
            # Get user's recent orders/fills
            user_state = self.hl.get_user_state(self.wallet_address)
            if not user_state:
                return []
            
            # Try to get fills from various endpoints
            # Note: API may vary, handle gracefully
            fills = user_state.get("fills", [])
            if fills:
                return fills[:limit]
            
            return []
        except Exception as e:
            logger.error(f"Error getting recent trades: {e}")
            return []
    
    def place_limit_order(self, side: str, size: float, price: float) -> Dict[str, Any]:
        """Place a limit order.
        
        Args:
            side: "long" or "short"
            size: Order size in ETH
            price: Limit price
            
        Returns:
            dict: Order result
        """
        try:
            is_buy = side == "long"
            
            order_result = self.hl.order(
                self.wallet_address,
                ETH_SYMBOL,
                is_buy=is_buy,
                size=size,
                price=round(price, 5)
            )
            
            logger.info(f"Placed limit {side} order: {size} ETH @ {price}")
            return {"success": True, "side": side, "size": size, "price": price, "order": order_result}
            
        except Exception as e:
            logger.error(f"Error placing limit order: {e}")
            return {"success": False, "error": str(e)}
