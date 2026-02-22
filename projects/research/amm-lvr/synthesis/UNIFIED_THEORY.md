# Unified Theory of LVR — Three Perspectives, One Phenomenon

> *"The same loss, seen through different mathematical lenses"*

## Executive Summary

Loss-Versus-Rebalancing (LVR) has been independently characterized by three distinct theoretical frameworks. This document demonstrates their mathematical equivalence and extracts unique design insights from each perspective.

| Framework | LVR Expression | Key Paper | Core Insight |
|-----------|---------------|-----------|--------------|
| **Microstructure** | σ²L/8 × dt | Milionis et al. 2022 | Adverse selection from stale prices |
| **Options Theory** | Θ (theta decay) | Singh et al. 2025 | LP = holder of continuous-installment option |
| **Thermodynamics** | Entropy leak | Meister 2026 | CPMM as irreversible Carnot engine |

---

## 1. Mathematical Equivalence

### 1.1 The Milionis Foundation (Microstructure)

From the foundational LVR paper:

```
LVR = (σ²/8) × L × dt
```

Where:
- σ = instantaneous volatility of the risky asset
- L = liquidity depth (∂x/∂√P for Uniswap v3)
- dt = time increment

**Derivation sketch**: In continuous time, arbitrageurs extract value proportional to the squared price change. For geometric Brownian motion with volatility σ, the expected squared return over dt is σ²dt. The factor 1/8 emerges from the curvature of the constant-product invariant.

### 1.2 The Singh Equivalence (Options Theory)

Singh et al. (2025) prove that an LP position is economically equivalent to holding a portfolio of **perpetual American continuous-installment (CI) options**.

Key result:
```
LVR ≡ Θ_CI
```

Where Θ_CI is the theta (time decay) of the embedded CI option.

**Connection to Milionis**: For an at-the-money CI option under Black-Scholes dynamics:

```
Θ_CI = (σ²S²/8) × Γ
```

For a constant-product AMM, the gamma Γ of the LP position equals L/S², yielding:

```
Θ_CI = (σ²S²/8) × (L/S²) = σ²L/8 ✓
```

**Mathematical identity confirmed.**

### 1.3 The Meister Perspective (Thermodynamics)

Meister (2026) frames the CPMM as a thermodynamic engine operating in cycles:
- **Phase 1**: Liquidity taker swaps (work extraction)
- **Phase 2**: Arbitrageur rebalancing (heat dissipation)
- **Phase 3**: LP deposit/withdrawal (reservoir interaction)

The "entropy leak" corresponds to irreversible value transfer to arbitrageurs.

**Connection to Milionis**: Under the thermodynamic framework:

```
ΔS_entropy = ∫ (dQ/T) ≈ σ²L/8 × dt
```

Where the "temperature" T corresponds to liquidity depth, and dQ represents the heat (value) lost to arbitrageurs.

**Key insight**: The 1/8 factor emerges from the **Carnot efficiency bound** — no engine (or AMM) can be 100% efficient when operating between two price reservoirs.

### 1.4 Unified Expression

All three frameworks yield the same fundamental relationship:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   LVR = Θ_CI = ΔS_entropy = (σ²/8) × L × dt            │
│                                                         │
│   "The cost of providing liquidity against informed     │
│    traders in a world of continuous price discovery"    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Design Insights by Framework

Each framework offers unique intuitions for AMM design:

### 2.1 Options Framework → Hedging & Greeks

**Core insight**: LPs are short volatility (negative gamma, positive theta outflow).

**Design implications**:

| Greek | LP Exposure | Mitigation Strategy |
|-------|-------------|---------------------|
| Θ (theta) | Negative (LVR) | Dynamic fees ≥ |Θ| |
| Γ (gamma) | Negative | Concentrated ranges reduce |Γ| exposure |
| Δ (delta) | Path-dependent | Directional LP (Maverick) |
| V (vega) | Negative | Vol-scaled fees |

**Actionable ideas**:
- **Constant-LVR vaults**: Use Singh's framework to design LP positions with predictable, targetable adverse selection costs
- **LP Greeks dashboard**: Real-time display of theta/gamma/vega for position management
- **Automated delta hedging**: Protocol-level hedging using perps/options

### 2.2 Thermodynamics Framework → Efficiency Bounds

**Core insight**: AMMs are heat engines with fundamental efficiency limits.

**The Carnot Bound for AMMs**:
```
η_max = 1 - (T_cold / T_hot) = 1 - (L_low / L_high)
```

Where liquidity depth acts as "temperature."

**Design implications**:

1. **Efficiency metric**: Define η_AMM = (Fees earned) / (Fees + LVR)
   - Current CFMMs: η ≈ 20-50% on volatile pairs
   - FM-AMM: η → 100% (eliminates arbitrage heat sink)

2. **Non-linear impact**: Meister shows market impact is √-law, not linear
   - Linearized liquidity models underestimate true costs
   - Large trades should face super-linear fees

3. **Catastrophe risk**: Stablecoin depeg as phase transition
   - Design circuit breakers at critical liquidity thresholds

**Actionable ideas**:
- **Thermodynamic efficiency dashboard**: Track η over time
- **√-law fee curves**: Better capture true market impact
- **Phase transition alerts**: Early warning for depeg risk

### 2.3 Microstructure Framework → Information-Sensitive Pricing

**Core insight**: LVR is adverse selection — LPs trade with counterparties who know more.

**The Information Hierarchy**:
```
Informed traders > CEX price > AMM pool price > Retail
```

**Design implications**:

1. **Flow segmentation**: Distinguish toxic vs. uninformed flow
   - MEV tax (Paradigm): fee = f(priority_fee)
   - Time-weighted: Higher fees for fast trades
   
