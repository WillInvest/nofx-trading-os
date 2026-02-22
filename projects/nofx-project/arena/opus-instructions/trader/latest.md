# Opus Instruction — Trader Fao
# Updated: 2026-02-19 15:20 EST

## Changes Made
- Fao redefined as Short-Term Executor (not strategist)
- Hourly plan injected via custom_prompt field
- Enabled Hyperliquid Main coin source (top 30)
- Disabled price rankings (Arena handles market scanning)
- Enabled EMA, RSI, ATR for execution-level technicals

## Reasoning
Fao was duplicating the Arena's work — re-analyzing the same raw data. Now the Arena debates and produces a plan; Fao executes based on the plan. This reduces tokens by ~44% and eliminates contradictory analysis.

## What to Monitor
- Is Fao citing the hourly plan in CoT?
- Are stop losses set per plan targets?
- Is Fao overtrading?
