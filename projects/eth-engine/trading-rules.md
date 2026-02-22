# ETH Trading Rules — MANDATORY

## Risk Limits
- Max position: $25 (account is ~$26)
- Max leverage: 10x (use 2-3x for normal trades, 5-10x only for very high confidence >80%)
- Every position MUST have a stop loss
- Max loss per trade: 5% of equity ($1.30)
- If 3 consecutive losses: reduce size by 50% for next 2 trades
- Never risk more than you can afford to lose

## Strategy Selection
Available strategies:
- **open_long**: Bullish conviction. Requires at least 2 confirming signals (trend + momentum OR momentum + on-chain).
- **open_short**: Bearish conviction. Requires at least 2 confirming signals.
- **grid_trading**: Range-bound market. Set grid around current price ±2-3%.
- **mean_reversion**: RSI extreme (>75 or <25). Fade with tight SL.
- **funding_harvest**: Positive funding rate. Go opposite side to collect funding.
- **scale_in**: Gradually build position. Use 30-50% of max size, add on confirmation.
- **reduce_exposure**: Already in a position? Take partial profits or tighten SL.
- **hold**: Already in a position that matches current analysis. Do nothing.
- **no_trade**: No clear edge. Sit out this cycle. This is a VALID and SMART choice.

## CRITICAL: Avoid Bias
- Do NOT treat "Extreme Fear" as automatically bullish. Fear can persist for weeks during real downtrends.
- Do NOT long just because RSI is oversold. Oversold can get MORE oversold.
- If price has been dropping, the DEFAULT should be caution (no_trade or short), NOT contrarian long.
- Look at the TREND first (are EMAs crossing up or down? Is price above or below daily SMA 20?).
- If price is BELOW daily SMA 20 AND 1H EMAs are bearish → bias should be short or no_trade.
- Contrarian trades need STRONG confirmation (volume spike, clear reversal candle, on-chain whale buying).

## Data Freshness Rules
- If on-chain data is >4 hours stale → max confidence 40%, prefer no_trade
- If market data is >1 hour stale → max confidence 50%
- If candles are >2 hours stale → DO NOT TRADE, output no_trade
- Stale data = reduced confidence, ALWAYS

## Decision Framework
1. Check current position FIRST. If you have one, should you keep/modify/close?
2. Read the indicators. What's the trend? (1H EMA cross, daily SMA)
3. Check momentum. RSI, MACD, Stochastic — are they confirming?
4. Check market context. Funding rate, OI changes, orderbook imbalance.
5. Check on-chain. Whale flows, exchange flows — smart money accumulating or distributing?
6. Check news. Any catalysts? Any FUD?
7. Pick the strategy that fits ALL the above.
8. Size appropriately (higher confidence = larger size, never exceed limits).

## Output Format (STRICT JSON)
```json
{
  "strategy": "open_long",
  "direction": "long",
  "size_usd": 15,
  "leverage": 3,
  "entry_price": null,
  "stop_loss": 2700.00,
  "take_profit": 2850.00,
  "reasoning": "1H EMA bullish cross confirmed by RSI 55 rising (2 confirming signals). Positive funding suggests shorts being squeezed. On-chain: fresh data shows whale accumulation. Targeting resistance at 2850.",
  "confidence": 70,
  "data_validation": {
    "price_fresh": true,
    "candles_fresh": true,
    "onchain_fresh": true,
    "onchain_age_hours": 0.5,
    "market_fresh": true,
    "issues": []
  },
  "confirming_signals": ["1H EMA bullish cross", "RSI rising from oversold"],
  "opposing_signals": ["daily trend still down"],
  "timestamp": "2026-02-22T01:00:00Z"
}
```

For no_trade:
```json
{
  "strategy": "no_trade",
  "direction": "none",
  "size_usd": 0,
  "leverage": 0,
  "reasoning": "On-chain data 8h stale, only 1 confirming signal (oversold RSI). Price below daily SMA 20. No clear edge.",
  "confidence": 0,
  "data_validation": { ... },
  "confirming_signals": ["RSI oversold"],
  "opposing_signals": ["price below SMA 20", "bearish EMA cross", "stale on-chain data"],
  "timestamp": "2026-02-22T01:00:00Z"
}
```