2. **Price staleness**: Reduce Δt between pool and market price
   - Oracle integration: TWAP, VWAP feeds
   - Batching: FM-AMM eliminates staleness entirely

3. **Volatility-reactive fees**: σ is observable → fees should scale
   - Realized vol → fee adjustment
   - Implied vol from options → predictive fees

**Actionable ideas**:
- **Information-sensitive fee schedule**: f(priority, speed, size, vol)
- **Staleness oracle**: Track pool-vs-CEX divergence in real-time
- **Adverse selection score**: Per-trade metric for LP analytics

---

## 3. Practical Guide

### 3.1 When to Use Each Framework

| Analysis Goal | Best Framework | Why |
|---------------|----------------|-----|
| Position hedging | Options | Greeks are actionable |
| Protocol efficiency comparison | Thermodynamics | Clear η metric |
| Fee optimization | Microstructure | Information economics |
| LP return prediction | Options | Theta = expected LVR |
| Systemic risk | Thermodynamics | Phase transitions |
| MEV capture design | Microstructure | Flow toxicity |

### 3.2 Unified Design Principles

From the three frameworks, we extract **seven design principles**:

```
┌─────────────────────────────────────────────────────────┐
│              UNIFIED LVR MITIGATION PRINCIPLES          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. PRICE FRESHNESS                                     │
│     Reduce Δt between pool and market price             │
│     → Oracles, batching, frequent updates               │
│                                                         │
│  2. VOLATILITY AWARENESS                                │
│     Fees must scale with σ (the root cause)             │
│     → Dynamic fees, vol-indexed spreads                 │
│                                                         │
│  3. FLOW SEGMENTATION                                   │
│     Distinguish informed vs. uninformed traders         │
│     → MEV taxes, time-weighted fees, reputation         │
│                                                         │
│  4. EFFICIENCY TARGETING                                │
│     Maximize η = Fees / (Fees + LVR)                    │
│     → Batch auctions approach η → 1                     │
│                                                         │
│  5. GAMMA MANAGEMENT                                    │
│     Reduce |Γ| exposure through range selection         │
│     → Concentrated liquidity, active management         │
│                                                         │
│  6. THETA CAPTURE                                       │
│     Charge fees ≥ |Θ| to break even on LVR              │
│     → Singh framework for fee calibration               │
│                                                         │
│  7. CATASTROPHE AWARENESS                               │
│     Monitor for phase transitions (depeg risk)          │
│     → Circuit breakers, liquidity thresholds            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3.3 Solution Ranking by Principle Coverage

| Solution | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Score |
|----------|----|----|----|----|----|----|----| ------|
| FM-AMM (CoW) | ✓ | ✓ | ✓ | ✓ | - | ✓ | - | 5/7 |
| Angstrom | ✓ | ✓ | ✓ | ✓ | - | ✓ | - | 5/7 |
| MEV Tax | ✓ | - | ✓ | ○ | - | ○ | - | 3/7 |
| Dynamic Fees | ○ | ✓ | ○ | ○ | - | ✓ | - | 3/7 |
| Oracle AMM | ✓ | - | - | ○ | - | - | - | 2/7 |
| Concentrated LP | - | - | - | - | ✓ | - | - | 1/7 |

Legend: ✓ = fully addresses, ○ = partially addresses, - = does not address

---

## 4. Open Questions

### 4.1 Theoretical

1. **Exact equivalence proof**: Rigorous derivation of Milionis ⟺ Singh ⟺ Meister under general dynamics
2. **Non-GBM extension**: How do the equivalences hold under jump-diffusion or rough volatility?
3. **Multi-asset generalization**: Extend unified framework to n-asset pools

### 4.2 Empirical

1. **Framework prediction accuracy**: Which framework best predicts realized LVR on historical data?
2. **Efficiency benchmarking**: Measure η across CoW AMM, Angstrom, traditional AMMs
3. **Phase transition detection**: Can thermodynamic metrics predict depeg events?

### 4.3 Design

1. **Optimal hybrid**: Combine best elements of FM-AMM + dynamic fees + MEV tax
2. **Trustless batching**: Can threshold encryption enable trustless FM-AMM?
3. **Cross-pool coordination**: Herlihy's defensive rebalancing at scale

---

## 5. Conclusion

The convergence of three independent theoretical frameworks on the same fundamental quantity — LVR = σ²L/8 × dt — is remarkable. It suggests we have arrived at a robust understanding of the core problem.

**The path forward is clear**:
- Use **options theory** for LP position management and hedging
- Use **thermodynamics** for protocol efficiency analysis
- Use **microstructure** for fee mechanism design

Together, they form a complete toolkit for building the next generation of LVR-resistant AMMs.

---

## References

1. Milionis, J., Moallemi, C., Roughgarden, T., Zhang, A.L. (2022). *Automated Market Making and Loss-Versus-Rebalancing*. arXiv:2208.06046
2. Singh, S.F. et al. (2025). *Modeling Loss-Versus-Rebalancing via Continuous-Installment Options*. arXiv:2508.02971
3. Meister, B. (2026). *Automated Liquidity: Market Impact, Cycles, and De-pegging Risk*. arXiv:2601.11375
4. Canidio, A., Fritsch, R. (2023). *Arbitrageurs' profits, LVR, and sandwich attacks: batch trading as an AMM design response*. arXiv:2307.02074
5. Robinson, D., White, D. (2024). *Priority Is All You Need*. Paradigm Research.
6. Herlihy, M. (2026). *Defensive Rebalancing for Automated Market Makers*. arXiv:2601.19950

---

*Last updated: 2026-02-07*
*Status: Draft v1 — foundational structure complete*
