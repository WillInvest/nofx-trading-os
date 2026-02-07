# Ideas — Output-Asset AMM Fees

## Core Concept

**Standard AMM (Input Fee):**
- User sells token A, receives token B
- Fee charged on token A (what user sells)
- LP accumulates more of token A

**Proposed AMM (Output Fee):**
- User sells token A, receives token B
- Fee charged on token B (what user receives)
- LP accumulates more of token B

## Key Insight

The choice of fee asset affects **what LPs accumulate over time**.

### Input Fee Accumulation Pattern
- LPs accumulate the token that traders are SELLING
- In trending markets: LPs accumulate the LOSING token
- Example: ETH pumps → traders sell USDC for ETH → LPs get more USDC

### Output Fee Accumulation Pattern
- LPs accumulate the token that traders are BUYING
- In trending markets: LPs accumulate the WINNING token
- Example: ETH pumps → traders buy ETH → LPs get more ETH

## Hypotheses

### H1: Output fees may reduce impermanent loss
- Rationale: LPs accumulate the appreciating asset
- Counter: May just shift the timing of losses

### H2: Output fees change arbitrage dynamics
- Arbitrageurs extract the "output" token
- Fee on output means arbitrageurs pay more when they're most profitable
- May reduce arbitrage profitability and LVR

### H3: Output fees affect pool rebalancing
- Standard AMM: fees keep pool closer to original ratio
- Output AMM: fees may push pool toward the demanded asset

### H4: Trader perspective
- Input fee: known cost upfront (I pay 0.3% of what I send)
- Output fee: cost on what I receive (I get 0.3% less than quoted)
- UX difference may affect trader behavior

## Mathematical Questions

1. **Invariant preservation**: Does output fee preserve x*y=k differently?
2. **Arbitrage equation**: How does arbitrage condition change?
3. **LP value over time**: Expected value comparison
4. **Fee revenue**: Total fees collected (same or different?)
5. **Slippage interaction**: How does fee interact with price impact?

## Implementation Ideas

### Uniswap v4 Hook
- Use `afterSwap` hook to charge additional fee on output
- Or use custom accounting to modify output amount
- Could make fee structure configurable per pool

### Hybrid Approach
- Partial input fee + partial output fee
- Dynamically adjust ratio based on market conditions
- Example: 0.15% input + 0.15% output = 0.3% total

### Directional Fees
- Higher fee for one direction (buy vs sell)
- Could use output fees only for "informed" flow direction
- Combines with MEV protection

## Related Concepts

### Connection to LVR
- LVR comes from arbitrageurs extracting value
- Arbitrageurs profit from the output token
- Output fees directly tax arbitrage profits
- **Potential LVR mitigation mechanism!**

### Connection to FM-AMM (Batch Auctions)
- FM-AMM eliminates LVR via competitive auctions
- Output fees may be a simpler partial solution
- Could combine both mechanisms

## Risks & Concerns

1. **Lower liquidity attraction**: LPs may prefer input fees
2. **Complexity**: Harder to reason about for users
3. **Arbitrage changes**: May reduce efficient price discovery
4. **Game theory**: Novel equilibria to analyze

## Priority Research

1. **Math derivation**: Full formulas for output-fee CPMM
2. **Simulation**: Monte Carlo comparison of LP returns
3. **Empirical**: Backtest on historical Uniswap data
4. **Implementation**: Uniswap v4 hook prototype
