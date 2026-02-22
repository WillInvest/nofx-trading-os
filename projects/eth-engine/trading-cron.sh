#!/bin/bash
# ETH Trading Cron - Complete Pipeline
# This script:
# 1. Collects fresh trading data
# 2. Fetches current position state from NOFX API
# 3. Builds comprehensive brain-prompt.md
# 4. Saves raw data to cycle directory

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
ARENA_DIR="/home/openclaw/.openclaw/workspace/projects/nofx-project/nofx/data/arena"
LOG_FILE="$DATA_DIR/cron.log"

# JWT Config for NOFX API
USER_ID="34dd0d3b-bf61-4a6a-82fc-0f0af42355c1"
JWT_SECRET="Fm9Dd/bc2ix30BkhbC22lKy2m/0CDjedaX/TAwkQMGc="
NOFX_API="http://localhost:8090"

mkdir -p "$DATA_DIR"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

# Generate JWT token for NOFX API
generate_jwt() {
    python3 -c "
import jwt, time
token = jwt.encode({'user_id': '$USER_ID', 'exp': int(time.time()) + 3600}, '$JWT_SECRET', algorithm='HS256')
print(token)
"
}

log "=== Trading Cycle Start ==="

# Generate cycle ID
CYCLE_ID=$(date '+%Y-%m-%dT%H-%M')
CYCLE_DIR="$DATA_DIR/cycle-$CYCLE_ID"
mkdir -p "$CYCLE_DIR"

log "Cycle ID: $CYCLE_ID"

# Step 1: Collect trading context
log "Step 1: Collecting trading context..."
cd "$SCRIPT_DIR"
python3 collect-trading-context.py 2>&1 | tee -a "$LOG_FILE"

if [ ! -f "$DATA_DIR/trading-context.json" ]; then
    log "ERROR: trading-context.json not created"
    exit 1
fi

# Step 2: Fetch position state from NOFX API
log "Step 2: Fetching position state from NOFX API..."
JWT_TOKEN=$(generate_jwt)

POSITION_RESPONSE=$(curl -s -X GET "$NOFX_API/api/traders" \
    -H "Authorization: Bearer $JWT_TOKEN" \
    -H "Content-Type: application/json" 2>/dev/null || echo '{"error": "API not available"}')

echo "$POSITION_RESPONSE" > "$CYCLE_DIR/position-state.json"
log "Position state saved to cycle directory"

