# Literature Index — Output-Asset AMM Fees

## Key Finding
**No existing research specifically addresses output-asset fees.** All surveyed AMMs and academic papers assume fees are charged on the INPUT asset. This represents a potential research gap.

---

## Categories
- [AMM Fee Mathematics](#amm-fee-mathematics)
- [Dynamic Fee Research](#dynamic-fee-research)
- [AMM Surveys & Foundations](#amm-surveys--foundations)
- [Uniswap v4 Custom Fees](#uniswap-v4-custom-fees)
- [LP Returns & LVR](#lp-returns--lvr)

---

## AMM Fee Mathematics

### A Formal Approach to AMM Fee Mechanisms with Lean 4 (Dessalvi et al., Jan 2026)
- **URL**: https://arxiv.org/abs/2602.00101
- **Key contribution**: Formal Lean 4 proofs of AMM fee properties
- **Relevance**: Proves that with fees, single large swaps > split trades (fee arbitrage)
- **Key insight**: "Fees are charged on a fraction of the assets being SOLD to the AMM"
- **Gap**: Only considers input-based fees

### Axioms for Constant Function Market Makers (2022)
- **URL**: https://arxiv.org/pdf/2210.00048
- **Key contribution**: Axiomatic foundation for CFMMs
- **Relevance**: Proves constant product is trader-optimal among scale-invariant AMMs
- **Gap**: Fee structure not explored in depth

### Axioms for Automated Market Makers (Feb 2025)
- **URL**: https://arxiv.org/html/2210.01227
- **Key contribution**: Mathematical framework for different AMM fee structures
- **Relevance**: "Propose a new fee structure for AMMs which is ambivalent to trade execution"
- **Priority**: HIGH - may discuss alternative fee mechanisms

### Optimal Dynamic Fees in Automated Market Makers (June 2025)
- **URL**: https://arxiv.org/html/2506.02869v1
- **Key contribution**: Determines optimal dynamic fees for CFMMs
- **Relevance**: Framework for fee optimization could extend to output fees

---

## Dynamic Fee Research

### Dynamic Fee Solutions for AMMs (2077 Research, 2024)
- **URL**: https://x.com/2077Research/status/1868782290123514300
- **Key contribution**: Survey of dynamic fee mechanisms
- **Relevance**: Shows fee complexity; no output fee discussion

### Designing Dynamic Fee Policy (CrocSwap, Sep 2022)
- **URL**: https://crocswap.medium.com/designing-a-dynamic-fee-policy-that-outperforms-all-uniswap-eth-usdc-pools
- **Key contribution**: Volatility-based dynamic fees outperform static tiers
- **Relevance**: Framework for comparing fee strategies

### Optimising LP Performance Part 2: Dynamic Fees (Catalyst, Nov 2023)
- **URL**: https://blog.catalyst.exchange/optimising-lp-performance-part-2-dynamic-fees/
- **Key insight**: "AMM pool fees effectively define the bid-ask spread"
- **Relevance**: Understanding fee-spread relationship

---

## AMM Surveys & Foundations

### SoK: DEX with AMM Protocols (Xu et al., 2022)
- **URL**: https://arxiv.org/pdf/2103.12732
- **Key contribution**: Comprehensive AMM systematization
- **Relevance**: Baseline understanding of AMM mechanisms
- **Confirms**: All surveyed AMMs use input-based fees

### An Interdisciplinary Analysis of AMMs (Liu, Jan 2026)
- **URL**: https://medium.com/@gwrx2005/an-interdisciplinary-analysis-of-automated-market-makers
- **Key contribution**: Mechanism design perspective on AMMs
- **Relevance**: Economic framework for analyzing fee structures

---

## Uniswap v4 Custom Fees

### Uniswap v4 Custom Accounting
- **URL**: https://docs.uniswap.org/contracts/v4/guides/custom-accounting
- **Key contribution**: Hook fees allow custom value distribution
- **Relevance**: **Could implement output-based fees via hooks**
- **Priority**: HIGH - implementation pathway

### Uniswap v4 Hooks Overview
- **URL**: https://docs.uniswap.org/contracts/v4/concepts/hooks
- **Key contribution**: Hooks can return deltas affecting swap execution
- **Relevance**: Technical mechanism for custom fee structures

---

## LP Returns & LVR

### ⭐ NEW: Defensive Rebalancing for Automated Market Makers (Herlihy et al., Jan 2026)
- **URL**: https://arxiv.org/abs/2601.19950
- **Key contribution**: Novel LVR mitigation via direct inter-CFMM asset transfers (bypassing trades)
- **Core insight**: Arbitrage-prone configs can be rebalanced to arbitrage-free states, strictly increasing liquidity
- **Key result**: Pareto-efficient configs ⟺ arbitrage-free configs; optimal rebalancing is convex optimization
- **"Mixed rebalancing"**: Participating CFMMs can harvest arbitrage from non-participants/CEXs
- **Relevance**: COMPLEMENTARY approach to our output-fee research — both aim to reduce LVR
- **Priority**: HIGH — compare/contrast with output-fee mechanism
- **Added**: 2026-02-07

### Impermanent Loss and Loss-vs-Rebalancing II (Fritz, Feb 2025)
- **URL**: https://arxiv.org/abs/2502.04097
- **Key contribution**: Statistical relationship between IL and LVR across time regimes
- **Key insight**: Three regimes: (i) short time where LVR≈IL; (ii) intermediate with same expectation; (iii) long-time divergence
- **Relevance**: Framework for understanding how fees interact with block times and arbitrage timing
- **Priority**: HIGH - directly relevant to fee impact analysis

### LVR under Deterministic and Generalized Block-times (Nezlobin & Tassy, May 2025)
- **URL**: https://arxiv.org/abs/2505.05113
- **Key contribution**: Closed-form LVR formula: $\overline{ARB} = \frac{\sigma_b^2}{2 + 1.7164 \cdot \gamma/\sigma_b}$
- **Key insight**: Constant block intervals minimize LVR; formula involves Riemann zeta function
- **Relevance**: **Baseline formula to compare output-fee LVR against**
- **Priority**: CRITICAL - use this formula as benchmark

### Growth Rate of Liquidity Provider's Wealth in G3Ms (Tung et al., Sep 2025)
- **URL**: https://arxiv.org/abs/2403.18177
- **Key contribution**: Extends LP profitability analysis to general Geometric Mean Market Makers (beyond constant product)
- **Methods**: Stochastic reflected diffusion processes under arbitrage-driven markets
- **Key insight**: Long-term expected logarithmic growth of LP wealth derived for G3Ms including Balancer
- **Relevance**: Theoretical framework that could be extended to output-fee analysis
- **Added**: 2026-02-07

### A Derivative Pricing Perspective on Liquidity Tokens (Sep 2024)
- **URL**: https://arxiv.org/html/2409.11339
- **Key contribution**: LP token valuation framework
- **Quote**: "fees are charged on a fraction of the assets being sold to the AMM"
- **Relevance**: Mathematical baseline for comparing fee structures

### The Price of Liquidity: Implied Volatility of AMM Fees (Sep 2025)
- **URL**: https://arxiv.org/html/2509.23222
- **Key contribution**: Expected fees earned by LPs analysis
- **Relevance**: Framework to compare LP returns under different fee models

### Optimal Fees for Liquidity Provision (Aug 2025)
- **URL**: https://arxiv.org/html/2508.08152
- **Key contribution**: Empirical fee optimization
- **Relevance**: Methodology for testing output fee impact

---

## Research Gap Identified

**No existing work explores:**
1. Fees charged on OUTPUT (received) asset instead of INPUT (sold) asset
2. Comparative analysis of LP returns: input-fee vs output-fee
3. Impact on arbitrageur behavior when fees are on output
4. LVR implications of output-based fees
5. Implementation via Uniswap v4 hooks

This gap makes the research novel and potentially valuable.

---

## Next Steps
1. Derive mathematical formulation of output-fee AMM
2. Compare to input-fee under same total fee rate
3. Analyze LP accumulation patterns
4. Model arbitrage dynamics
5. Implement proof-of-concept Uniswap v4 hook
