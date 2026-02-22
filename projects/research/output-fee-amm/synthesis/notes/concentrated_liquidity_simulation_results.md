# Concentrated Liquidity Simulation Results

**Date:** 2026-02-07

## Summary

Extended Monte Carlo simulation to Uniswap v3-style concentrated liquidity. Key question: Does the output fee advantage persist with concentrated ranges?

## Methodology

- Simulated single LP position with configurable range width
- Tested range widths from ±2.5% to ±50% around initial price
- 100 simulations per configuration, 10,000 blocks each
- Price follows GBM with 1% per-block volatility

## Results

### Key Finding: Output Fee Advantage Persists But Is Proportional to Trading Activity

| Range Width | Output Wins | LVR Reduction | Avg In-Range |
|-------------|-------------|---------------|--------------|
| ±2.5% | 71% | ~0% | 8% |
| ±5% | 74% | ~0% | 15% |
| ±10% | 71% | ~0% | 28% |
| ±25% | 65% | ~0% | 53% |
| ±50% | 64% | 1.7% | 73% |

### Interpretation

1. **Output fees still win more simulations** across all range widths (64-74% win rate)
2. **Aggregate LVR reduction scales with in-range time**: Near zero for narrow ranges, 1.7% at ±50%
3. **Explanation**: Concentrated liquidity only earns fees when in range. Narrow ranges are in-range less often → fewer trades → smaller total fee advantage

### Nuanced Finding

The per-trade output fee advantage likely persists, but:
- In narrow ranges: LP out of range most of the time
- Few trades executed → small absolute fee difference
- At wider ranges (more like full-range): effect matches our 6.7-8% constant product results

## Implications

1. **For passive LPs** (wide ranges): Output fees provide meaningful LVR reduction (~8% at full range)
2. **For active LPs** (narrow ranges): Benefit exists but smaller absolute magnitude
3. **For JIT LPs**: Effect likely minimal (only in range for single block)

## Connection to Earlier Theory

This supports the "fee-to-profit ratio" explanation from THEORY.md:
- Output fee advantage depends on capturing fee from arbitrage trades
- With narrow ranges + high volatility → price often out of range → no arb → no fee difference
- Effect is real but proportional to trading volume captured

## Next Steps

1. Analyze per-trade fee difference (not aggregate) to confirm effect persists at trade level
2. Model JIT LP specifically (single-block positions)
3. Consider: Could output fees make narrow ranges more attractive? (hedge against IL direction)
