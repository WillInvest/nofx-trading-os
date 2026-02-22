# Project-wide constants for FE621 HW1

# Tickers we're analyzing
TICKERS_EQUITY = ["TSLA", "SPY"]
TICKER_VIX = "^VIX"

# Federal funds effective rate from H.15 release (as of 2026-02-12)
RISK_FREE_RATE = 0.0364
RISK_FREE_RATE_DATE = "2026-02-12"

# Moneyness band for ATM classification (Q6)
MONEYNESS_LOWER = 0.95
MONEYNESS_UPPER = 1.05

# Root-finding parameters
TOLERANCE = 1e-6
MAX_ITER = 1000
IV_LOWER = 0.001  # lower bound for IV search
IV_UPPER = 5.0    # upper bound for IV search

OUTPUT_DIR = "output"
