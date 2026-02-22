#!/usr/bin/env python3
"""Merge all data sources into debate-context.json for the frontend."""

import json
import os
from datetime import datetime, timezone

ARENA_DIR = "/home/openclaw/.openclaw/workspace/projects/nofx-project/arena"
OUTPUT_DIR = "/home/openclaw/.openclaw/workspace/projects/nofx-project/nofx/data/arena"

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None

def main():
    # Load all sources
    onchain = load_json(f"{ARENA_DIR}/onchain-hourly.json")
    protocol = load_json(f"{ARENA_DIR}/protocol-hourly.json")
    market_hourly = load_json(f"{ARENA_DIR}/market-data-hourly.json")
    market_live = load_json(f"{ARENA_DIR}/market-live.json")
    profiles = load_json(f"{ARENA_DIR}/coin-profiles.json")
    
    # New live collectors from ETH node
    mempool = load_json(f"{ARENA_DIR}/mempool-live.json")
    whale = load_json(f"{ARENA_DIR}/whale-live.json")
    dex_trades = load_json(f"{ARENA_DIR}/dex-trades-live.json")
    liquidations = load_json(f"{ARENA_DIR}/liquidation-live.json")
    
    COINS = ["ETH", "AAVE", "LINK", "ZRO", "ENA", "UNI", "LDO", "CRV", "PENDLE", "ARB"]
    
    # Build shared intelligence
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
        shared["lido"] = protocol.get("lido", {})
        shared["eip1559_burn"] = protocol.get("eip1559_burn", {})
        shared["dex_volume"] = protocol.get("dex_volume", {})
    
    # Merge market data (hourly + live)
    if market_hourly:
        shared["fear_greed"] = market_hourly.get("macro", {}).get("fear_greed", {})
        shared["options"] = market_hourly.get("macro", {}).get("eth_options", {})
        shared["btc_options"] = market_hourly.get("macro", {}).get("btc_options", {})
    
    # Add live market data
    if market_live:
        shared["live_options"] = market_live.get("options", {})
        shared["live_liquidations"] = market_live.get("liquidations", {})
        shared["live_btc_eth"] = market_live.get("btc_eth", {})
        shared["live_dex_volume"] = market_live.get("dex_volume", {})
        shared["live_stablecoins"] = market_live.get("stablecoins", {})
        # Override fear_greed with live if available
        if market_live.get("fear_greed"):
            shared["fear_greed"] = market_live.get("fear_greed", {})
    
    # Add new live collectors from ETH node
    if mempool:
        shared["mempool"] = {
            "pending_count": mempool.get("pending_count", 0),
            "large_txs_count": len(mempool.get("large_txs", [])),
            "avg_gas_gwei": mempool.get("avg_gas_price_gwei", 0),
            "gas_distribution": mempool.get("gas_price_distribution", {})
        }
    
    if whale:
        shared["whale_activity"] = {
            "whale_count": whale.get("whale_count", 0),
            "whale_volume_eth": whale.get("whale_volume_eth", 0),
            "net_exchange_flow": whale.get("net_exchange_flow", 0),
            "exchange_flows": whale.get("exchange_flows", {}),
            "top_txs": whale.get("top_5_txs", [])
        }
    
    if dex_trades:
        shared["dex_large_trades"] = {
            "total_swaps": dex_trades.get("total_swaps", 0),
            "large_swap_count": dex_trades.get("large_swap_count", 0),
            "volume_eth": dex_trades.get("swap_volume_eth", 0),
            "net_buy_sell_eth": dex_trades.get("net_buy_sell_eth", 0),
            "large_swaps": dex_trades.get("large_swaps", [])
        }
    
    if liquidations:
        shared["liquidations_onchain"] = {
            "liquidation_count": liquidations.get("liquidation_count", 0),
            "total_debt_usd": liquidations.get("total_debt_usd", 0),
            "liquidations": liquidations.get("liquidations", [])
        }
    
    # Build per-coin data
    per_coin = {}
    market_coins = market_hourly.get("coins", {}) if market_hourly else {}
    
    for coin in COINS:
        coin_data = {}
        
        # Market data from hourly
        if coin in market_coins:
            mc = market_coins[coin]
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
        
        # Whale transfers
        if onchain:
            wt = onchain.get("whale_transfers", {})
            if coin in wt:
                coin_data["whale_transfers"] = wt[coin].get("large_transfers", [])[:5]
                coin_data["net_exchange_flow"] = wt[coin].get("net_exchange_flow", 0)
        
        # Profiles
        if profiles:
            pd = profiles.get("profiles", {})
            if coin in pd:
                coin_data["profile"] = pd[coin]
        
        per_coin[coin] = coin_data
    
    # Final output
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data_sources": {
            "onchain": onchain is not None,
            "protocol": protocol is not None,
            "market_hourly": market_hourly is not None,
            "market_live": market_live is not None,
            "profiles": profiles is not None,
            "mempool": mempool is not None,
            "whale": whale is not None,
            "dex_trades": dex_trades is not None,
            "liquidations": liquidations is not None
        },
        "shared_intelligence": shared,
        "per_coin": per_coin
    }
    
    # Write to output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f"{OUTPUT_DIR}/debate-context.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Merged -> {output_path}")
    print(f"Sources: onchain={'✓' if onchain else '✗'} protocol={'✓' if protocol else '✗'} market_hourly={'✓' if market_hourly else '✗'} market_live={'✓' if market_live else '✗'} mempool={'✓' if mempool else '✗'} whale={'✓' if whale else '✗'} dex={'✓' if dex_trades else '✗'} liq={'✓' if liquidations else '✗'}")

    # Also copy raw source files to Docker data dir for trading-cron.sh
    import shutil
    for f in ["onchain-hourly.json", "protocol-hourly.json", "market-data-hourly.json", "market-live.json"]:
        src = f"{ARENA_DIR}/{f}"
        dst = f"{OUTPUT_DIR}/{f}"
        if os.path.exists(src):
            shutil.copy2(src, dst)

if __name__ == "__main__":
    main()
