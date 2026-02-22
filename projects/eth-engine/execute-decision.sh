#!/bin/bash
# Execute Decision Script
# Runs AFTER MiniMax brain writes decision.json
# This script:
# 1. Converts decision to NOFX format
# 2. Copies files to arena and Docker
# 3. Waits for execution
# 4. Saves results to cycle directory
# 5. Updates cycles-history.json

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
ARENA_DIR="/home/openclaw/.openclaw/workspace/projects/nofx-project/nofx/data/arena"
DOCKER_CONTAINER="nofx-trading"
DOCKER_ARENA_DIR="/app/data/arena"
LOG_FILE="$DATA_DIR/cron.log"

# JWT Config for NOFX API
USER_ID="34dd0d3b-bf61-4a6a-82fc-0f0af42355c1"
JWT_SECRET="Fm9Dd/bc2ix30BkhbC22lKy2m/0CDjedaX/TAwkQMGc="
NOFX_API="http://localhost:8090"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

# Generate JWT token for NOFX API
generate_jwt() {
    python3 -c "
import jwt, time
token = jwt.encode({'user_id': '$USER_ID', 'exp': int(time.time()) + 3600}, '$JWT_SECRET', algorithm='HS256')
print(token)
"
}

log "=== Execute Decision Start ==="

# Find the most recent cycle directory
CYCLE_DIR=$(ls -td "$DATA_DIR"/cycle-* 2>/dev/null | head -1)
if [ -z "$CYCLE_DIR" ]; then
    log "ERROR: No cycle directory found"
    exit 1
fi

CYCLE_ID=$(basename "$CYCLE_DIR" | sed 's/cycle-//')
log "Using cycle: $CYCLE_ID"

# Check if decision.json exists
if [ ! -f "$DATA_DIR/decision.json" ]; then
    log "ERROR: decision.json not found"
    exit 1
fi

# Step 1: Convert decision to NOFX format
log "Step 1: Converting decision to NOFX format..."
cd "$SCRIPT_DIR"
python3 push-to-nofx.py 2>&1 | tee -a "$LOG_FILE"

if [ $? -ne 0 ]; then
    log "ERROR: push-to-nofx.py failed"
    exit 1
fi

# Step 2: Copy files to arena directory
log "Step 2: Copying files to arena..."
if [ -f "$ARENA_DIR/hourly-plan.json" ]; then
    cp "$ARENA_DIR/hourly-plan.json" "$CYCLE_DIR/trading-plan.json"
    log "Saved hourly-plan.json to cycle directory"
else
    log "WARNING: hourly-plan.json not found in arena"
fi

if [ -f "$ARENA_DIR/hourly-instruction.md" ]; then
    cp "$ARENA_DIR/hourly-instruction.md" "$CYCLE_DIR/"
    log "Saved hourly-instruction.md to cycle directory"
else
    log "WARNING: hourly-instruction.md not found in arena"
fi

# Step 3: Copy files to Docker container
log "Step 3: Copying files to Docker container..."
if docker ps | grep -q "$DOCKER_CONTAINER"; then
    docker cp "$ARENA_DIR/hourly-plan.json" "$DOCKER_CONTAINER:$DOCKER_ARENA_DIR/hourly-plan.json" 2>&1 | tee -a "$LOG_FILE" || true
    docker cp "$ARENA_DIR/hourly-instruction.md" "$DOCKER_CONTAINER:$DOCKER_ARENA_DIR/hourly-instruction.md" 2>&1 | tee -a "$LOG_FILE" || true
    log "Files copied to Docker container"
else
    log "WARNING: Docker container $DOCKER_CONTAINER not running"
fi

# Step 4: Wait for execution
log "Step 4: Waiting 10 seconds for execution..."
sleep 10

# Step 5: Get execution result
log "Step 5: Checking execution result..."
JWT_TOKEN=$(generate_jwt)

# Get position state BEFORE (from cycle directory)
POSITION_BEFORE=$(cat "$CYCLE_DIR/position-state.json" 2>/dev/null || echo '{}')

# Get current position state AFTER execution
POSITION_AFTER=$(curl -s -X GET "$NOFX_API/api/traders" \
    -H "Authorization: Bearer $JWT_TOKEN" \
    -H "Content-Type: application/json" 2>/dev/null || echo '{"error": "API not available"}')

echo "$POSITION_AFTER" > "$CYCLE_DIR/execution-result.json"

