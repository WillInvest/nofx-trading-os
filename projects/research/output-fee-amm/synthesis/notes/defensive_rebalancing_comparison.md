# Comparison: Output Fees vs Defensive Rebalancing for LVR Mitigation

*Date: 2026-02-07*

## Overview

Two complementary approaches to reducing Loss-Versus-Rebalancing (LVR) in AMMs:

1. **Output Fees** (our research): Charge fees on the output asset instead of input
2. **Defensive Rebalancing** (Herlihy et al. 2026): Direct inter-CFMM asset transfers to arbitrage-free states

## Mechanism Comparison

| Aspect | Output Fees | Defensive Rebalancing |
|--------|-------------|----------------------|
| **Core idea** | Tax arbitrageur profits directly | Rebalance pools without trading |
| **LVR reduction** | ~6.7% (simulated) | Theoretically eliminates LVR between participating pools |
| **Requires** | Single pool modification | Network of cooperating CFMMs |
| **Complexity** | Simple hook | Coordination mechanism needed |
| **Trade-offs** | Slightly worse trader UX | Requires pool operator cooperation |

## Defensive Rebalancing Deep Dive

From arXiv:2601.19950 (Herlihy et al.):

### Key Concepts
- **Arbitrage-prone**: A configuration where some CFMM can be profitably arbitraged
- **Arbitrage-free**: No CFMM can be profitably arbitraged in isolation
- **Defensive rebalancing**: Direct asset transfers between CFMMs to reach arbitrage-free state

### Main Results
1. **Pareto-efficiency ⟺ Arbitrage-free**: Optimal configurations for LPs are exactly the arbitrage-free ones
2. **Convex optimization**: Finding the optimal rebalance is a convex problem
3. **"Mixed rebalancing"**: Participating CFMMs can harvest arbitrage from non-participants

### Limitations
- Requires multiple cooperating CFMMs
- May not be feasible for isolated pools
- Complex coordination mechanism

## Output Fees: Complementary Approach

### Strengths vs Defensive Rebalancing
1. **Works for single pools**: No coordination needed
2. **Simple implementation**: Uniswap v4 hook
3. **Always-on**: Every swap benefits, not just rebalancing events
4. **Backward compatible**: Doesn't require protocol changes

### Weaknesses vs Defensive Rebalancing
1. **Partial mitigation**: ~6.7% LVR reduction vs potential elimination
2. **Regime-dependent**: Best at 0.3% fee, moderate volatility
3. **Doesn't address root cause**: Arbitrageurs still extract value

## Potential Combination

**Hypothesis**: Output fees + Defensive rebalancing could be synergistic:

1. **Output fees** reduce LVR from external arbitrage (CEX-DEX)
2. **Defensive rebalancing** eliminates LVR between participating DEX pools
3. Combined: Near-complete LVR mitigation

### Implementation Sketch
```
Pool with OutputFeeHook:
  - External trades: Output fee reduces LVR ~6.7%
  - Inter-pool rebalancing: No arbitrage needed (defensive rebalancing)
  
Result: LPs benefit from both mechanisms
```

## Research Questions

1. **Quantitative**: How much LVR remains when both mechanisms are active?
2. **Game theory**: Does output fee affect incentive to participate in defensive rebalancing?
3. **Implementation**: Can a single hook implement both?

## Conclusion

Output fees and defensive rebalancing are **complementary**, not competing approaches:
- **Output fees**: Simple, single-pool, partial mitigation
- **Defensive rebalancing**: Complex, multi-pool, stronger mitigation

For maximum LP protection, consider both.

## References

- Herlihy et al. "Defensive Rebalancing for Automated Market Makers" (arXiv:2601.19950, Jan 2026)
- Our simulation results: `experiments/simulations/amm_fee_comparison.py`
