# NOFX Arena Architecture v2 — Dynamic Prompt Management

## Core Principle

**Opus is the Head Coach.** It watches the game, reads the stats, and adjusts each player's instructions dynamically. It's not locked into rigid templates — it has full creative freedom to change what data gets collected, how debaters argue, how the judge decides, and how the trader executes.

## System Flow

```
┌─────────────────────────────────────────────────────────┐
│  OPUS — Head Coach (Hourly Review)                       │
│                                                         │
│  READS: past debates, plans, trader CoT, PnL,           │
│         market regime, what worked, what failed          │
│                                                         │
│  WRITES: updated prompts for all roles below             │
│          + data collection instructions                  │
│          + per-round debate strategy                     │
└──────────┬──────────────────────────────────────────────┘
           │ PUT /api/arena/prompts/:role
           ▼
┌──────────────────────────────────────────────────────────┐
│                DATA LAYER (Flexible)                      │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │ Arena Data Config │  │ Trader Data Config│             │
│  │ (hourly)          │  │ (5-min)           │             │
│  │                   │  │                   │             │
│  │ Opus decides:     │  │ Opus decides:     │             │
│  │ - timeframes      │  │ - timeframes      │             │
│  │ - indicators      │  │ - indicators      │             │
│  │ - rankings        │  │ - rankings        │             │
│  │ - special data    │  │ - orderbook depth │             │
│  │                   │  │ - recent trades   │             │
│  │ Could be 1h/4h    │  │ Could be 1m/5m    │             │
│  │ or 1d/1w if Opus  │  │ or 15m if Opus    │             │
│  │ wants big picture  │  │ wants more context│             │
│  └────────┬─────────┘  └────────┬─────────┘             │
└───────────┼──────────────────────┼───────────────────────┘
            │                      │
            ▼                      ▼
┌───────────────────────┐  ┌────────────────────────────────┐
│   ARENA (Hourly)      │  │   TRADER FAO (Every 5 min)     │
│                       │  │                                │
│   Round 1: OPENING    │  │   Reads:                       │
│   Bull: present case  │  │   - Hourly plan (from judge)   │
│   Bear: present case  │  │   - Short-term data            │
│                       │  │   - Current positions           │
│   Round 2: CLASH      │  │                                │
│   Bull: attack bear   │  │   Opus teaches Fao:            │
│   Bear: attack bull   │  │   - How to read the plan       │
│                       │  │   - When to follow vs deviate  │
│   Round 3: CLOSING    │  │   - Flash risk avoidance       │
│   Bull: final + concede│ │   - Flexibility boundaries     │
│   Bear: final + concede│ │                                │
│                       │  └────────────────────────────────┘
│   JUDGE: Final Verdict│
│   - Weighs all rounds │
│   - Produces 1h plan  │
│   - Opus teaches how  │
│     to use debate data│
└───────────────────────┘
```

## 6 Role Prompts (All Dynamic, Opus-Controlled)

### 1. Bull Debater — Per-Round Strategy

Opus writes a prompt that tells Bull HOW to behave in each round:

```
Round 1 (Opening):
- Present your bullish thesis with specific data
- Identify 2-3 strongest long candidates
- State entry levels, targets, and reasoning
- You are ESTABLISHING your position — be clear and data-heavy

Round 2 (Clash):
- READ the bear's Round 1 carefully
- Attack their weakest arguments with counter-data
- Defend your thesis where they challenged it
- Introduce new data the bear overlooked
- You are FIGHTING — be aggressive but factual

Round 3 (Closing):
- Acknowledge any valid bear points (shows intellectual honesty)
- Present your FINAL strongest case
- Adjust your confidence based on the debate
- If bear convinced you on some coins, DROP them
- You are CLOSING — summarize what survived the debate
```

Opus can change this dynamically. E.g., if past debates show Bull is too aggressive in R1 and wastes arguments, Opus can tell Bull to hold back strong data for R2.

### 2. Bear Debater — Per-Round Strategy

Mirror of Bull but adversarial:

```
Round 1 (Opening):
- Present bearish thesis / risks / short candidates
- Identify what could go WRONG with the obvious trades
- Find divergences, overbought signals, resistance levels

Round 2 (Clash):
- Dismantle bull's strongest argument
- If bull cited OI increase, show WHY that OI could be wrong
- Present counter-scenarios (what if support breaks?)

Round 3 (Closing):
- Concede where bull was genuinely stronger
- Final risk assessment: what's the WORST case?
- Adjust short confidence based on debate
```

Opus can make Bear more or less adversarial based on past performance. If Bear keeps agreeing with Bull, Opus strengthens the adversarial instructions.

### 3. Decision Maker (Judge) — Debate Synthesis

Opus teaches the judge HOW to use the debate:

