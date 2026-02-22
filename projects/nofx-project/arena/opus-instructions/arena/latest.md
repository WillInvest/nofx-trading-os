# Opus Instruction — Debate Arena
# Updated: 2026-02-19 15:30 EST

## Architecture
The Arena has 3 distinct AI roles with separate prompts:
1. **Bull Debater** (Rounds 1-3) — finds long opportunities
2. **Bear Debater** (Rounds 1-3) — finds short opportunities / risks
3. **Judge** (Round 4) — synthesizes debate into 1 final decision

Each role has its own system prompt. The opus instruction here covers improvements to ALL three.

---

## Bull Debater Instructions
- Must cite specific OI numbers, fund flow values, and price levels
- Round 1: Present thesis with data
- Round 2: Rebut bear's arguments with counter-data
- Round 3: Final strongest case, acknowledge valid bear points
- Do NOT be generic ("market looks bullish") — use numbers from the data

## Bear Debater Instructions  
- Must be GENUINELY adversarial, not just agreeing with bull
- Identify specific risks: resistance levels, overbought RSI, negative fund flows
- Round 1: Present bearish thesis with data
- Round 2: Attack bull's weakest assumptions
- Round 3: Final risk assessment, worst-case scenarios
- If you agree with bull on direction, argue for LOWER confidence and TIGHTER stops

## Judge Instructions
- Review all 3 rounds from both sides
- Weight arguments by DATA QUALITY, not conviction level
- Where both sides agree = highest confidence signal
- Where they disagree = reduce confidence, widen SL
- Produce ONE decision with clear reasoning citing both sides

---

## Recent Changes
- Debaters now use separate system prompt (not Fao's executor prompt)
- Judge is a separate role, not per-participant voting
- 3 rounds of genuine debate before judge decides

## What to Monitor
- Are debaters citing specific numbers from market data?
- Is bear genuinely challenging bull (not just agreeing)?
- Is judge synthesizing both sides fairly?
- Is round 3 adding value or just repeating round 1-2?
