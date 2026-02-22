#!/bin/bash
# hourly-cron.sh — Collect data, run debates, produce Opus decision brief
# Called by OpenClaw cron every hour 9am-11pm EST
set -euo pipefail

ARENA_DIR="$(cd "$(dirname "$0")" && pwd)"
NOFX_DIR="/home/openclaw/.openclaw/workspace/projects/nofx-project/nofx"
NOFX_API="http://localhost:8090/api"
JWT_SECRET="Fm9Dd/bc2ix30BkhbC22lKy2m/0CDjedaX/TAwkQMGc="
USER_ID="34dd0d3b-bf61-4a6a-82fc-0f0af42355c1"
TRADER_ID="f4f5f8d1_34dd0d3b-bf61-4a6a-82fc-0f0af42355c1_deepseek_1771480382"

TOKEN=$(python3 -c "
import jwt, time
print(jwt.encode({'user_id': '$USER_ID', 'exp': int(time.time()) + 3600}, '$JWT_SECRET', algorithm='HS256'))
")

STRATEGY_ID=$(curl -s "$NOFX_API/strategies/active" -H "Authorization: Bearer $TOKEN" 2>/dev/null | python3 -c "import json,sys;print(json.load(sys.stdin).get('id','2f9008bb-cfa1-44ad-bbb2-ef0e08104181'))" 2>/dev/null || echo "2f9008bb-cfa1-44ad-bbb2-ef0e08104181")

echo "[$(date '+%H:%M:%S')] === Hourly Pipeline Start ==="

# ─── Step 1: Collect fresh data (~20s) ───
echo "[$(date '+%H:%M:%S')] Step 1: Collecting data..."
bash "$ARENA_DIR/collect-all.sh" 2>&1

# ─── Step 2: Parallel debate scan (~7 min) ───
echo ""
echo "[$(date '+%H:%M:%S')] Step 2: Triggering parallel debate scan (10 coins, ~7 min)..."
SCAN_START=$(date +%s)

RESPONSE=$(curl -s --max-time 600 -X POST "$NOFX_API/debates/scan-parallel" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"strategy_id\": \"$STRATEGY_ID\", \"trader_id\": \"$TRADER_ID\"}")

SCAN_END=$(date +%s)
SCAN_DURATION=$((SCAN_END - SCAN_START))
echo "[$(date '+%H:%M:%S')] Debate scan completed in ${SCAN_DURATION}s"

# ─── Step 3: Build Opus decision brief ───
echo ""
echo "[$(date '+%H:%M:%S')] Step 3: Building decision brief for Opus..."

# Extract R1 syntheses + verdicts from scan response
python3 -c "
import json, sys, os
from datetime import datetime

try:
    response = json.loads('''$RESPONSE''')
except:
    # Response might have quotes — read from stdin alternative
    response = {}

coins = response.get('coins', [])
if not coins:
    print('ERROR: No coin results from debate scan')
    sys.exit(1)

print(f'Coins debated: {len(coins)}')

# Read current trading plan
plan_path = '$NOFX_DIR/data/arena/hourly-plan.json'
current_plan = {}
try:
    with open(plan_path) as f:
        current_plan = json.load(f)
except:
    pass

# Build the brief
brief = {
    'timestamp': datetime.now().isoformat(),
    'scan_duration_s': $SCAN_DURATION,
    'coin_count': len(coins),
    'coins': [],
    'current_plan': current_plan,
}

for c in coins:
    symbol = c.get('symbol', '?')
    r1 = c.get('r1_synthesis', '')
    error = c.get('error', '')
    price = c.get('market_price', 0)
    
    coin_data = {
        'symbol': symbol,
        'market_price': price,
        'error': error,
        'r1_synthesis': r1,
    }
    brief['coins'].append(coin_data)
    
    if error:
        print(f'  ❌ {symbol}: {error[:60]}')
    elif r1:
        print(f'  ✅ {symbol}: R1 synthesis ({len(r1)} chars)')
    else:
        print(f'  ⚠️  {symbol}: no R1 synthesis')

# Save brief for Opus
brief_path = '$NOFX_DIR/data/arena/opus-brief.json'
with open(brief_path, 'w') as f:
    json.dump(brief, f, indent=2)
print(f'\nBrief saved to {brief_path}')

# Also output the R1 summaries for Opus to read directly
print('\n=== R1 SUMMARIES FOR OPUS ===\n')
for c in brief['coins']:
    sym = c['symbol']
    r1 = c.get('r1_synthesis', '')
    if r1:
        # Truncate for readability but keep key content
        summary = r1[:1500] if len(r1) > 1500 else r1
        print(f'### {sym} (price: \${c.get(\"market_price\", 0):.2f})')
        print(summary)
        print()
    elif c.get('error'):
        print(f'### {sym}: ERROR - {c[\"error\"]}')
        print()

print('=== CURRENT PLAN ===')
if current_plan:
    print(f'Timestamp: {current_plan.get(\"timestamp\", \"unknown\")}')
    print(f'Regime: {current_plan.get(\"market_regime\", \"unknown\")}')
    for s in current_plan.get('strategies', []):
        print(f'  - {s.get(\"name\")}: {s.get(\"symbol\")} ({s.get(\"type\")}) \${s.get(\"allocation_usd\", 0)}')
else:
    print('No current plan found')

print('\n=== ACCOUNT STATUS ===')
" 2>/dev/null

# Get current positions and orders
echo ""
curl -s "$NOFX_API/account/balance" -H "Authorization: Bearer $TOKEN" 2>/dev/null | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(f'Balance: {json.dumps(d, indent=2)}')
except:
    print('Balance: unavailable')
" 2>/dev/null || true

# Get Hyperliquid positions from docker logs (most reliable)
cd "$NOFX_DIR"
docker compose logs nofx --tail=50 2>&1 | grep -E "Spot balance|Perpetuals equity|Margin used|Total:" | tail -5

echo ""
echo "[$(date '+%H:%M:%S')] === Hourly Pipeline End ==="
echo ""
echo "Opus: Review the R1 summaries above. Write a comprehensive trading plan for Fao."
echo "Write the plan to: $NOFX_DIR/data/arena/hourly-plan.json"
echo "Rules: NO WAITING. Always have active strategies. Consider current positions."
