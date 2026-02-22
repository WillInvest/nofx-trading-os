#!/usr/bin/env python3
"""Merge all data collector outputs into a single debate-context.json"""

import json
import os
import sys
from datetime import datetime, timezone

ARENA_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(path):
    """Load JSON file, return None if missing/invalid"""
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load {path}: {e}", file=sys.stderr)
        return None

def main():
    # Load all data sources
    onchain = load_json(os.path.join(ARENA_DIR, "onchain-hourly.json"))
    market = load_json(os.path.join(ARENA_DIR, "market-data-hourly.json"))
    protocol = load_json(os.path.join(ARENA_DIR, "protocol-hourly.json"))
    profiles = load_json(os.path.join(ARENA_DIR, "coin-profiles.json"))

    # Our 10 ETH-edge coins
    COINS = ["ETH", "AAVE", "LINK", "ZRO", "ENA", "UNI", "LDO", "CRV", "PENDLE", "ARB"]

    # Build shared intelligence section
    shared = {}
    
    if onchain:
        shared["stablecoin_exchange_flows"] = onchain.get("stablecoin_exchange_flows", {})
        shared["exchange_eth_reserves"] = onchain.get("exchange_eth_reserves", {})
        shared["gas"] = onchain.get("gas", {})
        shared["stablecoin_supply"] = onchain.get("stablecoin_supply", {})
        shared["whale_transfers_summary"] = {}
        wt = onchain.get("whale_transfers", {})
        for coin in COINS:
            if coin in wt:
                transfers = wt[coin].get("large_transfers", [])
                shared["whale_transfers_summary"][coin] = {
                    "count": len(transfers),
                    "net_exchange_flow": wt[coin].get("net_exchange_flow", 0)
                }

    if protocol:
        shared["aave"] = protocol.get("aave", {})
        shared["curve_3pool"] = protocol.get("curve_3pool", {})
        shared["uniswap"] = protocol.get("uniswap", {})
        shared["ethena"] = protocol.get("ethena", {})
        shared["arb_bridge"] = protocol.get("arb_bridge", {})
        shared["link_staking"] = protocol.get("link_staking", {})
        shared["pendle"] = protocol.get("pendle", {})
        # V2 additions
        shared["lido"] = protocol.get("lido", {})
        shared["eip1559_burn"] = protocol.get("eip1559_burn", {})
        shared["dex_volume"] = protocol.get("dex_volume", {})

    if market:
        macro = market.get("macro", {})
        shared["fear_greed"] = macro.get("fear_greed", {})
        shared["options"] = macro.get("eth_options", {})

    # Build per-coin section
    per_coin = {}
    market_coins = market.get("coins", {}) if market else {}
    profile_data = profiles.get("profiles", {}) if profiles else {}

    for coin in COINS:
        coin_data = {}
        
        # Market data (funding, orderbook, OI, CVD)
        # Legacy PEPE→kPEPE mapping (no longer needed, LDO replaced PEPE)
        market_key = coin
        if coin == "PEPE" and "PEPE" not in market_coins and "kPEPE" in market_coins:
            market_key = "kPEPE"
        
        if market_key in market_coins:
            mc = market_coins[market_key]
            coin_data["funding_rate"] = mc.get("funding_rate")
            coin_data["funding_signal"] = mc.get("funding_signal")
            coin_data["orderbook_imbalance"] = mc.get("orderbook_imbalance")
            coin_data["orderbook_signal"] = mc.get("orderbook_signal")
            coin_data["oi_usd"] = mc.get("oi_usd")
            coin_data["oi_change_pct"] = mc.get("oi_change_pct")
            coin_data["oi_signal"] = mc.get("oi_signal")
            coin_data["cvd"] = mc.get("cvd")
            coin_data["cvd_signal"] = mc.get("cvd_signal")
            coin_data["price"] = mc.get("price")
            coin_data["liquidations_1h"] = mc.get("liquidations_1h")

        # Whale transfers for this coin
        if onchain:
            wt = onchain.get("whale_transfers", {})
            if coin in wt:
                coin_data["whale_transfers"] = wt[coin].get("large_transfers", [])[:5]  # Top 5
                coin_data["net_exchange_flow"] = wt[coin].get("net_exchange_flow", 0)

        # Coin profile
        if coin in profile_data:
            coin_data["profile"] = profile_data[coin]

        per_coin[coin] = coin_data

    # Build final output
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data_sources": {
            "onchain": onchain is not None,
            "market": market is not None,
            "protocol": protocol is not None,
            "profiles": profiles is not None
        },
        "shared_intelligence": shared,
        "per_coin": per_coin
    }

    # Write output
    output_path = os.path.join(ARENA_DIR, "debate-context.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Merged data written to {output_path}")
    print(f"Sources: onchain={'✓' if onchain else '✗'} market={'✓' if market else '✗'} protocol={'✓' if protocol else '✗'} profiles={'✓' if profiles else '✗'}")
    print(f"Coins: {len(per_coin)}")

if __name__ == "__main__":
    main()