```
You receive 6 messages: 3 from Bull, 3 from Bear.

HOW TO READ THE DEBATE:
1. Round 1 reveals each side's thesis — note the data points
2. Round 2 reveals which arguments survived attack
   - Arguments that survived R2 = high conviction
   - Arguments that got dismantled = low conviction
3. Round 3 reveals final positions after debate
   - What each side CONCEDED tells you the real risk
   - What both AGREE on = strongest signal

DECISION FRAMEWORK:
- Agreement between bull and bear = highest confidence
- Surviving arguments > initial arguments
- Concessions reveal genuine risks
- If debate was one-sided: be cautious (maybe both missed something)

OUTPUT: A 1-hour trading plan with:
- Direction + confidence per coin
- Entry zones, TP, SL
- What to AVOID (conceded risks)
- Flexibility notes for the trader
```

Opus can evolve this. E.g., if judge keeps making bad decisions despite good debates, Opus changes how the judge weighs arguments.

### 4. Trader Fao — Plan Execution + Flexibility

Opus teaches Fao the balance between following the plan and independent judgment:

```
THE PLAN IS YOUR NORTH STAR, NOT YOUR PRISON.

How to read the plan:
- Direction (bullish/bearish) = your bias for the hour
- Coin recommendations = your watchlist (not must-trade)
- TP/SL targets = your reference levels (adjust for real-time data)
- Avoid list = hard constraint (don't touch these)

When to FOLLOW the plan exactly:
- Normal market conditions
- Data confirms plan direction
- No sudden volatility spikes

When to DEVIATE from the plan:
- Flash crash: exit ALL positions immediately, ignore plan TP/SL
- Sudden OI spike (>20% in 5min): something changed, reassess
- Plan says long but 5m data shows momentum reversal: WAIT, don't force entry
- Your current position is > +3% profit: tighten SL regardless of plan

FLEXIBILITY RULES:
- You can DELAY a plan entry (wait for better price) — ALWAYS OK
- You can TIGHTEN a stop loss — ALWAYS OK
- You can SKIP a trade the plan suggests — OK if data doesn't confirm
- You CANNOT open trades the plan says to avoid — NEVER OK
- You CANNOT widen a stop loss — NEVER OK
```

### 5. Data Collector — Arena (Long-term, Hourly)

This is NOT a fixed config. Opus writes INSTRUCTIONS for what data to collect:

```
Current Market Regime: [Opus fills this in]
e.g., "Trending bull market, BTC above 20-day EMA, low volatility"

Data to Collect:
- Klines: 1h (50 candles), 4h (20 candles)
- OI rankings: top 10 increase, top 10 decrease
- Fund flows: institutional + retail
- Indicators: EMA(20,50), RSI(14), ATR(14)
- Special: Include WEEKLY close levels for support/resistance context

Why this data:
- 4h gives trend context for hourly debate
- OI shows where smart money is moving
- Weekly levels because BTC is near weekly resistance at $68K

What's NOT needed right now:
- 1m data (too noisy for strategic debate)
- Bollinger bands (not useful in trending market)
- Price rankings (Arena doesn't need to scan for coins, we have candidates)
```

Opus can change this completely next hour. If market turns choppy, Opus might add Bollinger Bands and remove EMA. If a macro event happens, Opus might add daily/weekly klines for perspective.

### 6. Data Collector — Trader (Short-term, 5-min)

```
Current Phase: [Opus fills in]
e.g., "Executing bullish plan, watching for entry on BTC pullback"

Data to Collect:
- Klines: 5m (20 candles)
- Indicators: EMA(9,21) for momentum, RSI(14) for overbought check
- Volume: last 5 bars vs 20-bar average
- Current positions + unrealized PnL

Why:
- 5m EMA crossover for precise entry timing
- Volume confirms breakout vs fakeout
- RSI prevents buying into overbought exhaustion

Not needed:
- 4h klines (Arena already analyzed this)
- OI rankings (plan already incorporated this)
- Fund flows (too slow for 5-min decisions)
```

## Database Design

### New Table: `arena_prompts`

```sql
CREATE TABLE arena_prompts (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    -- 'bull', 'bear', 'judge', 'trader',
    -- 'data_arena', 'data_trader'
    prompt TEXT NOT NULL,          -- the actual prompt
    opus_reasoning TEXT,           -- WHY Opus wrote this version
    data_config TEXT,              -- JSON: for data roles, what to collect
    version INTEGER DEFAULT 1,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME,
    updated_at DATETIME
);
-- Keep history: on update, increment version, keep old rows with is_active=0
```

### API Endpoints

```
GET  /api/arena/prompts              — list all active prompts
GET  /api/arena/prompts/:role        — get one role's prompt
PUT  /api/arena/prompts/:role        — update (creates new version)
GET  /api/arena/prompts/:role/history — version history
```

### How Components Read Prompts

