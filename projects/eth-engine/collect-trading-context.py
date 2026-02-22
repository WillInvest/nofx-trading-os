#!/usr/bin/env python3
"""
ETH Trading Context Collector
Collects all market data, computes indicators, and outputs trading-context.json
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add executor directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / "executor"))

import numpy as np

# Configuration
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
ARENA_DIR = Path("/home/openclaw/.openclaw/workspace/projects/nofx-project/arena")

# Import executor modules (after adding to path)
# For price and candles, we use REST API directly (no auth needed)
# For position/balance, we try HyperliquidSync with ccxt-style init
from config import HL_PRIVATE_KEY, HL_WALLET_ADDRESS, HL_TESTNET

# Try importing HyperliquidExecutor - may fail if API changed
try:
    from executor import HyperliquidExecutor
    HAS_EXECUTOR = True
except ImportError:
    HAS_EXECUTOR = False
    print("Warning: HyperliquidExecutor not available, using fallback")


def api_post(url: str, data: Dict) -> Any:
    """Make POST request to API."""
    req = urllib.request.Request(url, json.dumps(data).encode(), {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"API POST error to {url}: HTTP {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"API POST error to {url}: {e}")
        return None


def load_json_file(filepath: Path, default: Any = None) -> Any:
    """Load JSON file, return default if not found."""
    try:
        if filepath.exists():
            with open(filepath) as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
    return default


def get_hyperliquid_price() -> float:
    """Fetch ETH price from Hyperliquid REST API (no auth needed)."""
    data = {"type": "allMids"}
    result = api_post("https://api.hyperliquid.xyz/info", data)
    
    if result and isinstance(result, dict) and "ETH" in result:
        return float(result["ETH"])
    return 0.0


def get_hyperliquid_candles(coin: str = "ETH", interval: str = "1h", num_candles: int = 200) -> List[Dict]:
    """Fetch candle data from Hyperliquid."""
    now_ms = int(time.time() * 1000)
    
    # Calculate start time based on interval
    if interval == "5m":
        start_ms = now_ms - (num_candles * 5 * 60 * 1000)
    elif interval == "1d":
        start_ms = now_ms - (num_candles * 24 * 60 * 60 * 1000)
    else:  # 1h
        start_ms = now_ms - (num_candles * 60 * 60 * 1000)
    
    # BUG FIX: params must be nested under "req" and need BOTH startTime and endTime
    data = {
        "type": "candleSnapshot",
        "req": {
            "coin": coin,
            "interval": interval,
            "startTime": start_ms,
            "endTime": now_ms
        }
    }
    result = api_post("https://api.hyperliquid.xyz/info", data)
    
    if result and isinstance(result, list):
        # Convert to our format: {t, T, o, h, l, c, v}
        candles = []
        for r in result:
            candles.append({
                "t": r.get("t", 0),
                "T": r.get("T", 0),
                "o": float(r.get("o", 0)),
                "h": float(r.get("h", 0)),
                "l": float(r.get("l", 0)),
                "c": float(r.get("c", 0)),
                "v": float(r.get("v", 0))
            })
        return candles
    return []


# ============================================================
# TECHNICAL INDICATORS (self-computed)
# ============================================================

def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Safe division."""
    return a / b if b != 0 and not np.isnan(b) and not np.isinf(b) else default


def sma(values: np.ndarray, period: int) -> np.ndarray:
    """Simple Moving Average."""
    if len(values) < period:
        return np.full(len(values), np.nan)
    result = np.convolve(values, np.ones(period)/period, mode='valid')
    # Pad with NaNs
    return np.concatenate([np.full(period-1, np.nan), result])


def ema(values: np.ndarray, period: int) -> np.ndarray:
    """Exponential Moving Average."""
    if len(values) < period:
        return np.full(len(values), np.nan)
    ema_arr = np.full(len(values), np.nan)
    ema_arr[period-1] = np.mean(values[:period])
    multiplier = 2 / (period + 1)
    for i in range(period, len(values)):
        ema_arr[i] = (values[i] - ema_arr[i-1]) * multiplier + ema_arr[i-1]
    return ema_arr


