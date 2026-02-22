#!/usr/bin/env python3
"""NOFX Live Market Data Collector - runs every 30 seconds as a daemon."""

import json
import urllib.request
import urllib.error
import time
import os
import sys
from datetime import datetime, timezone

OUTPUT = "/home/openclaw/.openclaw/workspace/projects/nofx-project/arena/market-live.json"
INTERVAL = 30  # seconds

def api_get(url, headers=None):
    """Simple GET request with timeout."""
    if headers is None:
        headers = {"User-Agent": "NOFX-Live/1.0"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return None

def api_post(url, data):
    """Simple POST request."""
    try:
        payload = json.dumps(data).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "NOFX-Live/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return None

def get_liquidations():
    """Get liquidation data from Binance futures."""
    result = {"long_liquidations_1h": 0, "short_liquidations_1h": 0, "total_1h": 0}
    try:
        data = api_get("https://fapi.binance.com/fapi/v1/forceOrders?symbol=ETHUSDT&limit=100")
        if data:
            now = int(time.time() * 1000)
            one_hour_ago = now - 3600000
            for order in data:
                if order.get("time", 0) < one_hour_ago:
                    continue
                qty = float(order.get("origQty", 0))
                price = float(order.get("price", 0))
                usd_val = qty * price
                if order.get("side") == "SELL":
                    result["long_liquidations_1h"] += usd_val
                else:
                    result["short_liquidations_1h"] += usd_val
            result["total_1h"] = round(result["long_liquidations_1h"] + result["short_liquidations_1h"], 2)
            result["long_liquidations_1h"] = round(result["long_liquidations_1h"], 2)
            result["short_liquidations_1h"] = round(result["short_liquidations_1h"], 2)
    except:
        pass
    return result

def get_options_data():
    """Get ETH options data from Deribit."""
    result = {"put_call_ratio": 0, "total_put_oi": 0, "total_call_oi": 0, "signal": "neutral", "avg_iv": 0}
    try:
        data = api_get("https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency=ETH&kind=option")
        if data and data.get("result"):
            put_oi = call_oi = total_iv = iv_count = 0
            for opt in data["result"]:
                name = opt.get("instrument_name", "")
                oi = float(opt.get("open_interest", 0))
                iv = float(opt.get("mark_iv", 0))
                if "-P" in name:
                    put_oi += oi
                elif "-C" in name:
                    call_oi += oi
                if iv > 0:
                    total_iv += iv
                    iv_count += 1
            
            result["total_put_oi"] = round(put_oi, 2)
            result["total_call_oi"] = round(call_oi, 2)
            if call_oi > 0:
                result["put_call_ratio"] = round(put_oi / call_oi, 3)
            if iv_count > 0:
                result["avg_iv"] = round(total_iv / iv_count, 2)
            
            pc = result["put_call_ratio"]
            if pc > 1.0:
                result["signal"] = "bearish_hedge"
            elif pc < 0.6:
                result["signal"] = "bullish_positioning"
    except:
        pass
    return result

def get_btc_eth_prices():
    """Get BTC and ETH prices for correlation."""
    result = {"btc_price": 0, "eth_price": 0, "ratio": 0, "correlation": "balanced"}
    try:
        btc = api_get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        eth = api_get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
        if btc and eth:
            btc_price = float(btc.get("price", 0))
            eth_price = float(eth.get("price", 0))
            result["btc_price"] = btc_price
            result["eth_price"] = eth_price
            if eth_price > 0:
                result["ratio"] = round(btc_price / eth_price, 4)
                if result["ratio"] > 20:
                    result["correlation"] = "btc_leading"
                elif result["ratio"] < 12:
                    result["correlation"] = "eth_leading"
    except:
        pass
    return result

def get_dex_volume():
    """Get DEX volume from DeFiLlama."""
    result = {"dex_volume_24h": 0}
    try:
        data = api_get("https://api.llama.fi/overview/dexs/ethereum")
        if data and isinstance(data, list) and len(data) > 0:
            result["dex_volume_24h"] = data[0].get("volume24h", 0)
    except:
        pass
    return result

def get_stablecoin_mcaps():
    """Get stablecoin market caps."""
    result = {"usdt_market_cap": 0, "usdc_market_cap": 0, "total": 0}
    try:
        data = api_get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=tether,usd-coin&order=market_cap_desc&sparkline=false")
        if data and isinstance(data, list):
            for coin in data:
                symbol = coin.get("symbol", "").lower()
                mc = coin.get("market_cap", 0)
                if symbol == "usdt":
                    result["usdt_market_cap"] = mc
                elif symbol == "usd-coin":
                    result["usdc_market_cap"] = mc
            result["total"] = result["usdt_market_cap"] + result["usdc_market_cap"]
    except:
        pass
    return result

def get_fear_greed():
    """Get Fear & Greed index."""
    result = {"value": 50, "label": "Neutral"}
    try:
        data = api_get("https://api.alternative.me/fng/")
        if data and data.get("data"):
            d = data["data"][0]
            result["value"] = int(d.get("value", 50))
            result["label"] = d.get("value_classification", "Neutral")
    except:
        pass
    return result

def collect():
    """Collect all data once."""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "liquidations": get_liquidations(),
        "options": get_options_data(),
        "btc_eth": get_btc_eth_prices(),
        "dex_volume": get_dex_volume(),
        "stablecoins": get_stablecoin_mcaps(),
        "fear_greed": get_fear_greed(),
    }

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting live collector (every {INTERVAL}s)...")
    
    while True:
        try:
            result = collect()
            with open(OUTPUT, "w") as f:
                json.dump(result, f, indent=2)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Wrote live data: PC={result['options']['put_call_ratio']}, liq=${result['liquidations']['total_1h']:,.0f}")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
        
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
