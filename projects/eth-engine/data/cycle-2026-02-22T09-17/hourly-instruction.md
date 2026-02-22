# Hourly Trading Instruction (from MiniMax Brain)

**Time:** 2026-02-22T14:16:50Z
**Valid until:** 2026-02-22 15:20:43 UTC

## EXECUTE THIS PLAN:
- **Action:** OPEN LONG
- **Symbol:** ETH
- **Size:** $0 at 0x leverage
- **Entry:** market
- **Stop Loss:** $None (MANDATORY)
- **Take Profit:** $None
- **Confidence:** 0%

## WHY:
Bearish structure confirmed: price dropped from $1980 to $1950 over 2 hours with high volume (28k in 08:00 hour). Price now BELOW daily SMA 20, 1H EMA 12/26 bearish cross (1967 < 1970), MACD histogram negative (-3.04). 1H RSI at 33 is oversold but price continues down. Two big red candles with volume spike suggest selling pressure. Rules: if price below daily SMA 20 with bearish EMA cross, bias should be short or no_trade, NOT contrarian long. On-chain and market data unavailable = no on-chain confirmation. With <2 confirming signals and stale data, no_trade is the correct decision.

## RULES:
- Execute this plan ONCE, then HOLD until next hourly instruction
- Do NOT overtrade - one entry per hour max
- If already in a position matching this direction, HOLD (do not double up)
- If in opposite position, CLOSE first then open new
- SL is non-negotiable. Never remove SL.
