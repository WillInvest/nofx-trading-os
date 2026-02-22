"""Grid trading strategy for ETH on Hyperliquid."""
import logging
from typing import List, Dict, Any, Optional

from executor import HyperliquidExecutor

logger = logging.getLogger(__name__)


class GridStrategy:
    """Grid trading strategy for ETH.
    
    Places buy orders at lower prices and sell orders at higher prices
    within a price range to capture volatility.
    """
    
    def __init__(
        self,
        executor: HyperliquidExecutor,
        lower: float,
        upper: float,
        num_grids: int = 5,
        total_usd: float = 25.0,
        leverage: int = 3
    ):
        """Initialize grid strategy.
        
        Args:
            executor: HyperliquidExecutor instance
            lower: Lower price bound for grid
            upper: Upper price bound for grid
            num_grids: Number of grid levels (default: 5)
            total_usd: Total USD to allocate (default: 25.0)
            leverage: Leverage multiplier (default: 3)
        """
        self.executor = executor
        self.lower = lower
        self.upper = upper
        self.num_grids = num_grids
        self.total_usd = total_usd
        self.leverage = leverage
        
        # Calculate price step
        self.price_step = (upper - lower) / (num_grids - 1) if num_grids > 1 else 0
        
        # USD per grid level
        self.usd_per_level = total_usd / num_grids
        
        # Track active orders
        self.grid_levels: List[Dict[str, Any]] = []
        
        logger.info(f"Grid strategy initialized: {lower}-{upper}, {num_grids} levels, ${total_usd}")
    
    def calculate_grid_levels(self) -> List[Dict[str, Any]]:
        """Calculate grid levels with side and size.
        
        Returns:
            list: List of {price, side, size, status} for each grid level
        """
        current_price = self.executor.get_market_price()
        levels = []
        
        for i in range(self.num_grids):
            price = self.lower + (i * self.price_step)
            
            # Determine side: buy below current price, sell above
            # Alternate sides for a balanced grid
            if current_price > 0:
                if price < current_price:
                    side = "long"  # Buy low
                else:
                    side = "short"  # Sell high
            else:
                # Default: even numbered = long, odd = short
                side = "long" if i % 2 == 0 else "short"
            
            # Calculate size in ETH
            size_eth = self.usd_per_level / price
            
            levels.append({
                "price": round(price, 5),
                "side": side,
                "size": size_eth,
                "size_usd": self.usd_per_level,
                "status": "pending"
            })
        
        self.grid_levels = levels
        return levels
    
    def sync_orders(self) -> Dict[str, Any]:
        """Sync grid orders with exchange.
        
        Compare desired grid levels vs current open orders,
        place new orders and cancel stale ones.
        
        Returns:
            dict: Sync result with placed/cancelled counts
        """
        result = {"placed": 0, "cancelled": 0, "errors": []}
        
        try:
            # Get current open orders
            open_orders = self.executor.get_open_orders()
            open_prices = {round(float(o.get("price", 0)), 5) for o in open_orders}
            
            # Calculate desired levels
            desired_levels = self.calculate_grid_levels()
            
            # Cancel orders that are not in our grid
            for order in open_orders:
                order_price = round(float(order.get("price", 0)), 5)
                # Check if this order matches any desired level
                matched = any(
                    abs(level["price"] - order_price) < 0.01 
                    for level in desired_levels
                )
                if not matched:
                    try:
                        self.executor.cancel_all_orders()
                        result["cancelled"] += 1
                    except Exception as e:
                        result["errors"].append(f"Cancel error: {e}")
            
            # Place new orders for grid levels
            for level in desired_levels:
                if level["price"] not in open_prices:
                    try:
                        order_result = self.executor.place_limit_order(
                            side=level["side"],
                            size=level["size"],
                            price=level["price"]
                        )
                        if order_result.get("success"):
                            result["placed"] += 1
                            level["status"] = "active"
                        else:
                            result["errors"].append(order_result.get("error", "Unknown error"))
                    except Exception as e:
                        result["errors"].append(f"Place order error: {e}")
            
            logger.info(f"Grid sync: placed={result['placed']}, cancelled={result['cancelled']}")
            
        except Exception as e:
            logger.error(f"Error syncing grid orders: {e}")
            result["errors"].append(str(e))
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get grid strategy status for dashboard.
        
        Returns:
            dict: Status information
        """
        current_price = self.executor.get_market_price()
        position = self.executor.get_position()
        balance = self.executor.get_balance()
        
        return {
            "strategy": "grid",
            "active": len(self.grid_levels) > 0,
            "lower": self.lower,
            "upper": self.upper,
            "num_grids": self.num_grids,
            "total_usd": self.total_usd,
            "current_price": current_price,
            "grid_levels": self.grid_levels,
            "position": position,
            "balance": balance,
            "leverage": self.leverage
        }
    
    def adjust_range(self, lower: float, upper: float) -> None:
        """Adjust grid range dynamically.
        
        Args:
            lower: New lower bound
            upper: New upper bound
        """
        if lower >= upper:
            logger.warning(f"Invalid range: {lower} >= {upper}")
            return
        
        self.lower = lower
        self.upper = upper
        self.price_step = (upper - lower) / (self.num_grids - 1)
        
        logger.info(f"Grid range adjusted to {lower}-{upper}")
        
        # Sync with new range
        self.sync_orders()


def create_grid_from_market(
    executor: HyperliquidExecutor,
    num_grids: int = 5,
    total_usd: float = 25.0,
    range_pct: float = 0.05
) -> GridStrategy:
    """Create grid strategy based on current market price.
    
    Args:
        executor: HyperliquidExecutor instance
        num_grids: Number of grid levels
        total_usd: Total USD to allocate
        range_pct: Price range as percentage of current price (default: 5%)
    
    Returns:
        GridStrategy: Configured grid strategy
    """
    current_price = executor.get_market_price()
    if current_price == 0:
        raise ValueError("Could not get current market price")
    
    lower = current_price * (1 - range_pct)
    upper = current_price * (1 + range_pct)
    
    return GridStrategy(
        executor=executor,
        lower=round(lower, 5),
        upper=round(upper, 5),
        num_grids=num_grids,
        total_usd=total_usd
    )