# Extract position info for summary
POSITION_SIZE=$(echo "$POSITION_AFTER" | python3 -c "
import json, sys
data = json.load(sys.stdin)
positions = data.get('positions', [])
for p in positions:
    if p.get('coin') == 'ETH':
        print(p.get('size', 0))
        sys.exit(0)
print('0')
" 2>/dev/null || echo "0")

ENTRY_PRICE=$(echo "$POSITION_AFTER" | python3 -c "
import json, sys
data = json.load(sys.stdin)
positions = data.get('positions', [])
for p in positions:
    if p.get('coin') == 'ETH':
        print(p.get('entry_price', 0))
        sys.exit(0)
print('0')
" 2>/dev/null || echo "0")

UNREALIZED_PNL=$(echo "$POSITION_AFTER" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('unrealized_pnl', 0))
" 2>/dev/null || echo "0")

BALANCE=$(echo "$POSITION_AFTER" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('balance', data.get('available_balance', 0)))
" 2>/dev/null || echo "0")

# Step 6: Read decision for summary
log "Step 6: Building cycle summary..."
DECISION=$(cat "$DATA_DIR/decision.json")
STRATEGY=$(echo "$DECISION" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('strategy','hold'))" 2>/dev/null || echo "unknown")
DIRECTION=$(echo "$DECISION" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('direction','neutral'))" 2>/dev/null || echo "unknown")
CONFIDENCE=$(echo "$DECISION" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('confidence',0))" 2>/dev/null || echo "0")
ENTRY_PRICE_DEC=$(echo "$DECISION" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('entry_price', 0))" 2>/dev/null || echo "0")

# Get ETH price from trading context
ETH_PRICE=$(python3 -c "
import json
with open('$DATA_DIR/trading-context.json') as f:
    data = json.load(f)
print(data.get('eth_price', 0))
" 2>/dev/null || echo "0")

if [ "$ENTRY_PRICE_DEC" = "None" ] || [ -z "$ENTRY_PRICE_DEC" ]; then
    ETH_PRICE_DISPLAY=$ETH_PRICE
else
    ETH_PRICE_DISPLAY=$ENTRY_PRICE_DEC
fi

# Determine decision string
if [ "$STRATEGY" = "close_all" ]; then
    DECISION_STR="close"
elif [ "$DIRECTION" = "long" ]; then
    DECISION_STR="open_long"
elif [ "$DIRECTION" = "short" ]; then
    DECISION_STR="open_short"
else
    DECISION_STR="hold"
fi

# Determine status
if echo "$POSITION_AFTER" | grep -q '"error"'; then
    STATUS="failed"
    ERROR=$(echo "$POSITION_AFTER" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('error','Unknown error'))" 2>/dev/null || echo "API error")
else
    STATUS="executed"
    ERROR="null"
fi

# Step 7: Write cycle-summary.json
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

cat > "$CYCLE_DIR/cycle-summary.json" << EOF
{
  "cycle_id": "$CYCLE_ID",
  "timestamp": "$TIMESTAMP",
  "status": "$STATUS",
  "eth_price": $ETH_PRICE_DISPLAY,
  "decision": "$DECISION_STR",
  "confidence": $CONFIDENCE,
  "position_after": {
    "size": $POSITION_SIZE,
    "entry": $ENTRY_PRICE,
    "pnl": $UNREALIZED_PNL
  },
  "balance": $BALANCE,
  "error": $ERROR
}
EOF

log "Cycle summary written to $CYCLE_DIR/cycle-summary.json"

# Step 8: Copy analysis (decision.json) to cycle directory
cp "$DATA_DIR/decision.json" "$CYCLE_DIR/analysis.json"
log "Analysis saved to cycle directory"

# Step 9: Append to cycles-history.json
log "Step 9: Updating cycles-history.json..."
HISTORY_FILE="$DATA_DIR/cycles-history.json"

# Create history file if it doesn't exist
if [ ! -f "$HISTORY_FILE" ]; then
    echo "[]" > "$HISTORY_FILE"
fi

# Read existing history, add new entry, keep last 100
python3 -c "
import json

history_file = '$HISTORY_FILE'
summary_file = '$CYCLE_DIR/cycle-summary.json'

# Read existing history
try:
    with open(history_file) as f:
        history = json.load(f)
except:
    history = []

# Read new summary
with open(summary_file) as f:
    new_entry = json.load(f)

# Add to history
history.append(new_entry)

# Keep last 100
history = history[-100:]

# Write back
with open(history_file, 'w') as f:
    json.dump(history, f, indent=2)

print(f'History now has {len(history)} entries')
"

log "=== Execution Complete ==="
log "Status: $STATUS"
log "Position size: $POSITION_SIZE at \$$ENTRY_PRICE"
log "Unrealized PnL: \$$UNREALIZED_PNL"
log "Balance: \$$BALANCE"

# Show summary
echo ""
echo "=== CYCLE SUMMARY ==="
cat "$CYCLE_DIR/cycle-summary.json"
echo ""
echo "====================="