def rsi(values: np.ndarray, period: int = 14) -> np.ndarray:
    """Relative Strength Index."""
    if len(values) < period + 1:
        return np.full(len(values), np.nan)
    
    deltas = np.diff(values)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    
    rsi_arr = np.full(len(values), np.nan)
    if avg_loss == 0:
        rsi_arr[period:] = 100
        return rsi_arr
    
    rs = avg_gain / avg_loss
    rsi_arr[period-1] = 100 - (100 / (1 + rs))
    
    for i in range(period, len(values)):
        avg_gain = (avg_gain * (period - 1) + gains[i-1]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i-1]) / period
        if avg_loss == 0:
            rsi_arr[i] = 100
        else:
            rs = avg_gain / avg_loss
            rsi_arr[i] = 100 - (100 / (1 + rs))
    
    return rsi_arr


def macd(values: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
    """MACD: (macd_line, signal_line, histogram)."""
    if len(values) < slow:
        return (np.full(len(values), np.nan), np.full(len(values), np.nan), np.full(len(values), np.nan))
    
    ema_fast = ema(values, fast)
    ema_slow = ema(values, slow)
    
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line[~np.isnan(macd_line)], signal) if len(macd_line[~np.isnan(macd_line)]) >= signal else np.full(len(values), np.nan)
    
    # Pad signal line
    if len(signal_line) < len(values):
        signal_line = np.concatenate([np.full(len(values) - len(signal_line), np.nan), signal_line])
    
    histogram = macd_line - signal_line
    return (macd_line, signal_line, histogram)


def bollinger_bands(values: np.ndarray, period: int = 20, std_dev: float = 2.0) -> tuple:
    """Bollinger Bands: (upper, middle, lower)."""
    if len(values) < period:
        return (np.full(len(values), np.nan), np.full(len(values), np.nan), np.full(len(values), np.nan))
    
    middle = sma(values, period)
    std = np.array([np.std(values[i-period:i]) if i >= period else np.nan for i in range(len(values))])
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    return (upper, middle, lower)


def atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
    """Average True Range."""
    if len(high) < period + 1:
        return np.full(len(high), np.nan)
    
    tr = np.zeros(len(high))
    tr[0] = high[0] - low[0]
    for i in range(1, len(high)):
        tr[i] = max(
            high[i] - low[i],
            abs(high[i] - close[i-1]),
            abs(low[i] - close[i-1])
        )
    
    atr_arr = np.full(len(high), np.nan)
    atr_arr[period-1] = np.mean(tr[:period])
    for i in range(period, len(tr)):
        atr_arr[i] = (atr_arr[i-1] * (period - 1) + tr[i]) / period
    
    return atr_arr


def stochastic_rsi(close: np.ndarray, rsi_period: int = 14, k_period: int = 3, d_period: int = 3) -> tuple:
    """Stochastic RSI: (%K, %D)."""
    rsival = rsi(close, rsi_period)
    
    if len(rsival) < rsi_period + k_period:
        return (np.full(len(close), np.nan), np.full(len(close), np.nan))
    
    k_arr = np.full(len(close), np.nan)
    d_arr = np.full(len(close), np.nan)
    
    for i in range(rsi_period - 1, len(close)):
        window = rsival[max(0, i - k_period + 1):i + 1]
        window = window[~np.isnan(window)]
        if len(window) >= k_period:
            lowest = np.min(window)
            highest = np.max(window)
            if highest != lowest:
                k_arr[i] = 100 * (rsival[i] - lowest) / (highest - lowest)
            else:
                k_arr[i] = 50
    
    # %D is SMA of %K
    for i in range(k_period - 1, len(close)):
        window = k_arr[max(0, i - d_period + 1):i + 1]
        window = window[~np.isnan(window)]
        if len(window) >= d_period:
            d_arr[i] = np.mean(window)
    
    return (k_arr, d_arr)


