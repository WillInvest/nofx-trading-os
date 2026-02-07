# Output Fees in Concentrated Liquidity AMMs

*Date: 2026-02-07*

## Motivation

Our output fee research focuses on constant product AMMs (x·y=k). But Uniswap v3/v4 uses **concentrated liquidity** where LPs provide within price ranges. How does output fee mechanism interact with this?

## Concentrated Liquidity Recap

In Uniswap v3:
- LPs specify price range [p_low, p_high]
- Liquidity only active when current price is in range
- Higher capital efficiency (up to 4000x for narrow ranges)
- But: LPs go "out of range" when price moves

### Key Difference: Fee Accumulation
- Standard: Fees accumulate globally to all LPs
- Concentrated: Fees only accrue to LPs whose range includes current price

## Output Fee Implications

### 1. Fee Distribution Changes

**Input fee (standard):**
- Fee in token X → distributed to in-range LPs
- LP accumulates the sold token

**Output fee:**
- Fee in token Y → distributed to in-range LPs
- LP accumulates the bought token

**Question**: Does this change LP incentives for range selection?

### 2. Range Strategy Interactions

Consider ETH/USDC pool with ETH rising:

**Input fee scenario:**
- Traders sell USDC, buy ETH
- In-range LPs accumulate USDC fees
- Price moves up → some LPs go out of range (holding more ETH)
- Fee revenue (USDC) depreciates relative to ETH

**Output fee scenario:**
- Traders sell USDC, buy ETH  
- In-range LPs accumulate ETH fees
- Price moves up → some LPs go out of range (holding more ETH)
- Fee revenue (ETH) appreciates with price

**Insight**: Output fees provide partial hedge against directional exposure for in-range LPs.

### 3. Just-in-Time (JIT) Liquidity

JIT LPs add concentrated liquidity right before a large swap to capture fees, then remove immediately after.

**With output fees:**
- JIT LP captures fee in output token
- If arbitrage trade: output is the valuable (appreciating) token
- May increase JIT profitability
- **Concern**: Could increase MEV, not reduce it

### 4. LVR in Concentrated Liquidity

Concentrated LPs face **amplified LVR**:
- Same arbitrage extracts more value from concentrated position
- LVR per dollar of liquidity is higher

**Output fee mitigation:**
- Our ~6.7% LVR reduction applies to each tick
- But concentrated LPs face more trades per dollar
- Net effect unclear without simulation

## Hypotheses for Concentrated Liquidity

### H1: Output fees benefit narrow ranges more
- Narrow range = more trades, more fees
- Output fee = fees in appreciating asset
- Combined: stronger hedge for aggressive LPs

### H2: Range selection may shift
- If output fees favor staying in range longer
- LPs may choose wider ranges (less rebalancing needed)
- Capital efficiency trade-off changes

### H3: Tick crossing dynamics change
- When price crosses tick boundary:
  - Input fee: LP exits with accumulated "sold" token
  - Output fee: LP exits with accumulated "bought" token
- May affect how LPs position around likely tick crossings

## Simulation Requirements

To properly analyze, we need to simulate:
1. Concentrated liquidity mechanics (tick-based)
2. Range selection strategies
3. Fee accumulation per tick
4. Compare LP returns: input vs output fees

### Proposed Extension to Current Simulation
```python
# Add to amm_fee_comparison.py:
# - Track LP positions by tick range
# - Accumulate fees per tick
# - Compare concentrated LP returns
# - Test narrow vs wide range strategies
```

## Research Questions

1. **Quantitative**: What's the LVR reduction for concentrated LPs?
2. **Optimal ranges**: Does output fee change optimal range width?
3. **JIT interaction**: Does output fee help or hurt retail LPs vs JIT?
4. **Fee tier interaction**: Different effects at 0.05% vs 0.3% vs 1%?

## Next Steps

1. [ ] Extend Monte Carlo to concentrated liquidity model
2. [ ] Backtest on historical v3 position data
3. [ ] Analyze fee accumulation patterns by tick
4. [ ] Model JIT LP behavior under both fee types

## Key Insight

Output fees may provide a **natural hedge** for concentrated LPs:
- When price moves up: LPs accumulate ETH (appreciating)
- When price moves down: LPs accumulate USDC (stable)

This could reduce the "wrong asset accumulation" problem inherent in concentrated liquidity.

---

*To be validated via simulation*
