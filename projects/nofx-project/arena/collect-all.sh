#!/bin/bash
# collect-all.sh — Runs all data collectors and merges results
# Called hourly before debate scan
set -euo pipefail

ARENA_DIR="$(cd "$(dirname "$0")" && pwd)"
ETH_NODE="hfu11@10.246.103.160"
REMOTE_OUTPUT="/srv/ethnode/output"
LOCAL_DATA="$ARENA_DIR"
LOG_EVENT="$ARENA_DIR/log-event.sh"

# Helper to log events
log_agent_event() {
    local type="$1"
    local model="$2"
    local message="$3"
    local task="${4:-data-collection}"
    local tokens_in="${5:-0}"
    local tokens_out="${6:-0}"
    local cost="${7:-0}"
    local duration="${8:-0}"

    if [ -x "$LOG_EVENT" ]; then
        "$LOG_EVENT" "$type" "$model" "$message" "$task" "$tokens_in" "$tokens_out" "$cost" "$duration" 2>/dev/null || true
    fi
}

echo "[$(date '+%H:%M:%S')] Starting data collection..."

# Log start of data collection
log_agent_event "dispatch" "Opus 4.6" "Starting hourly data collection" "hourly-data-collection"

START_TIME=$(date +%s)

# 1. Run ETH node collectors (remote)
echo "[$(date '+%H:%M:%S')] Running on-chain collector..."
ONCHAIN_START=$(date +%s)
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$ETH_NODE" \
  "python3 /srv/ethnode/bin/onchain-collector.py" 2>&1 | tail -3 || echo "WARN: on-chain collector failed"
ONCHAIN_END=$(date +%s)
ONCHAIN_DURATION=$((ONCHAIN_END - ONCHAIN_START))
log_agent_event "result" "MiniMax M2.5" "On-chain collector done" "onchain-collector" 0 0 0 "$ONCHAIN_DURATION"

echo "[$(date '+%H:%M:%S')] Running protocol collector..."
PROTOCOL_START=$(date +%s)
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$ETH_NODE" \
  "python3 /srv/ethnode/bin/protocol-collector.py" 2>&1 | tail -3 || echo "WARN: protocol collector failed"
PROTOCOL_END=$(date +%s)
PROTOCOL_DURATION=$((PROTOCOL_END - PROTOCOL_START))
log_agent_event "result" "MiniMax M2.5" "Protocol collector done" "protocol-collector" 0 0 0 "$PROTOCOL_DURATION"

# 2. SCP results back
echo "[$(date '+%H:%M:%S')] Fetching remote data..."
scp -o ConnectTimeout=10 -q "$ETH_NODE:$REMOTE_OUTPUT/onchain-hourly.json" "$LOCAL_DATA/onchain-hourly.json" 2>/dev/null || echo "WARN: failed to fetch onchain-hourly.json"
scp -o ConnectTimeout=10 -q "$ETH_NODE:$REMOTE_OUTPUT/protocol-hourly.json" "$LOCAL_DATA/protocol-hourly.json" 2>/dev/null || echo "WARN: failed to fetch protocol-hourly.json"

# 3. Run local market collector
echo "[$(date '+%H:%M:%S')] Running market collector..."
MARKET_START=$(date +%s)
python3 "$ARENA_DIR/market-collector.py" 2>&1 | tail -3 || echo "WARN: market collector failed"
MARKET_END=$(date +%s)
MARKET_DURATION=$((MARKET_END - MARKET_START))
log_agent_event "result" "MiniMax M2.5" "Market collector done" "market-collector" 0 0 0 "$MARKET_DURATION"

# 4. Merge all data
echo "[$(date '+%H:%M:%S')] Merging data..."
python3 "$ARENA_DIR/merge-data.py" 2>&1 || echo "WARN: merge failed"

# 5. Copy to Docker data volume so backend container can read it
DOCKER_DATA="$(dirname "$ARENA_DIR")/nofx/data/arena"
mkdir -p "$DOCKER_DATA"
cp "$ARENA_DIR/debate-context.json" "$DOCKER_DATA/debate-context.json" 2>/dev/null || echo "WARN: failed to copy to docker data"

END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))

# Log completion
log_agent_event "result" "Opus 4.6" "All data collected and merged" "hourly-data-collection" 0 0 0 "$TOTAL_DURATION"

echo "[$(date '+%H:%M:%S')] Data collection complete."
echo ""
echo "Debate framework: Strategy-based (grid/funding/mean_reversion/directional/breakout)"
echo "Rule: NO plain waiting. Always pick an active strategy."
