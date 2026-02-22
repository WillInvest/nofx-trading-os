# Prompt Optimization Plan — Arena + Fao

## Current Architecture Problem

```
[Raw Market Data] → Arena (debates) → hourly-plan.json
[Raw Market Data] → Fao (trades) ← should read plan but DOESN'T
```

Fao receives the SAME raw data the Arena already analyzed and re-does the analysis from scratch. The hourly plan is never injected into Fao's input.

## Current Prompt Sizes

| Component | Chars | Problem |
|-----------|-------|---------|
| System prompt | 6,234 | 2,000 chars of data dictionary, generic role |
| Input prompt | 6,973 | 80% ranking tables, 0% hourly plan |
| **Total per cycle** | **~13,200** | Every 5 min = ~158K chars/hour |

## What Fao Actually Gets (Input Prompt Breakdown)

1. ✅ Account state (compact, ~200 chars) — **KEEP**
2. ❌ Candidate coins = 0 (coin source not configured!) — **FIX**
3. ⚠️ OI Increase ranking (top 10 table, ~800 chars) — **KEEP but condense**
4. ⚠️ OI Decrease ranking (top 10 table, ~800 chars) — **KEEP but condense**
5. ⚠️ Institution Inflow ranking (top 10, ~600 chars) — **REDUNDANT with Arena**
6. ⚠️ Institution Outflow ranking (top 10, ~600 chars) — **REDUNDANT with Arena**
7. ⚠️ Retail flow (1 line) — **KEEP**
8. ⚠️ Price gainers 1h/4h/24h (3 tables, ~2,400 chars) — **REDUNDANT with Arena**
9. ⚠️ Price losers 1h/4h/24h (3 tables, ~2,400 chars) — **REDUNDANT with Arena**
10. ❌ Hourly plan — **MISSING, critical**

## Optimization: Role Separation

### Arena (Strategist) — Runs hourly
**Should get:** ALL raw market data (OI, fund flows, price rankings, klines)
**Job:** Debate, analyze, produce hourly plan with:
- Market bias (bullish/bearish/neutral)
- Specific coins to watch (long candidates, short candidates)  
- Entry zones, TP/SL targets
- Coins to AVOID
- Risk level assessment

### Fao (Executor) — Runs every 5 min
**Should get:**
1. Account state + positions (already has)
2. **Hourly plan** (MISSING — needs injection)
3. Candidate coin data (for coins the plan recommends)
4. OI + fund flow for current positions (for monitoring)

**Should NOT get:**
- Full market-wide rankings (Arena already did this)
- Price gainers/losers tables (Arena's job)
- Redundant analysis work

## Implementation Options

### Option A: Inject plan via `custom_prompt` field (Quick, no code change)
The strategy has a `custom_prompt` field that gets appended to system prompt.
We can update it hourly via API with the current plan.
- **Pro:** No backend code change needed
- **Con:** Plan is in system prompt (static per cycle), not user prompt (dynamic)

### Option B: Inject plan via `role_definition` prompt section (Quick, no code change)
Update `prompt_sections.role_definition` via PUT API to include the current plan.
- **Pro:** Clean, uses existing infrastructure
- **Con:** Same as A — mixes role with dynamic data

### Option C: Add `hourly_plan` field to strategy config (Proper, needs code change)
Add a new field that gets injected into BuildUserPrompt.
- **Pro:** Clean separation, plan appears in user prompt where it belongs
- **Con:** Requires Go code change + rebuild

### Option D: File-based injection (Hacky but effective)
Have the Arena write hourly-plan.json, then Fao's system prompt says "the hourly plan is: {plan}".
Update `custom_prompt` via API after each Arena run.
- **Pro:** No code change, dynamic
- **Con:** Relies on cron timing

## Recommended: Option A (now) → Option C (in PR)

### Immediate (Option A):
1. After each Arena debate, update strategy `custom_prompt` with the synthesized plan
2. The cron job already does this — just needs to actually call PUT with the plan

### Enable proper coin sources:
Fix the strategy config — enable `use_hyper_main: true` so Fao gets candidate coins

### Reduce noise:
- Disable price rankings (Arena handles market scanning)
- Keep OI + fund flow rankings (useful real-time signals for execution)
- Enable indicators: EMA, RSI, ATR (Fao needs execution-level technicals)

## Strategy Config Changes Needed

```json
{
  "config": {
    "coin_source": {
      "source_type": "hyperliquid",
      "use_hyper_main": true
    },
    "indicators": {
      "klines": {
        "primary_timeframe": "5m",
        "primary_count": 50,
        "enable_multi_timeframe": true
      },
      "enable_ema": true,
      "enable_rsi": true,
      "enable_atr": true,
      "enable_volume": true,
      "enable_oi": true,
      "enable_funding_rate": true,
      "enable_oi_ranking": true,
      "enable_netflow_ranking": true,
      "enable_price_ranking": false
    }
  }
}
```

## Prompt Section Rewrites

### Role Definition (for Fao)
```
# You are Trader Fao — Short-Term Executor

You execute trades based on the Hourly Plan from the Debate Arena.

## Your Role
- You are NOT the strategist. The Arena handles market analysis.
- You ARE the executor. Your job: timing, entry, risk management.
- Every decision must reference the current Hourly Plan.

## Decision Framework
1. Read the Hourly Plan (in Custom Strategy section below)
2. Check current positions — align with plan bias?
3. For new entries: only trade coins the plan recommends
4. For exits: respect plan's TP/SL targets
5. Override plan ONLY if real-time data shows urgent risk (liquidation, flash crash)
```

### Decision Process
```
1. State the plan's current bias and targets
2. Check positions — TP/SL per plan
3. If no position: is there a plan-aligned setup with confidence ≥ 75?
4. Chain of thought (MUST cite plan), then JSON
```

## Token Savings Estimate

| Component | Before | After | Savings |
|-----------|--------|-------|---------|
| System prompt | 6,234 | ~4,500 | -28% |
| Input (rankings) | ~5,800 | ~2,500 | -57% |
| Input (plan injection) | 0 | +500 | — |
| **Total per cycle** | **~13,200** | **~8,500** | **-36%** |
| **Per hour (12 cycles)** | **158K** | **102K** | **-36%** |

## Implementation Steps

1. ✅ Write this optimization plan
2. [ ] Update strategy config (coin source, indicators)
3. [ ] Rewrite prompt_sections (role_definition, decision_process)
4. [ ] Update cron job to inject hourly plan into custom_prompt after each debate
5. [ ] Monitor 2-3 cycles to verify Fao references the plan
6. [ ] Iterate on prompt quality based on CoT analysis
