# Sensitivity Analysis: Output Fees vs Input Fees

**Date:** 2026-02-07  
**Status:** Initial analysis complete

## Summary

Monte Carlo simulations reveal that the LVR advantage of output-asset fees is **regime-dependent**, with the strongest benefits at standard fee levels and moderate volatility.

## Methodology

- 100 simulations per parameter combination
- 10,000 blocks per simulation
- GBM price model
- Arbitrage-driven trading

## Results

### Fee Rate Sensitivity

| Fee Rate | LVR Reduction | Win Rate |
|----------|---------------|----------|
| 0.1%     | 0.3%          | 100%     |
| 0.3%     | **8.2%**      | 100%     |
| 0.5%     | -2.0%         | 100%     |
| 1.0%     | -1.1%         | 77%      |

**Insight:** Output fees work best at the standard 0.3% fee level. At higher fees, the benefit disappears or reverses.

### Volatility Sensitivity

| Block σ | LVR Reduction | Win Rate |
|---------|---------------|----------|
| 0.5%    | -0.6%         | 93%      |
| 1.0%    | **8.2%**      | 100%     |
| 2.0%    | 2.1%          | 100%     |
| 3.0%    | 3.6%          | 100%     |

**Insight:** Moderate volatility (~1% per block) shows strongest benefit. Effect persists but diminishes at higher volatility.

## Interpretation

### Why Regime-Dependent?

1. **At very low fees:** Minimal fee revenue in either case, so difference is negligible.

2. **At high fees:** The fee itself becomes a larger fraction of trade value, changing arbitrage dynamics. The "output tax on profit" effect is diluted.

3. **At low volatility:** Fewer arbitrage opportunities, less LVR to mitigate.

4. **At high volatility:** Large price movements dominate; the subtle output vs input fee difference matters less.

### Optimal Regime

The "sweet spot" appears to be:
- Fee rate: ~0.3% (standard Uniswap)
- Volatility: ~1% per block
- This matches typical ETH/stablecoin pool conditions

## Implications

1. **Implementation target:** Focus on pools with standard 0.3% fees

2. **Market fit:** Best suited for:
   - Major pairs (ETH/USDC, ETH/USDT)
   - Normal market conditions
   - Pools with active arbitrage flow

3. **Not ideal for:**
   - Exotic pairs with high fees
   - Stablecoin/stablecoin pairs (low vol)
   - Meme coins (extreme vol)

## Next Steps

1. Validate with historical data from Uniswap ETH/USDC
2. Investigate theoretical explanation for regime dependence
3. Consider adaptive output fee rates based on volatility

## Raw Data

See: `experiments/simulations/sensitivity_results.json` (TODO: save)
