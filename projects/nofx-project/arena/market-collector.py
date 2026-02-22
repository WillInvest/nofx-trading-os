#!/usr/bin/env python3
"""NOFX Market Data Collector - gathers free data from Hyperliquid, Binance, Deribit, and alternative.me"""

import json
import urllib.request
import urllib.error
import time
from datetime import datetime, timezone, timedelta

COINS = ["ETH", "AAVE", "LINK", "ZRO", "ENA", "UNI", "LDO", "CRV", "PENDLE", "ARB"]
COIN_DISPLAY = {}  # no special display names needed
BINANCE_MAP = {}  # no special Binance symbol overrides
OUTPUT = "/home/openclaw/.openclaw/workspace/projects/nofx-project/arena/market-data-hourly.json"
TIMEOUT = 10


def api_post(url, data):
    req = urllib.request.Request(url, json.dumps(data).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read())


def api_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "NOFX-Collector/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read())


def load_previous():
    try:
        with open(OUTPUT) as f:
            return json.load(f)
    except Exception:
        return None


def get_meta_and_asset_ctxs():
    """Returns (meta, asset_ctxs) - meta has universe[], asset_ctxs has per-asset data"""
    resp = api_post("https://api.hyperliquid.xyz/info", {"type": "metaAndAssetCtxs"})
    return resp[0], resp[1]


def funding_signal(rate):
    if rate > 0.0005:
        return "longs_crowded"
    elif rate < -0.0005:
        return "shorts_crowded"
    return "neutral"


def ob_signal(imbalance):
    if imbalance > 0.2:
        return "buying_pressure"
    elif imbalance < -0.2:
        return "selling_pressure"
    return "neutral"


def oi_signal(oi_change_pct, price_prev, price_now):
    if price_prev is None or price_prev == 0:
        return "neutral"
    price_change = (price_now - price_prev) / price_prev
    if oi_change_pct > 2:
        if price_change > 0.005:
            return "trend_confirmation"
        elif price_change < -0.005:
            return "short_buildup"
    elif oi_change_pct < -2:
        if price_change < -0.005:
            return "long_unwinding"
    return "neutral"


def cvd_signal(cvd, total_vol):
    if total_vol == 0:
        return "balanced"
    ratio = abs(cvd) / total_vol
    if ratio < 0.1:
        return "balanced"
    return "buyers_dominant" if cvd > 0 else "sellers_dominant"


