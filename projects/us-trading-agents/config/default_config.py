"""
Default configuration for US Trading Agents.
Copy to config/config.py and customize.
"""

from typing import Literal

DEFAULT_CONFIG = {
    # ===== LLM Settings =====
    "llm_provider": "ollama",  # ollama, openai, anthropic, google
    
    # Deep thinking model - for complex reasoning, debates, decisions
    "deep_think_llm": "llama3.3:70b",  # or "gpt-4o", "claude-3-opus"
    
    # Quick thinking model - for summarization, data extraction
    "quick_think_llm": "llama3.2:8b",  # or "gpt-4o-mini", "claude-3-haiku"
    
    # Temperature settings
    "deep_think_temperature": 0.7,
    "quick_think_temperature": 0.3,
    
    # ===== Agent Settings =====
    # Number of debate rounds between bull/bear researchers
    "max_debate_rounds": 3,
    
    # Risk management personas to use
    "risk_personas": ["aggressive", "neutral", "conservative"],
    
    # ===== Data Settings =====
    # Days of historical price data to fetch
    "price_lookback_days": 60,
    
    # Hours of news to analyze
    "news_lookback_hours": 72,
    
    # Number of Reddit posts to analyze
    "reddit_post_limit": 50,
    
    # Technical indicators to calculate
    "technical_indicators": [
        "RSI", "MACD", "SMA_20", "SMA_50", "SMA_200",
        "EMA_12", "EMA_26", "BB_upper", "BB_lower", "BB_middle",
        "ATR", "OBV", "VWAP", "ADX", "CCI"
    ],
    
    # ===== Trading Settings =====
    "initial_capital": 100000,
    
    # Maximum position size as percentage of portfolio
    "max_position_pct": 0.20,
    
    # Default stop loss percentage
    "default_stop_loss_pct": 0.05,
    
    # Default take profit percentage
    "default_take_profit_pct": 0.15,
    
    # Risk tolerance: conservative, moderate, aggressive
    "risk_tolerance": "moderate",
    
    # ===== API Keys (set via environment variables) =====
    # OPENAI_API_KEY
    # ANTHROPIC_API_KEY
    # FINNHUB_API_KEY
    # ALPHA_VANTAGE_API_KEY
    
    # ===== Output Settings =====
    "output_dir": "output",
    "save_reports": True,
    "save_decisions": True,
    "verbose": True,
}

# Model mappings for different providers
LLM_MODELS = {
    "ollama": {
        "deep": "llama3.3:70b",
        "quick": "llama3.2:8b",
    },
    "openai": {
        "deep": "gpt-4o",
        "quick": "gpt-4o-mini",
    },
    "anthropic": {
        "deep": "claude-3-5-sonnet-20241022",
        "quick": "claude-3-5-haiku-20241022",
    },
    "google": {
        "deep": "gemini-2.0-flash-thinking-exp",
        "quick": "gemini-2.0-flash",
    },
}

# Risk tolerance parameters
RISK_PARAMS = {
    "conservative": {
        "max_position_pct": 0.10,
        "stop_loss_pct": 0.03,
        "min_confidence": 0.75,
    },
    "moderate": {
        "max_position_pct": 0.20,
        "stop_loss_pct": 0.05,
        "min_confidence": 0.60,
    },
    "aggressive": {
        "max_position_pct": 0.30,
        "stop_loss_pct": 0.08,
        "min_confidence": 0.50,
    },
}
