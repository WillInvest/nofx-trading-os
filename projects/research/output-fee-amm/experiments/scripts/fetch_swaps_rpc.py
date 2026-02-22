#!/usr/bin/env python3
"""
Fetch Uniswap v3 Swap events via RPC (eth_getLogs)
Target: ETH/USDC 0.3% pool, June 2024
"""

import json
import requests
import time
from pathlib import Path

# Config
POOL_ADDRESS = "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8"
SWAP_TOPIC = "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"

# June 2024 block range (approximate)
# June 1, 2024 ~= block 20000000
# June 30, 2024 ~= block 20216000
START_BLOCK = 20000000
END_BLOCK = 20216000
CHUNK_SIZE = 500  # blocks per request (public RPCs limit to 1k)

# RPC endpoints (try in order)
RPC_ENDPOINTS = [
    "https://ethereum.publicnode.com",  # Most reliable free RPC
    "https://eth.drpc.org",
    "https://1rpc.io/eth",
]

OUTPUT_FILE = Path(__file__).parent.parent / "data" / "eth_usdc_swaps_june2024.json"


def get_working_rpc():
    """Find a working RPC endpoint"""
    for rpc in RPC_ENDPOINTS:
        try:
            resp = requests.post(rpc, json={
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": [],
                "id": 1
            }, timeout=5)
            if resp.status_code == 200:
                print(f"Using RPC: {rpc}")
                return rpc
        except:
            continue
    raise Exception("No working RPC found")


def fetch_logs(rpc, from_block, to_block):
    """Fetch logs for a block range"""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getLogs",
        "params": [{
            "address": POOL_ADDRESS,
            "topics": [SWAP_TOPIC],
            "fromBlock": hex(from_block),
            "toBlock": hex(to_block)
        }],
        "id": 1
    }
    
    resp = requests.post(rpc, json=payload, timeout=30)
    result = resp.json()
    
    if "error" in result:
        raise Exception(f"RPC error: {result['error']}")
    
    return result.get("result", [])


def decode_swap_event(log):
    """Decode Swap event data"""
    # Data layout (each 32 bytes):
    # amount0 (int256), amount1 (int256), sqrtPriceX96 (uint160), liquidity (uint128), tick (int24)
    data = log["data"][2:]  # remove 0x
    
    def to_signed_int(hex_str):
        val = int(hex_str, 16)
        if val >= 2**255:
            val -= 2**256
        return val
    
    amount0 = to_signed_int(data[0:64])
    amount1 = to_signed_int(data[64:128])
    sqrt_price_x96 = int(data[128:192], 16)
    
    return {
        "block_number": int(log["blockNumber"], 16),
        "tx_hash": log["transactionHash"],
        "log_index": int(log["logIndex"], 16),
        "amount0": amount0,
        "amount1": amount1,
        "sqrtPriceX96": sqrt_price_x96
    }


def main():
    print(f"Fetching Swap events from block {START_BLOCK} to {END_BLOCK}")
    print(f"Pool: {POOL_ADDRESS}")
    
    rpc = get_working_rpc()
    
    # Create output directory
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    all_swaps = []
    current_block = START_BLOCK
    
    while current_block < END_BLOCK:
        chunk_end = min(current_block + CHUNK_SIZE, END_BLOCK)
        
        try:
            logs = fetch_logs(rpc, current_block, chunk_end)
            
            for log in logs:
                swap = decode_swap_event(log)
                all_swaps.append(swap)
            
            progress = (current_block - START_BLOCK) / (END_BLOCK - START_BLOCK) * 100
            print(f"Block {current_block}-{chunk_end}: {len(logs)} swaps (total: {len(all_swaps)}, {progress:.1f}%)")
            
            current_block = chunk_end + 1
            time.sleep(0.2)  # rate limit
            
        except Exception as e:
            print(f"Error at block {current_block}: {e}")
            print("Waiting 5s and retrying...")
            time.sleep(5)
            continue
    
    # Save results
    print(f"\nTotal swaps: {len(all_swaps)}")
    print(f"Saving to: {OUTPUT_FILE}")
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump({
            "pool": POOL_ADDRESS,
            "start_block": START_BLOCK,
            "end_block": END_BLOCK,
            "swap_count": len(all_swaps),
            "swaps": all_swaps
        }, f, indent=2)
    
    print("Done!")


if __name__ == "__main__":
    main()