def main():
    prev = load_previous()
    now = datetime.now(timezone.utc)
    result = {"timestamp": now.isoformat(), "coins": {}, "macro": {}}

    # 1 & 4: Meta + asset contexts (funding rates, OI, prices)
    meta = asset_ctxs = None
    coin_index = {}
    try:
        meta, asset_ctxs = get_meta_and_asset_ctxs()
        for i, u in enumerate(meta["universe"]):
            coin_index[u["name"]] = i
    except Exception as e:
        print(f"[WARN] metaAndAssetCtxs failed: {e}")

    # Init coin data
    for coin in COINS:
        dk = COIN_DISPLAY.get(coin, coin)  # display key
        result["coins"][dk] = {}
        if meta and coin in coin_index:
            ctx = asset_ctxs[coin_index[coin]]
            fr = float(ctx.get("funding", 0))
            price = float(ctx.get("markPx", 0))
            oi_raw = float(ctx.get("openInterest", 0))
            oi_usd = oi_raw * price

            # OI velocity
            prev_oi = None
            prev_price = None
            oi_change = 0
            if prev and dk in prev.get("coins", {}):
                prev_oi = prev["coins"][dk].get("oi_usd")
                prev_price = prev["coins"][dk].get("price")
                if prev_oi and prev_oi > 0:
                    oi_change = ((oi_usd - prev_oi) / prev_oi) * 100

            result["coins"][dk].update({
                "funding_rate": fr,
                "funding_signal": funding_signal(fr),
                "price": price,
                "oi_usd": round(oi_usd, 2),
                "oi_change_pct": round(oi_change, 2),
                "oi_signal": oi_signal(oi_change, prev_price, price),
            })

    # 2: Orderbook depth
    for coin in COINS:
        dk = COIN_DISPLAY.get(coin, coin)
        try:
            book = api_post("https://api.hyperliquid.xyz/info", {"type": "l2Book", "coin": coin})
            levels = book.get("levels", [[], []])
            bids = sum(float(l["sz"]) * float(l["px"]) for l in levels[0][:10])
            asks = sum(float(l["sz"]) * float(l["px"]) for l in levels[1][:10])
            total = bids + asks
            imbalance = (bids - asks) / total if total > 0 else 0
            result["coins"][dk]["orderbook_imbalance"] = round(imbalance, 4)
            result["coins"][dk]["orderbook_signal"] = ob_signal(imbalance)
        except Exception as e:
            print(f"[WARN] L2 book {coin}: {e}")
            result["coins"][dk]["orderbook_imbalance"] = 0
            result["coins"][dk]["orderbook_signal"] = "neutral"

    # 3: Liquidations (Binance)
    one_hour_ago = int((now - timedelta(hours=1)).timestamp() * 1000)
    for coin in COINS:
        dk = COIN_DISPLAY.get(coin, coin)
        sym = BINANCE_MAP.get(coin, coin + "USDT")
        liq = {"long_count": 0, "short_count": 0, "long_usd": 0, "short_usd": 0}
        try:
            data = api_get(f"https://fapi.binance.com/fapi/v1/forceOrders?symbol={sym}&limit=100")
            for o in data:
                if o.get("time", 0) < one_hour_ago:
                    continue
                usd = float(o.get("origQty", 0)) * float(o.get("price", 0))
                if o.get("side") == "SELL":  # long liquidated
                    liq["long_count"] += 1
                    liq["long_usd"] += usd
                else:
                    liq["short_count"] += 1
                    liq["short_usd"] += usd
            liq["long_usd"] = round(liq["long_usd"], 2)
            liq["short_usd"] = round(liq["short_usd"], 2)
        except Exception as e:
            print(f"[WARN] Liquidations {sym}: {e}")
        result["coins"][dk]["liquidations_1h"] = liq

    # 5: CVD from recent trades
    for coin in COINS:
        dk = COIN_DISPLAY.get(coin, coin)
        try:
            trades = api_post("https://api.hyperliquid.xyz/info", {"type": "recentTrades", "coin": coin})
            buy_vol = sell_vol = 0
            for t in trades:
                vol = float(t.get("sz", 0)) * float(t.get("px", 0))
                if t.get("side") == "B":
                    buy_vol += vol
                else:
                    sell_vol += vol
            cvd = buy_vol - sell_vol
            total = buy_vol + sell_vol
            result["coins"][dk]["cvd"] = round(cvd, 2)
            result["coins"][dk]["cvd_signal"] = cvd_signal(cvd, total)
        except Exception as e:
            print(f"[WARN] CVD {coin}: {e}")
            result["coins"][dk]["cvd"] = 0
            result["coins"][dk]["cvd_signal"] = "balanced"

    # 6: Fear & Greed
    try:
        fg = api_get("https://api.alternative.me/fng/")
        d = fg["data"][0]
        result["macro"]["fear_greed"] = {"value": int(d["value"]), "label": d["value_classification"]}
    except Exception as e:
        print(f"[WARN] Fear & Greed: {e}")
        result["macro"]["fear_greed"] = {"value": 0, "label": "unknown"}

    # 7: Deribit options (ETH)
    try:
        opts = api_get("https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency=ETH&kind=option")
        put_oi = call_oi = 0
        for o in opts.get("result", []):
            name = o.get("instrument_name", "")
            oi = o.get("open_interest", 0)
            if "-P" in name:
                put_oi += oi
            elif "-C" in name:
                call_oi += oi
        pc_ratio = put_oi / call_oi if call_oi > 0 else 0
        if pc_ratio > 1.0:
            sig = "bearish_hedge"
        elif pc_ratio < 0.6:
            sig = "bullish_positioning"
        else:
            sig = "neutral"
        result["macro"]["eth_options"] = {
            "put_call_ratio": round(pc_ratio, 3),
            "total_put_oi": round(put_oi, 2),
            "total_call_oi": round(call_oi, 2),
            "signal": sig,
        }
    except Exception as e:
        print(f"[WARN] Deribit options: {e}")
        result["macro"]["eth_options"] = {"put_call_ratio": 0, "signal": "unknown"}

    # Deribit BTC options
    try:
        opts = api_get("https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency=BTC&kind=option")
        put_oi = call_oi = 0
        for o in opts.get("result", []):
            name = o.get("instrument_name", "")
            oi = o.get("open_interest", 0)
            if "-P" in name:
                put_oi += oi
            elif "-C" in name:
                call_oi += oi
        pc_ratio = put_oi / call_oi if call_oi > 0 else 0
        if pc_ratio > 1.0:
            sig = "bearish_hedge"
        elif pc_ratio < 0.6:
            sig = "bullish_positioning"
        else:
            sig = "neutral"
        result["macro"]["btc_options"] = {
            "put_call_ratio": round(pc_ratio, 3),
            "total_put_oi": round(put_oi, 2),
            "total_call_oi": round(call_oi, 2),
            "signal": sig,
        }
    except Exception as e:
        print(f"[WARN] Deribit BTC options: {e}")

    # Write output
    with open(OUTPUT, "w") as f:
        json.dump(result, f, indent=2)
    print(f"[OK] Written to {OUTPUT}")
    print(json.dumps(result, indent=2)[:3000])


if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"\n[TIME] {time.time() - t0:.1f}s")