**Debate Engine:**
1. Reads `data_arena` prompt → configures data collection
2. Reads `bull` prompt → builds Round 1/2/3 system prompts
3. Reads `bear` prompt → builds Round 1/2/3 system prompts
4. Reads `judge` prompt → builds judge system prompt

**Trader (auto_trader.go):**
1. Reads `data_trader` prompt → configures indicators/klines
2. Reads `trader` prompt → builds system prompt
3. Injects hourly plan into user prompt

## Frontend Design

### Arena Page — Redesigned

```
┌─────────────────────────────────────────────────────┐
│ Left Sidebar          │  Main Content               │
│                       │                              │
│ Session List          │  ┌─────────────────────────┐ │
│ ┌───────────────┐     │  │ OPUS REASONING          │ │
│ │ ● Arena 15:00 │     │  │ "I changed Bear's R2    │ │
│ │   Feb 19 3:00p│     │  │  prompt because it was  │ │
│ │   BTC +3.2%   │     │  │  too agreeable..."      │ │
│ │               │     │  └─────────────────────────┘ │
│ │ ● Arena 14:00 │     │                              │
│ │   Feb 19 2:00p│     │  ┌───┬───┬───┬───┬───┬───┐  │
│ │   BTC +1.1%   │     │  │ALL│R1 │R2 │R3 │⚖️ │📊│  │
│ └───────────────┘     │  └───┴───┴───┴───┴───┴───┘  │
│                       │                              │
│                       │  [Selected tab content]      │
│                       │                              │
│                       │  ALL: Full debate timeline   │
│                       │  R1: Round 1 bull + bear     │
│                       │  R2: Round 2 clash           │
│                       │  R3: Round 3 closing         │
│                       │  ⚖️: Judge's verdict + plan  │
│                       │  📊: Data that was collected │
│                       │                              │
│                       │  Each message shows:         │
│                       │  - The AI's response (CoT)   │
│                       │  - Click to see its prompt   │
│                       │  - Click to see its data     │
└───────────────────────┴──────────────────────────────┘
```

### Trader Dashboard — Updated

```
Each decision cycle shows:
┌──────────────────────────────────────┐
│ Cycle #25 — 15:15 EST               │
│ Action: HOLD BTC LONG               │
│                                      │
│ [Plan] [Data] [Prompt] [CoT]        │
│                                      │
│ Plan: "Bullish, TP $68K, SL $66.2K" │
│ CoT: "Plan says hold BTC long.      │
│   5m RSI=58, not overbought.        │
│   Volume declining but not alarming. │
│   SL at $66,200 per plan.           │
│   Decision: HOLD, no action needed." │
└──────────────────────────────────────┘
```

## Cron Job — Opus Hourly Review

```
1. GATHER DATA (read-only)
   - Last 1-5 hours of debate messages
   - Last 1-5 hours of judge decisions
   - Last 1-5 hours of trader CoT
   - Current PnL, positions, win rate
   - Current market regime (volatility, trend)

2. ANALYZE
   - Did debaters use specific data? Or generic fluff?
   - Did bear actually challenge bull? Or agree?
   - Did judge's plan match what actually happened?
   - Did trader follow the plan? When did it deviate? Was that good?
   - What data was useful? What was noise?

3. UPDATE PROMPTS (write)
   For each role that needs improvement:
   PUT /api/arena/prompts/:role with:
   - New prompt text
   - opus_reasoning: "Changed because X wasn't working"
   
   For data collectors:
   PUT /api/arena/prompts/data_arena with:
   - Updated data_config JSON
   - opus_reasoning: "Added weekly klines because BTC near weekly resistance"

4. REPORT
   - What changed and why
   - Performance summary
   - System health
```

## Implementation Order

### Phase 1: Database + API (backend)
1. Create `arena_prompts` table in store/
2. Add CRUD API endpoints
3. Seed initial prompts from current hardcoded values

### Phase 2: Debate Engine (backend)
1. Debate engine reads bull/bear/judge prompts from DB
2. Data collection reads from data_arena config
3. Per-round prompt injection (R1/R2/R3 context added to base prompt)

### Phase 3: Trader (backend)
1. Trader reads prompt from DB instead of strategy prompt_sections
2. Data collection reads from data_trader config
3. Hourly plan still injected into user prompt

### Phase 4: Frontend
1. Arena page: round tabs + per-message prompt viewer
2. Trader dashboard: plan/data/prompt/cot tabs per cycle
3. Opus reasoning panel at top of both pages

### Phase 5: Cron (Opus)
1. Update cron to read data, analyze, update prompts via API
2. Remove file-based opus instructions
3. Clean up old files

### Phase 6: Cleanup
1. Remove hardcoded BuildDebateSystemPrompt, BuildPromptRule
2. Remove opus-instructions/ directory
3. Remove PROMPT_OPTIMIZATION.md, OBSERVABILITY_SPEC.md
4. Prune unused Docker images
