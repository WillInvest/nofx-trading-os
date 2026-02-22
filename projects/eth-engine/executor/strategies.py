"""Strategy dispatcher for ETH trading on Hyperliquid."""
import json
import logging
import os
from typing import Dict, Any, Optional

from executor import HyperliquidExecutor
from grid import GridStrategy, create_grid_from_market

logger = logging.getLogger(__name__)

# Decision file path
DECISION_FILE = os.path.join(os.path.dirname(__file__), "..", "decision.json")


class StrategyDispatcher:
    """Dispatcher for executing trading strategies based on decisions."""
    
    def __init__(self, executor: HyperliquidExecutor):
        """Initialize dispatcher.
        
        Args:
            executor: HyperliquidExecutor instance
        """
        self.executor = executor
        self.current_strategy: Optional[Any] = None
        self.last_decision: Optional[Dict[str, Any]] = None
    
    def load_decision(self, path: str = None) -> Optional[Dict[str, Any]]:
        """Load decision from JSON file.
        
        Args:
            path: Path to decision.json (default: uses DECISION_FILE)
        
        Returns:
            dict: Decision data or None
        """
        decision_path = path or DECISION_FILE
        
        if not os.path.exists(decision_path):
            logger.warning(f"Decision file not found: {decision_path}")
            return None
        
        try:
            with open(decision_path, "r") as f:
                decision = json.load(f)
            
            self.last_decision = decision
            logger.info(f"Loaded decision: {decision.get('strategy')} (confidence: {decision.get('confidence')})")
            return decision
            
        except Exception as e:
            logger.error(f"Error loading decision: {e}")
            return None
    
    def execute(self, decision: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a trading strategy based on decision.
        
        Args:
            decision: Decision dict. If None, loads from file.
        
        Returns:
            dict: Execution result
        """
        if decision is None:
            decision = self.load_decision()
        
        if not decision:
            return {"success": False, "error": "No decision available"}
        
        strategy = decision.get("strategy", "").lower()
        confidence = decision.get("confidence", 0)
        params = decision.get("params", {})
        reasoning = decision.get("reasoning", "")
        
        logger.info(f"Executing strategy: {strategy} (confidence: {confidence}%)")
        logger.info(f"Reasoning: {reasoning}")
        
        # Route to appropriate strategy
        if strategy == "grid_trading":
            return self._execute_grid_trading(params)
        elif strategy == "funding_harvest":
            return self._execute_funding_harvest(params)
        elif strategy == "mean_reversion":
            return self._execute_mean_reversion(params)
        elif strategy == "breakout":
            return self._execute_breakout(params)
        elif strategy == "open_long":
            return self._execute_open_long(params)
        elif strategy == "open_short":
            return self._execute_open_short(params)
        else:
            logger.warning(f"Unknown strategy: {strategy}")
            return {"success": False, "error": f"Unknown strategy: {strategy}"}
    
    def _execute_grid_trading(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute grid trading strategy.
        
        Args:
            params: Strategy parameters (lower, upper, num_grids, total_usd)
        
        Returns:
            dict: Execution result
        """
        try:
            lower = params.get("lower")
            upper = params.get("upper")
            num_grids = params.get("num_grids", 5)
            total_usd = params.get("total_usd", 25.0)
            
            if lower is None or upper is None:
                # Create from market
                grid = create_grid_from_market(
                    self.executor,
                    num_grids=num_grids,
                    total_usd=total_usd
                )
            else:
                grid = GridStrategy(
                    executor=self.executor,
                    lower=lower,
                    upper=upper,
                    num_grids=num_grids,
                    total_usd=total_usd
                )
            
            result = grid.sync_orders()
            self.current_strategy = grid
            
            return {
                "success": True,
                "strategy": "grid_trading",
                "result": result,
                "status": grid.get_status()
            }
            
        except Exception as e:
            logger.error(f"Grid trading error: {e}")
            return {"success": False, "error": str(e)}
    
    def _execute_funding_harvest(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute funding rate harvest strategy.
        
        Args:
            params: Strategy parameters
        
        Returns:
            dict: Execution result
        """
        try:
            # Check current funding rate (would need to fetch from exchange)
            # For now, implement simple long/short based on funding
            
            leverage = params.get("leverage", 3)
            size_usd = params.get("size_usd", 25.0)
            
            # Get position - close if exists
            position = self.executor.get_position()
            if position:
                self.executor.close_position()
            
            # Open based on funding direction (simplified)
            # In practice, you'd check actual funding rates
            result = self.executor.open_long(size_usd, leverage)
            
            return {
                "success": result.get("success", False),
                "strategy": "funding_harvest",
                "action": "opened_long",
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Funding harvest error: {e}")
            return {"success": False, "error": str(e)}
    
    def _execute_mean_reversion(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute mean reversion strategy.
        
        Args:
            params: Strategy parameters (window, std_dev)
        
        Returns:
            dict: Execution result
        """
        try:
            current_price = self.executor.get_market_price()
            
            # In practice, you'd calculate moving average and std dev
            # For now, simple implementation
            window = params.get("window", 20)
            std_dev = params.get("std_dev", 2.0)
            
            position = self.executor.get_position()
            
            # Check if we should close
            if position:
                self.executor.close_position()
            
            # Open position (simplified - would need actual MA calculation)
            leverage = params.get("leverage", 3)
            size_usd = params.get("size_usd", 25.0)
            
            # Determine direction based on params
            direction = params.get("direction", "long")
            if direction == "long":
                result = self.executor.open_long(size_usd, leverage)
            else:
                result = self.executor.open_short(size_usd, leverage)
            
            return {
                "success": result.get("success", False),
                "strategy": "mean_reversion",
                "current_price": current_price,
                "action": f"opened_{direction}",
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Mean reversion error: {e}")
            return {"success": False, "error": str(e)}
    
    def _execute_breakout(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute breakout strategy.
        
        Args:
            params: Strategy parameters (breakout_threshold)
        
        Returns:
            dict: Execution result
        """
        try:
            current_price = self.executor.get_market_price()
            threshold = params.get("breakout_threshold", 0.02)  # 2%
            
            # In practice, you'd check price vs resistance/support
            # For now, open position based on params
            leverage = params.get("leverage", 3)
            size_usd = params.get("size_usd", 25.0)
            direction = params.get("direction", "long")
            
            position = self.executor.get_position()
            if position:
                self.executor.close_position()
            
            if direction == "long":
                result = self.executor.open_long(size_usd, leverage)
            else:
                result = self.executor.open_short(size_usd, leverage)
            
            return {
                "success": result.get("success", False),
                "strategy": "breakout",
                "current_price": current_price,
                "action": f"opened_{direction}",
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Breakout error: {e}")
            return {"success": False, "error": str(e)}
    
    def _execute_open_long(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute simple long opening.
        
        Args:
            params: Strategy parameters (size_usd, leverage)
        
        Returns:
            dict: Execution result
        """
        try:
            # Close any existing position first
            position = self.executor.get_position()
            if position:
                self.executor.close_position()
            
            size_usd = params.get("size_usd", 25.0)
            leverage = params.get("leverage", 3)
            
            result = self.executor.open_long(size_usd, leverage)
            return {
                "success": result.get("success", False),
                "strategy": "open_long",
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Open long error: {e}")
            return {"success": False, "error": str(e)}
    
    def _execute_open_short(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute simple short opening.
        
        Args:
            params: Strategy parameters (size_usd, leverage)
        
        Returns:
            dict: Execution result
        """
        try:
            # Close any existing position first
            position = self.executor.get_position()
            if position:
                self.executor.close_position()
            
            size_usd = params.get("size_usd", 25.0)
            leverage = params.get("leverage", 3)
            
            result = self.executor.open_short(size_usd, leverage)
            return {
                "success": result.get("success", False),
                "strategy": "open_short",
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Open short error: {e}")
            return {"success": False, "error": str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """Get current strategy status.
        
        Returns:
            dict: Status information
        """
        balance = self.executor.get_balance()
        position = self.executor.get_position()
        open_orders = self.executor.get_open_orders()
        
        status = {
            "current_strategy": self.last_decision.get("strategy") if self.last_decision else None,
            "balance": balance,
            "position": position,
            "open_orders_count": len(open_orders),
            "last_decision": self.last_decision
        }
        
        if self.current_strategy and hasattr(self.current_strategy, "get_status"):
            status["strategy_status"] = self.current_strategy.get_status()
        
        return status
