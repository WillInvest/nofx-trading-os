#!/bin/bash
# collect-eth.sh — Collect all ETH-relevant data for Opus decision
# Runs existing collectors + any evolving data requests
set -euo pipefail

ARENA_DIR="$(cd "$(dirname "$0")" && pwd)"
NOFX_DIR="/home/openclaw/.openclaw/workspace/projects/nofx-project/nofx"
OUTPUT_DIR="$NOFX_DIR/data/arena"
ETH_NODE="hfu11@10.246.103.160"

echo "[$(date '+%H:%M:%S')] === ETH Data Collection Start ==="

# ─── 1. On-chain data from ETH node (~43s) ───
echo "[$(date '+%H:%M:%S')] Collecting on-chain data..."
ssh -o ConnectTimeout=10 "$ETH_NODE" "cd /srv/ethnode && python3 bin/onchain-collector.py" 2>/dev/null
scp -q "$ETH_NODE:/srv/ethnode/output/onchain-hourly.json" "$ARENA_DIR/onchain-hourly.json" 2>/dev/null || echo "  ⚠️ On-chain collection failed"

# ─── 2. Protocol-specific data from ETH node (~10s) ───
echo "[$(date '+%H:%M:%S')] Collecting protocol data..."
ssh -o ConnectTimeout=10 "$ETH_NODE" "cd /srv/ethnode && python3 bin/protocol-collector.py" 2>/dev/null
scp -q "$ETH_NODE:/srv/ethnode/output/protocol-hourly.json" "$ARENA_DIR/protocol-hourly.json" 2>/dev/null || echo "  ⚠️ Protocol collection failed"

# ─── 3. Market data from free APIs (~5s) ───
echo "[$(date '+%H:%M:%S')] Collecting market data..."
python3 "$ARENA_DIR/market-collector.py" 2>/dev/null || echo "  ⚠️ Market collection failed"

# ─── 4. Evolving data requests (if any) ───
REQUESTS_FILE="$OUTPUT_DIR/data-requests.json"
if [ -f "$REQUESTS_FILE" ]; then
    echo "[$(date '+%H:%M:%S')] Processing evolving data requests..."
    python3 -c "
import json, subprocess, os

with open('$REQUESTS_FILE') as f:
    requests = json.load(f)

results = {}
for req in requests.get('requests', []):
    name = req.get('name', 'unknown')
    cmd = req.get('command', '')
    if cmd:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            results[name] = result.stdout.strip()
            print(f'  ✅ {name}')
        except Exception as e:
            results[name] = f'ERROR: {e}'
            print(f'  ❌ {name}: {e}')

# Save extra data
with open('$OUTPUT_DIR/extra-data.json', 'w') as f:
    json.dump(results, f, indent=2)
" 2>/dev/null || true
fi

# ─── 5. Merge all data into single brief ───
echo "[$(date '+%H:%M:%S')] Merging data..."
python3 -c "
import json, os
from datetime import datetime

brief = {
    'timestamp': datetime.now().isoformat(),
    'symbol': 'ETH',
    'data_sources': {}
}

files = {
    'onchain': '$ARENA_DIR/onchain-hourly.json',
    'protocol': '$ARENA_DIR/protocol-hourly.json',
    'market': '$ARENA_DIR/market-data-hourly.json',
    'extra': '$OUTPUT_DIR/extra-data.json',
}

for name, path in files.items():
    if os.path.exists(path):
        try:
            with open(path) as f:
                brief['data_sources'][name] = json.load(f)
            print(f'  ✅ {name}')
        except:
            print(f'  ⚠️ {name} (parse error)')
    else:
        print(f'  ⚠️ {name} (not found)')

with open('$OUTPUT_DIR/eth-brief.json', 'w') as f:
    json.dump(brief, f, indent=2)

# Calculate size
size = os.path.getsize('$OUTPUT_DIR/eth-brief.json')
print(f'\n  📊 ETH brief: {size:,} bytes')
" 2>/dev/null

echo "[$(date '+%H:%M:%S')] === ETH Data Collection Complete ==="