def williams_r(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
    """Williams %R."""
    if len(close) < period:
        return np.full(len(close), np.nan)
    
    wr_arr = np.full(len(close), np.nan)
    for i in range(period - 1, len(close)):
        highest = np.max(high[i - period + 1:i + 1])
        lowest = np.min(low[i - period + 1:i + 1])
        if highest != lowest:
            wr_arr[i] = -100 * (highest - close[i]) / (highest - lowest)
        else:
            wr_arr[i] = -50
    
    return wr_arr


def cci(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 20) -> np.ndarray:
    """Commodity Channel Index."""
    if len(close) < period:
        return np.full(len(close), np.nan)
    
    typical_price = (high + low + close) / 3
    sma_tp = sma(typical_price, period)
    
    cci_arr = np.full(len(close), np.nan)
    for i in range(period - 1, len(close)):
        if not np.isnan(sma_tp[i]):
            mean_dev = np.mean(np.abs(typical_price[max(0, i-period+1):i+1] - sma_tp[i]))
            if mean_dev != 0:
                cci_arr[i] = (typical_price[i] - sma_tp[i]) / (0.015 * mean_dev)
    
    return cci_arr


def obv(close: np.ndarray, volume: np.ndarray) -> np.ndarray:
    """On-Balance Volume."""
    obv_arr = np.zeros(len(close))
    if len(close) > 0:
        obv_arr[0] = volume[0] if volume[0] else 0
        for i in range(1, len(close)):
            if close[i] > close[i-1]:
                obv_arr[i] = obv_arr[i-1] + (volume[i] if volume[i] else 0)
            elif close[i] < close[i-1]:
                obv_arr[i] = obv_arr[i-1] - (volume[i] if volume[i] else 0)
            else:
                obv_arr[i] = obv_arr[i-1]
    return obv_arr


def mfi(high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray, period: int = 14) -> np.ndarray:
    """Money Flow Index."""
    if len(close) < period + 1:
        return np.full(len(close), np.nan)
    
    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume
    
    mfi_arr = np.full(len(close), np.nan)
    
    for i in range(period, len(close)):
        positive_flow = 0
        negative_flow = 0
        
        for j in range(i - period + 1, i + 1):
            if typical_price[j] > typical_price[j-1] if j > 0 else False:
                positive_flow += money_flow[j]
            else:
                negative_flow += money_flow[j]
        
        if negative_flow != 0:
            mfi_arr[i] = 100 - (100 / (1 + positive_flow / negative_flow))
        else:
            mfi_arr[i] = 100
    
    return mfi_arr


def vwap(high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray) -> float:
    """Volume Weighted Average Price (returns last value)."""
    if len(close) == 0:
        return 0.0
    
    typical_price = (high + low + close) / 3
    cumulative_tp_vol = np.cumsum(typical_price * volume)
    cumulative_vol = np.cumsum(volume)
    
    vwap_arr = cumulative_tp_vol / np.where(cumulative_vol > 0, cumulative_vol, 1)
    return float(vwap_arr[-1]) if len(vwap_arr) > 0 else 0.0


def compute_indicators_1h(candles: List[Dict]) -> Dict[str, Any]:
    """Compute indicators for 1H candles."""
    if len(candles) < 20:
        return {}
    
    close = np.array([c["c"] for c in candles])
    high = np.array([c["h"] for c in candles])
    low = np.array([c["l"] for c in candles])
    volume = np.array([c["v"] for c in candles])
    
    # Get last values
    def last_val(arr, default=0.0):
        valid = arr[~np.isnan(arr)]
        return float(valid[-1]) if len(valid) > 0 else default
    
    return {
        "sma_7": round(last_val(sma(close, 7)), 2),
        "sma_25": round(last_val(sma(close, 25)), 2),
        "sma_99": round(last_val(sma(close, 99)), 2),
        "ema_12": round(last_val(ema(close, 12)), 2),
        "ema_26": round(last_val(ema(close, 26)), 2),
        "rsi_14": round(last_val(rsi(close, 14)), 2),
        "macd_line": round(last_val(macd(close, 12, 26, 9)[0]), 4),
        "macd_signal": round(last_val(macd(close, 12, 26, 9)[1]), 4),
        "macd_histogram": round(last_val(macd(close, 12, 26, 9)[2]), 4),
        "bollinger_upper": round(last_val(bollinger_bands(close, 20, 2.0)[0]), 2),
        "bollinger_middle": round(last_val(bollinger_bands(close, 20, 2.0)[1]), 2),
        "bollinger_lower": round(last_val(bollinger_bands(close, 20, 2.0)[2]), 2),
        "atr_14": round(last_val(atr(high, low, close, 14)), 2),
        "stoch_rsi_k": round(last_val(stochastic_rsi(close)[0]), 2),
        "stoch_rsi_d": round(last_val(stochastic_rsi(close)[1]), 2),
        "williams_r": round(last_val(williams_r(high, low, close, 14)), 2),
        "cci_20": round(last_val(cci(high, low, close, 20)), 2),
        "obv": round(last_val(obv(close, volume)), 2),
        "mfi_14": round(last_val(mfi(high, low, close, volume, 14)), 2),
        "vwap": round(vwap(high, low, close, volume), 2),
    }


def compute_indicators_5m(candles: List[Dict]) -> Dict[str, Any]:
    """Compute indicators for 5m candles."""
    if len(candles) < 20:
        return {}
    
    close = np.array([c["c"] for c in candles])
    volume = np.array([c["v"] for c in candles])
    
    def last_val(arr, default=0.0):
        valid = arr[~np.isnan(arr)]
        return float(valid[-1]) if len(valid) > 0 else default
    
    # Volume vs average
    vol_avg = np.mean(volume[-20:]) if len(volume) >= 20 else np.mean(volume)
    vol_ratio = volume[-1] / vol_avg if vol_avg > 0 else 1.0
    
    return {
        "ema_12": round(last_val(ema(close, 12)), 2),
        "ema_26": round(last_val(ema(close, 26)), 2),
        "rsi_14": round(last_val(rsi(close, 14)), 2),
        "volume_ratio": round(vol_ratio, 2),
    }


def compute_indicators_daily(candles: List[Dict]) -> Dict[str, Any]:
    """Compute indicators for Daily candles."""
    if len(candles) < 20:
        return {}
    
    close = np.array([c["c"] for c in candles])
    
    def last_val(arr, default=0.0):
        valid = arr[~np.isnan(arr)]
        return float(valid[-1]) if len(valid) > 0 else default
    
    return {
        "sma_20": round(last_val(sma(close, 20)), 2),
        "sma_50": round(last_val(sma(close, 50)), 2),
        "rsi_14": round(last_val(rsi(close, 14)), 2),
    }


def get_trade_streak(trades: List[Dict]) -> Dict[str, Any]:
    """Calculate current win/loss streak from trade history."""
    if not trades:
        return {"streak": 0, "direction": "none", "recent_pnl": 0.0}
    
    # Sort by timestamp descending
    sorted_trades = sorted(trades, key=lambda x: x.get("timestamp", ""), reverse=True)
    
    streak = 0
    direction = "none"
    
    if len(sorted_trades) > 0:
        first_pnl = sorted_trades[0].get("pnl", 0)
        direction = "win" if first_pnl > 0 else "loss" if first_pnl < 0 else "none"
        
        for trade in sorted_trades:
            pnl = trade.get("pnl", 0)
            if (direction == "win" and pnl > 0) or (direction == "loss" and pnl < 0):
                streak += 1
            else:
                break
    
    recent_pnl = sum(t.get("pnl", 0) for t in sorted_trades[:5])
    
    return {
        "streak": streak,
        "direction": direction,
        "recent_pnl": round(recent_pnl, 2)
    }


def load_trade_history() -> List[Dict]:
    """Load trade history from log file."""
    trade_file = DATA_DIR / "trade-log.jsonl"
    trades = []
    try:
        if trade_file.exists():
            with open(trade_file) as f:
                for line in f:
                    try:
                        trades.append(json.loads(line.strip()))
                    except:
                        pass
    except Exception as e:
        print(f"Error loading trade history: {e}")
    return trades


def main():
    """Main collection function."""
    print("=== ETH Trading Context Collector ===")
    
    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "eth_price": 0.0,
        "candles_1h": [],
        "candles_5m": [],
        "candles_daily": [],
        "indicators_1h": {},
        "indicators_5m": {},
        "indicators_daily": {},
        "position": None,
        "balance": {},
        "open_orders": [],
        "market_data": {},
        "onchain_data": {},
        "protocol_data": {},
        "news": {},
        "recent_trades": [],
        "trade_streak": {}
    }
    
    # 1. Get ETH price from Hyperliquid (REST API - no auth needed)
    print("Fetching ETH price...")
    try:
        # Try REST API first (works without auth)
        result["eth_price"] = get_hyperliquid_price()
        if result["eth_price"] > 0:
            print(f"  ETH price: ${result['eth_price']}")
        else:
            raise ValueError("Price was 0")
    except Exception as e:
        print(f"  Error getting price from API: {e}")
        # Fallback: try HyperliquidExecutor if available
        try:
            if HAS_EXECUTOR:
                executor = HyperliquidExecutor(HL_PRIVATE_KEY, HL_WALLET_ADDRESS, HL_TESTNET)
                result["eth_price"] = executor.get_market_price()
                print(f"  ETH price (via executor): ${result['eth_price']}")
        except Exception as e2:
            print(f"  Executor also failed: {e2}")
    
    # 2. Fetch candles
    print("Fetching 1H candles...")
    candles_1h = get_hyperliquid_candles("ETH", "1h", 200)
    result["candles_1h"] = candles_1h
    print(f"  Got {len(candles_1h)} 1H candles")
    
    print("Fetching 5m candles...")
    candles_5m = get_hyperliquid_candles("ETH", "5m", 120)
    result["candles_5m"] = candles_5m
    print(f"  Got {len(candles_5m)} 5m candles")
    
    print("Fetching Daily candles...")
    candles_daily = get_hyperliquid_candles("ETH", "1d", 30)
    result["candles_daily"] = candles_daily
    print(f"  Got {len(candles_daily)} Daily candles")
    
    # 3. Compute indicators
    print("Computing indicators...")
    result["indicators_1h"] = compute_indicators_1h(candles_1h)
    result["indicators_5m"] = compute_indicators_5m(candles_5m)
    result["indicators_daily"] = compute_indicators_daily(candles_daily)
    print(f"  1H indicators: {list(result['indicators_1h'].keys())[:5]}...")
    print(f"  5m indicators: {list(result['indicators_5m'].keys())}")
    print(f"  Daily indicators: {list(result['indicators_daily'].keys())}")
    
    # 4. Get position and balance (direct REST API for Unified Account support)
    print("Getting position and balance...")
    try:
        # Query Spot balance
        spot_usdc = 0.0
        spot_state = api_post("https://api.hyperliquid.xyz/info", {
            "type": "spotClearinghouseState",
            "user": HL_WALLET_ADDRESS
        })
        if spot_state and isinstance(spot_state, dict):
            for b in spot_state.get("balances", []):
                if b.get("coin") == "USDC":
                    spot_usdc = float(b.get("total", 0))
                    break
            print(f"  Spot USDC: {spot_usdc}")

        # Query Perp state
        perp_equity = 0.0
        perp_available = 0.0
        unrealized_pnl = 0.0
        position = None
        perp_state = api_post("https://api.hyperliquid.xyz/info", {
            "type": "clearinghouseState",
            "user": HL_WALLET_ADDRESS
        })
        if perp_state and isinstance(perp_state, dict):
            margin = perp_state.get("crossMarginSummary", perp_state.get("marginSummary", {}))
            perp_equity = float(margin.get("accountValue", 0))
            total_margin_used = float(margin.get("totalMarginUsed", 0))
            perp_available = perp_equity - total_margin_used

            # Find ETH position from assetPositions
            for ap in perp_state.get("assetPositions", []):
                pos = ap.get("position", {})
                if pos.get("coin") == "ETH":
                    size = float(pos.get("szi", 0))
                    if size != 0:
                        entry_price = float(pos.get("entryPx", 0))
                        upnl = float(pos.get("unrealizedPnl", 0))
                        lev = pos.get("leverage", {})
                        leverage = float(lev.get("value", 0)) if isinstance(lev, dict) else float(lev)
                        side = "long" if size > 0 else "short"
                        position = {
                            "side": side,
                            "size": abs(size),
                            "size_usd": abs(size * entry_price),
                            "entry_price": entry_price,
                            "unrealized_pnl": upnl,
                            "leverage": leverage
                        }
                # Sum all unrealized PnL
                unrealized_pnl += float(pos.get("unrealizedPnl", 0))

        # Compute unified equity
        if perp_equity > 0:
            equity = perp_equity
        else:
            equity = spot_usdc
        available = max(perp_available, 0) if perp_equity > 0 else spot_usdc

        result["position"] = position
        result["balance"] = {
            "equity": equity,
            "available": available,
            "unrealized_pnl": unrealized_pnl,
            "wallet_balance": equity - unrealized_pnl,
            "spot_usdc": spot_usdc,
            "perp_equity": perp_equity
        }
        print(f"  Position: {result['position']}")
        print(f"  Balance: {result['balance']}")

        # Get open orders via executor if available
        if HAS_EXECUTOR:
            try:
                executor = HyperliquidExecutor(HL_PRIVATE_KEY, HL_WALLET_ADDRESS, HL_TESTNET)
                result["open_orders"] = executor.get_open_orders()
            except Exception as e2:
                print(f"  Error getting open orders: {e2}")
        print(f"  Open orders: {len(result['open_orders'])}")
    except Exception as e:
        print(f"  Error getting position/balance: {e}")
    
    # 5. Read market data
    print("Reading market data...")
    result["market_data"] = load_json_file(ARENA_DIR / "market-live.json", {})
    if not result["market_data"]:
        result["market_data"] = load_json_file(ARENA_DIR / "market-data-hourly.json", {})
    print(f"  Market data keys: {list(result['market_data'].keys())[:5]}...")
    
    # 6. Read on-chain data
    print("Reading on-chain data...")
    result["onchain_data"] = load_json_file(ARENA_DIR / "onchain-hourly.json", {})
    print(f"  On-chain data keys: {list(result['onchain_data'].keys())[:5]}...")
    
    # 7. Read protocol data
    print("Reading protocol data...")
    result["protocol_data"] = load_json_file(ARENA_DIR / "protocol-hourly.json", {})
    print(f"  Protocol data keys: {list(result['protocol_data'].keys())[:5]}...")
    
    # 8. Read news
    print("Reading news...")
    news_data = load_json_file(ARENA_DIR / "news-summary.json", {})
    top_stories = news_data.get("top_stories", [])[:3]
    result["news"] = {
        "top_headlines": [s.get("headline", "") for s in top_stories],
        "sentiment": "bullish" if any(s.get("impact") == "bullish" for s in top_stories) else "bearish" if any(s.get("impact") == "bearish" for s in top_stories) else "neutral",
        "fear_greed": news_data.get("indices", [{}])[0].get("value", 50)
    }
    print(f"  Headlines: {result['news']['top_headlines']}")
    
    # 9. Read trade history
    print("Reading trade history...")
    trades = load_trade_history()
    result["recent_trades"] = trades[-10:] if len(trades) > 10 else trades
    print(f"  Recent trades: {len(result['recent_trades'])}")
    
    # 10. Compute streak
    result["trade_streak"] = get_trade_streak(trades)
    print(f"  Trade streak: {result['trade_streak']}")
    
    # Write trading-context.json
    output_file = DATA_DIR / "trading-context.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Written to {output_file}")
    
    # Write position-state.json (just position + balance + orders)
    position_state = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "position": result["position"],
        "balance": result["balance"],
        "open_orders": result["open_orders"],
        "eth_price": result["eth_price"]
    }
    position_file = DATA_DIR / "position-state.json"
    with open(position_file, "w") as f:
        json.dump(position_state, f, indent=2)
    print(f"Written to {position_file}")
    
    print("=== Collection Complete ===")
    return result


if __name__ == "__main__":
    main()