# Extract position info from NOFX response
CURRENT_POSITION=$(echo "$POSITION_RESPONSE" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'positions' in data and len(data['positions']) > 0:
    for p in data['positions']:
        if p.get('coin') == 'ETH':
            print(json.dumps(p))
            sys.exit(0)
print('null')
" 2>/dev/null || echo "null")

BALANCE=$(echo "$POSITION_RESPONSE" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('balance', data.get('available_balance', 0)))
" 2>/dev/null || echo "0")

# Step 3: Read collected data
log "Step 3: Reading collected data..."
TRADING_CONTEXT=$(cat "$DATA_DIR/trading-context.json" 2>/dev/null || echo '{}')
POSITION_STATE=$(cat "$DATA_DIR/position-state.json" 2>/dev/null || echo '{}')
TRADING_RULES=$(cat "$SCRIPT_DIR/trading-rules.md" 2>/dev/null || echo '')

# Extract ETH price
ETH_PRICE=$(echo "$TRADING_CONTEXT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('eth_price', 0))
" 2>/dev/null || echo "0")

# Read on-chain data from arena (if available)
ONCHAIN_DATA=""
if [ -f "$ARENA_DIR/onchain-hourly.json" ]; then
    ONCHAIN_DATA=$(cat "$ARENA_DIR/onchain-hourly.json" 2>/dev/null || echo '{}')
    log "On-chain data found in arena"
else
    log "Warning: No on-chain data in arena"
fi

# Read market data from arena (if available)
MARKET_DATA=""
if [ -f "$ARENA_DIR/market-live.json" ]; then
    MARKET_DATA=$(cat "$ARENA_DIR/market-live.json" 2>/dev/null || echo '{}')
    log "Market data found in arena"
elif [ -f "$ARENA_DIR/market-data-hourly.json" ]; then
    MARKET_DATA=$(cat "$ARENA_DIR/market-data-hourly.json" 2>/dev/null || echo '{}')
    log "Market data (hourly) found in arena"
else
    log "Warning: No market data in arena"
fi

# Read news from arena (if available)
NEWS_DATA=""
if [ -f "$ARENA_DIR/news-summary.json" ]; then
    NEWS_DATA=$(cat "$ARENA_DIR/news-summary.json" 2>/dev/null || echo '{}')
    log "News data found in arena"
else
    log "Warning: No news data in arena"
fi

# Save raw data to cycle directory
log "Step 4: Saving raw data to cycle directory..."
echo "$ONCHAIN_DATA" > "$CYCLE_DIR/node-data.json"
echo "$MARKET_DATA" > "$CYCLE_DIR/market-data.json"
echo "$NEWS_DATA" > "$CYCLE_DIR/news-data.json"

# Extract and save price data
python3 -c "
import json
with open('$DATA_DIR/trading-context.json') as f:
    data = json.load(f)
price_data = {
    'eth_price': data.get('eth_price'),
    'candles_1h': data.get('candles_1h', [])[-24:],
    'candles_5m': data.get('candles_5m', [])[-60:],
    'candles_daily': data.get('candles_daily', [])[-7:],
    'indicators_1h': data.get('indicators_1h', {}),
    'indicators_5m': data.get('indicators_5m', {}),
    'indicators_daily': data.get('indicators_daily', {}),
    'timestamp': data.get('timestamp')
}
with open('$CYCLE_DIR/price-data.json', 'w') as f:
    json.dump(price_data, f, indent=2)
"
log "Price data saved to cycle directory"

# Step 5: Build brain-prompt.md using Python
log "Step 5: Building brain-prompt.md..."

CURRENT_TIME=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

python3 << PYTHON_SCRIPT
import json
import os
from datetime import datetime

# Load data
with open('$DATA_DIR/trading-context.json') as f:
    trading_context = json.load(f)

with open('$CYCLE_DIR/position-state.json') as f:
    position_state = json.load(f)

with open('$SCRIPT_DIR/trading-rules.md') as f:
    trading_rules = f.read()

# Load arena data
onchain_data = {}
market_data = {}
news_data = {}

arena_dir = '$ARENA_DIR'
if os.path.exists(f'{arena_dir}/onchain-hourly.json'):
    with open(f'{arena_dir}/onchain-hourly.json') as f:
        onchain_data = json.load(f)

if os.path.exists(f'{arena_dir}/market-live.json'):
    with open(f'{arena_dir}/market-live.json') as f:
        market_data = json.load(f)
elif os.path.exists(f'{arena_dir}/market-data-hourly.json'):
    with open(f'{arena_dir}/market-data-hourly.json') as f:
        market_data = json.load(f)

if os.path.exists(f'{arena_dir}/news-summary.json'):
    with open(f'{arena_dir}/news-summary.json') as f:
        news_data = json.load(f)

# Get ETH price
eth_price = trading_context.get('eth_price', 0)

# Build prompt
prompt = f"""# ETH Trading Brain Prompt

**Generated:** $CURRENT_TIME
**Cycle ID:** $CYCLE_ID

---

## CURRENT TIME (UTC)
$CURRENT_TIME

---

## CURRENT POSITION & ACCOUNT STATE

**NOFX API Response:**
{json.dumps(position_state, indent=2)[:1000]}

**Position from Trading Context:**
{json.dumps(trading_context.get('position'), indent=2) if trading_context.get('position') else 'No position'}

**Balance from Trading Context:**
Equity: {trading_context.get('balance', {}).get('equity', 0)}
Available: {trading_context.get('balance', {}).get('available', 0)}
Unrealized PnL: {trading_context.get('balance', {}).get('unrealized_pnl', 0)}

---

## ETH PRICE & CANDLES

**Current ETH Price:** \${eth_price}

### 1H Candles (last 6)
"""

# Add 1H candles
candles_1h = trading_context.get('candles_1h', [])[-24:]
for c in candles_1h[-6:]:
    ts = datetime.fromtimestamp(c.get('t', 0)/1000).strftime('%m-%d %H:%M') if c.get('t') else 'N/A'
    prompt += f"{ts} | O:{c.get('o')} H:{c.get('h')} L:{c.get('l')} C:{c.get('c')} V:{c.get('v',0):.0f}\n"

prompt += """
### 5m Candles (last 12)
"""
candles_5m = trading_context.get('candles_5m', [])[-60:]
for c in candles_5m[-12:]:
    ts = datetime.fromtimestamp(c.get('t', 0)/1000).strftime('%H:%M') if c.get('t') else 'N/A'
    prompt += f"{ts} | O:{c.get('o')} C:{c.get('c')} V:{c.get('v',0):.0f}\n"

prompt += """
### Daily Candles (last 7)
"""
candles_daily = trading_context.get('candles_daily', [])[-7:]
for c in candles_daily:
    ts = datetime.fromtimestamp(c.get('t', 0)/1000).strftime('%m-%d') if c.get('t') else 'N/A'
    prompt += f"{ts} | O:{c.get('o')} H:{c.get('h')} L:{c.get('l')} C:{c.get('c')}\n"

# Add indicators
ind_1h = trading_context.get('indicators_1h', {})
prompt += f"""
---

## TECHNICAL INDICATORS

### 1H Indicators
SMA 7: {ind_1h.get('sma_7')}, SMA 25: {ind_1h.get('sma_25')}, SMA 99: {ind_1h.get('sma_99')}
EMA 12: {ind_1h.get('ema_12')}, EMA 26: {ind_1h.get('ema_26')}
RSI 14: {ind_1h.get('rsi_14')}
MACD: {ind_1h.get('macd_line')} (signal: {ind_1h.get('macd_signal')}, hist: {ind_1h.get('macd_histogram')})
Bollinger: U:{ind_1h.get('bollinger_upper')} M:{ind_1h.get('bollinger_middle')} L:{ind_1h.get('bollinger_lower')}
ATR 14: {ind_1h.get('atr_14')}
Stoch RSI: K:{ind_1h.get('stoch_rsi_k')} D:{ind_1h.get('stoch_rsi_d')}
Williams %R: {ind_1h.get('williams_r')}
CCI 20: {ind_1h.get('cci_20')}
MFI 14: {ind_1h.get('mfi_14')}
VWAP: {ind_1h.get('vwap')}
"""

ind_5m = trading_context.get('indicators_5m', {})
prompt += f"""
### 5m Indicators
EMA 12: {ind_5m.get('ema_12')}, EMA 26: {ind_5m.get('ema_26')}
RSI 14: {ind_5m.get('rsi_14')}
Volume Ratio: {ind_5m.get('volume_ratio')}
"""

ind_daily = trading_context.get('indicators_daily', {})
prompt += f"""
### Daily Indicators
SMA 20: {ind_daily.get('sma_20')}, SMA 50: {ind_daily.get('sma_50')}
RSI 14: {ind_daily.get('rsi_14')}
"""

# Add on-chain data
prompt += f"""
---

## ON-CHAIN DATA

**Source:** $ARENA_DIR/onchain-hourly.json

"""
if onchain_data:
    prompt += f"""Timestamp: {onchain_data.get('timestamp', 'N/A')}
Block: {onchain_data.get('block_number', 'N/A')}
"""
    for k, v in list(onchain_data.items())[:10]:
        if k not in ['timestamp', 'block_number', 'raw']:
            prompt += f"{k}: {str(v)[:200]}\n"
else:
    prompt += "**ON-CHAIN DATA NOT AVAILABLE**\n"

# Add market data
prompt += f"""
---

## MARKET DATA

**Source:** $ARENA_DIR (market-live.json or market-data-hourly.json)

"""
if market_data:
    prompt += f"Timestamp: {market_data.get('timestamp', 'N/A')}\n"
    for k in ['funding_rate', 'open_interest', 'oi_change']:
        if k in market_data:
            prompt += f"{k}: {market_data[k]}\n"
else:
    prompt += "**MARKET DATA NOT AVAILABLE**\n"

# Add news
prompt += f"""
---

## NEWS & SENTIMENT

**Source:** $ARENA_DIR/news-summary.json

"""
if news_data:
    stories = news_data.get('top_stories', [])[:3]
    for i, s in enumerate(stories, 1):
        prompt += f"{i}. {s.get('headline', 'N/A')} [{s.get('impact', '?')}]\n"
    indices = news_data.get('indices', [])
    if indices:
        prompt += f"Fear & Greed: {indices[0].get('value', 'N/A')} ({indices[0].get('classification', '?')})\n"
    prompt += f"Overall Sentiment: {news_data.get('sentiment', 'N/A')}\n"
else:
    prompt += "**NEWS DATA NOT AVAILABLE**\n"

# Add recent trades
recent_trades = trading_context.get('recent_trades', [])[-5:]
prompt += """
---

## RECENT TRADES

"""
for t in recent_trades:
    prompt += f"{t.get('timestamp', 'N/A')} | {t.get('side', '?')} | \${t.get('size', 0)} | PnL: \${t.get('pnl', 0):.2f}\n"

streak = trading_context.get('trade_streak', {})
prompt += f"""
**Trade Streak:**
{streak.get('direction', 'none').upper()} streak: {streak.get('streak', 0)} trades, Recent PnL: \${streak.get('recent_pnl', 0):.2f}
"""

# Add trading rules
prompt += f"""
---

## TRADING RULES (MANDATORY)

{trading_rules}

---

## YOUR TASK

1. **VALIDATE DATA FIRST** - Check timestamps, freshness, price reasonability
2. **ANALYZE** - Review indicators, on-chain, market, news
3. **DECIDE** - Pick strategy, direction, size, SL, TP
4. **OUTPUT** - Valid JSON with ALL required fields

**CRITICAL:**
- Max leverage: 10x
- Max position size: $25
- Every trade MUST have stop loss
- If on-chain/market data is stale (>6h), reduce confidence by 20%

Output ONLY valid JSON. No markdown fences.
"""

# Write prompt
with open('$DATA_DIR/brain-prompt.md', 'w') as f:
    f.write(prompt)

print("Brain prompt written successfully")
PYTHON_SCRIPT

log "Brain prompt written to $DATA_DIR/brain-prompt.md"

# Step 6: Save cycle metadata
echo "$CURRENT_TIME" > "$CYCLE_DIR/timestamp.txt"

log "=== Data Collection Complete ==="
log "Ready for brain analysis. Brain should read: $DATA_DIR/brain-prompt.md"
log "Brain should write decision to: $DATA_DIR/decision.json"
log "After decision, run: bash $SCRIPT_DIR/execute-decision.sh"
