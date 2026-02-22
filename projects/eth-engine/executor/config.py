"""Configuration from environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()

HL_PRIVATE_KEY = os.getenv("HL_PRIVATE_KEY", "")
HL_WALLET_ADDRESS = os.getenv("HL_WALLET_ADDRESS", "")
HL_TESTNET = os.getenv("HL_TESTNET", "false").lower() in ("true", "1", "yes")

# Trading defaults
DEFAULT_LEVERAGE = 3
DEFAULT_ETH_SIZE = 25.0  # USD
GRID_NUM_LEVELS = 5
GRID_TOTAL_USD = 25.0

# Logging
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
