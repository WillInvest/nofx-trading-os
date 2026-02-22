#!/bin/bash
# collect-node-live.sh — Collect live on-chain data from ETH node every 2 minutes
set -euo pipefail

ARENA_DIR="$(cd "$(dirname "$0")" && pwd)"
NOFX_DIR="/home/openclaw/.openclaw/workspace/projects/nofx-project/nofx"
OUTPUT_DIR="$NOFX_DIR/data/arena"
ETH_NODE="hfu11@10.246.103.160"

echo "[$(date '+%H:%M:%S')] === Live Node Collection Start ==="

# ─── Run live collectors on remote ───
echo "[$(date '+%H:%M:%S')] Running live collectors on remote..."
ssh -o ConnectTimeout=10 "$ETH_NODE" "cd /srv/ethnode && bash bin/collect-live.sh" 2>/dev/null || echo "  ⚠️ Remote collection failed"

# ─── Copy back the 4 new JSON files ───
echo "[$(date '+%H:%M:%S')] Copying live data..."
scp -q "$ETH_NODE:/srv/ethnode/output/mempool-live.json" "$ARENA_DIR/mempool-live.json" 2>/dev/null || echo "  ⚠️ mempool-live.json failed"
scp -q "$ETH_NODE:/srv/ethnode/output/whale-live.json" "$ARENA_DIR/whale-live.json" 2>/dev/null || echo "  ⚠️ whale-live.json failed"
scp -q "$ETH_NODE:/srv/ethnode/output/dex-trades-live.json" "$ARENA_DIR/dex-trades-live.json" 2>/dev/null || echo "  ⚠️ dex-trades-live.json failed"
scp -q "$ETH_NODE:/srv/ethnode/output/liquidation-live.json" "$ARENA_DIR/liquidation-live.json" 2>/dev/null || echo "  ⚠️ liquidation-live.json failed"

# ─── Merge all data into debate-context.json ───
echo "[$(date '+%H:%M:%S')] Merging data..."
python3 "$ARENA_DIR/merge-live.py" 2>/dev/null || echo "  ⚠️ Merge failed"

# ─── Copy to Docker data dir ───
if [ -d "$NOFX_DIR/data" ]; then
    cp "$OUTPUT_DIR/debate-context.json" "$NOFX_DIR/data/" 2>/dev/null || echo "  ⚠️ Copy to Docker data dir failed"
fi

echo "[$(date '+%H:%M:%S')] === Live Node Collection Complete ==="
