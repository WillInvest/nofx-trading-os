# Opus Instruction — 2026-02-19 14:00 EST

## Changes Made
- Initial setup: Separated Arena (strategist) from Fao (executor)
- Fao's role redefined: No longer doing full market analysis, now focuses on plan execution
- Enabled Hyperliquid Main coin source (top 30) for candidate generation
- Disabled price rankings (Arena handles market scanning)
- Enabled EMA, RSI, ATR indicators for execution-level technicals
- Hourly plan now injected into Fao's custom_prompt via strategy API

## Reasoning
Previously Fao received the same raw data as the Arena and independently re-analyzed everything. This was:
1. Wasteful (duplicate analysis)
2. Contradictory (Fao might reach different conclusions than the plan)
3. Missing the plan entirely (it was never injected)

The new architecture: Arena debates → produces hourly plan → plan injected into Fao → Fao executes based on plan.

## What to Monitor
- Is Fao citing the hourly plan in reasoning?
- Are debate arguments using specific data points?
- Token savings (~36% expected)
