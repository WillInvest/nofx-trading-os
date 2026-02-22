"""Hyperliquid ETH Executor - Main trading class."""
import json
import logging
import time
import urllib.request
import urllib.error
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
        
        # Initialize Hyperliquid sync with ccxt-style config
        # BUG FIX: API changed - now uses config dict instead of kwargs
        config = {
            'privateKey': private_key,
            'walletAddress': wallet_address,
            'enableRateLimit': True,
        }
        if testnet:
            # Testnet uses different URL - check if supported
            config['options'] = {'testnet': True}
        
        self.hl = HyperliquidSync(config)
        
        logger.info(f"Initialized Hyperliquid executor for {wallet_address[:10]}... (testnet={testnet})")
    
    @staticmethod
    def _hl_api_call(payload: dict) -> Optional[dict]:
        """Direct REST call to Hyperliquid info API."""
        try:
            req = urllib.request.Request(
                "https://api.hyperliquid.xyz/info",
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read())
        except Exception as e:
            logger.error(f"Hyperliquid API call failed ({payload.get('type', '?')}): {e}")
            return None

    def get_balance(self) -> Dict[str, float]:
        """Get account balance information.
        
        Supports Unified Account mode where Spot USDC is used as
        collateral for Perpetual trading. Queries both spot and perp
        clearinghouse states via direct REST API.
        
        Returns:
            dict: {equity, available, unrealized_pnl, wallet_balance, spot_usdc} in USD
        """
        result = {
            "equity": 0.0,
            "available": 0.0,
            "unrealized_pnl": 0.0,
            "wallet_balance": 0.0,
            "spot_usdc": 0.0
        }
        try:
            # 1. Query Spot balance
            spot_usdc = 0.0
            spot_state = self._hl_api_call({
                "type": "spotClearinghouseState",
                "user": self.wallet_address
            })
            if spot_state and isinstance(spot_state, dict):
                for b in spot_state.get("balances", []):
                    if b.get("coin") == "USDC":
                        spot_usdc = float(b.get("total", 0))
                        break
            result["spot_usdc"] = spot_usdc

            # 2. Query Perp state
            perp_equity = 0.0
            perp_available = 0.0
            unrealized_pnl = 0.0
            perp_state = self._hl_api_call({
                "type": "clearinghouseState",
                "user": self.wallet_address
            })
            if perp_state and isinstance(perp_state, dict):
                margin = perp_state.get("crossMarginSummary", perp_state.get("marginSummary", {}))
                perp_equity = float(margin.get("accountValue", 0))
                total_margin_used = float(margin.get("totalMarginUsed", 0))
                perp_available = perp_equity - total_margin_used
                # Sum unrealized PnL from positions
                for ap in perp_state.get("assetPositions", []):
                    pos = ap.get("position", {})
                    unrealized_pnl += float(pos.get("unrealizedPnl", 0))

            # 3. Compute unified equity
            # In unified mode, perp accountValue already includes spot as collateral.
            # If perp shows 0 but spot has USDC, use spot as equity.
            if perp_equity > 0:
                equity = perp_equity
            else:
                equity = spot_usdc

            available = max(perp_available, 0) if perp_equity > 0 else spot_usdc

            result["equity"] = equity
            result["available"] = available
            result["unrealized_pnl"] = unrealized_pnl
            result["wallet_balance"] = equity - unrealized_pnl

            return result
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return result
    
    def get_position(self) -> Optional[Dict[str, Any]]:
        """Get current ETH position.
        
        Returns:
            dict: {side, size, entry_price, unrealized_pnl, leverage} or None
        """
        try:
            # Use ccxt-style fetch_positions
            positions = self.hl.fetch_positions()
            if not positions:
                return None
            
            # Find ETH position
            for pos in positions:
                info = pos.get('info', {})
                coin = info.get('coin', '')
                if coin == ETH_SYMBOL:
                    size = float(info.get('size', 0))
                    if size == 0:
                        return None
                    
                    entry_price = float(info.get('entryPrice', 0))
                    unrealized_pnl = float(info.get('unrealizedPnl', 0))
                    leverage_val = info.get('leverage', {})
                    leverage = float(leverage_val.get('value', 0)) if isinstance(leverage_val, dict) else float(leverage_val)
                    
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
            # Use ccxt-style fetch_ticker
            ticker = self.hl.fetch_ticker(ETH_CCXT)
            # Use last price or mid price
            return float(ticker.get('last', 0)) or float(ticker.get('mid', 0)) or 0.0
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
            
            # Place market order using ccxt-style create_order
            order_result = self.hl.create_order(
                symbol=ETH_CCXT,
                type='market',
                side='buy' if is_buy else 'sell',
                amount=size_eth,
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
            
            order_result = self.hl.create_order(
                symbol=ETH_CCXT,
                type='market',
                side='buy' if is_buy else 'sell',
                amount=position["size"],
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
            # Use ccxt-style set_leverage
            self.hl.set_leverage(leverage, ETH_CCXT)
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
            
            # Use ccxt-style trigger order
            trigger_result = self.hl.create_order(
                symbol=ETH_CCXT,
                type='stop_market',
                side='buy' if is_buy else 'sell',
                amount=position["size"],
                params={
                    'triggerPrice': round(price, 5),
                    'reduceOnly': True
                }
            )
            
            logger.info(f"Set {order_type} at {price}")
            return {"success": True, "type": order_type, "price": price, "order": trigger_result}
            
        except Exception as e:
            logger.error(f"Error setting {order_type}: {e}")
            return {"success": False, "error": str(e)}
    
    def cancel_all_orders(self) -> None:
        """Cancel all open orders."""
        try:
            self.hl.cancel_all_orders(ETH_CCXT)
            logger.info("Cancelled all orders")
        except Exception as e:
            logger.error(f"Error cancelling orders: {e}")
    
    def get_open_orders(self) -> List[Dict[str, Any]]:
        """Get list of open orders.
        
        Returns:
            list: List of open orders
        """
        try:
            # Use ccxt-style fetch_open_orders
            orders = self.hl.fetch_open_orders(ETH_CCXT)
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
            # Use ccxt-style fetch_my_trades
            trades = self.hl.fetch_my_trades(ETH_CCXT, limit=limit)
            return trades if trades else []
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
            
            # Use ccxt-style create_order for limit order
            order_result = self.hl.create_order(
                symbol=ETH_CCXT,
                type='limit',
                side='buy' if is_buy else 'sell',
                amount=size,
                price=round(price, 5)
            )
            
            logger.info(f"Placed limit {side} order: {size} ETH @ {price}")
            return {"success": True, "side": side, "size": size, "price": price, "order": order_result}
            
        except Exception as e:
            logger.error(f"Error placing limit order: {e}")
            return {"success": False, "error": str(e)}
