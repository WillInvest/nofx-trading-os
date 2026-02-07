# THEORY.md — Extending One-Step to Long-Term Fee Analysis

## Overview

Most AMM fee literature focuses on one-step (instantaneous) analysis. This document tracks theoretical approaches for extending to **long-term fee revenue estimation**.

---

## Key Long-Term Analysis Framework

### 1. Tassy-White (2020) — Foundation
**Paper**: "Growth Rate of LP Wealth in XY=C Automated Market Makers"
- **Key Innovation**: Computes **asymptotic logarithmic growth rate** of LP wealth
- **Method**: Models LP-arbitrageur game as Markov chain on finite state space
- **Key Formula**: `lim(T→∞) (1/T) E[log W_T]` — expected long-run log growth of wealth
- **Key Finding**: Under GBM prices with fee γ, LP wealth has deterministic long-term growth rate depending on fee level, volatility, and drift

### 2. Tung et al. (2024) — G3M Extension (arXiv:2403.18177) ⭐ CRITICAL
**Key Extension**: Uses **stochastic reflected diffusion processes** to model continuous-time G3M dynamics
- Extends Tassy-White from CPMM (Uniswap v2) to general G3Ms (Balancer, etc.)
- Computes **long-term expected logarithmic growth** of LP wealth
- Incorporates both fees AND continuous-time arbitrage
- **Key Insight**: The reflection boundary conditions model the no-arbitrage zone naturally

### 3. Evans et al. (2021) — Optimal Fees for G3Ms (arXiv:2104.00446)
**Framework**: General diffusion price processes
- Shows how to select **optimal fees** for maximizing LP value over time
- Key result: LP with mean-variance utility prefers G3M as fees → 0
- Extends to general LP objective functions

---

## Three Time Regimes (Fritz et al., 2025 — arXiv:2502.04097)

Critical finding for long-term analysis:

| Regime | Time Scale | IL vs LVR Relationship |
|--------|------------|------------------------|
| **Short** | Infinitesimal | IL ≡ LVR (identical) |
| **Intermediate** | Moderate | Same expectation, different distributions (CLT applies) |
| **Long** | Extended | Different expectations AND distributions |

**Implication**: One-step analysis (σ²/8 for LVR) does NOT extrapolate linearly to long horizons!

---

## From One-Step to Long-Term: Key Relationships

### One-Step Analysis (Most Papers)
- **LVR per unit time**: E[LVR] = σ²L/8 (where L = liquidity, σ = volatility)
- **Fee income per trade**: γ × trade_volume
- **Net**: Fee_income - LVR

### Long-Term Challenges

1. **Non-linear Accumulation**: Fees compound, but so do losses
2. **Path Dependence**: Final wealth depends on sequence of price movements
3. **Regime Changes**: Volatility, volume, and price drift change over time
4. **Compounding Effects**: 
   - Fee reinvestment (if auto-compounding)
   - IL recovery vs permanent divergence

### Tassy-White Approach
Models as **discrete Markov chain**:
- States: Price ratio relative to LP ratio (within no-arb zone)
- Transitions: Price moves + trades when crossing fee boundary
- Stationary distribution → long-run expected growth

**Key Insight**: The product X_t × Y_t grows by factor C^n after n trades:
```
C = exp(δ × (1-γ)/(1+γ))
```
where δ = price step size, γ = fee rate

### Stationary Distribution Approach — Milionis et al. (2023/2025)
**Paper**: arXiv:2305.14604

Proves that with fees + discrete Poisson block times:
- **Process is ergodic** → unique stationary distribution exists
- Long-term expected arbitrage profits computable in closed form
- **Key practical insight**: Faster blockchains → reduced LP losses

This provides the mathematical foundation connecting:
- Instantaneous LVR (σ²L/8)
- Block-discrete reality
- Long-term stationary expected loss rates

---

## Open Questions for Long-Term Fee Estimation

1. **Optimal Horizon Length**: How long must an LP commit to expect positive returns?

2. **Break-Even Fee Levels**: Given volatility σ, what fee γ makes E[log W_T] > 0?

3. **Risk-Adjusted Returns**: Sharpe ratio or similar for LP positions over time

4. **Volume Sustainability**: Do fees from volume offset LVR persistently?

5. **Regime-Dependent Models**: How to incorporate changing market conditions?

---

## Continuous-Time Subtlety (Tung et al., 2024 — arXiv:2412.18580)

**Critical Finding**: Fees preclude diffusion terms in continuous-time price processes!
- If price is continuous diffusion → fees would be infinite (quadratic variation)
- Real AMM prices must have **jumps** or discrete updates
- Implication: Pure GBM models are approximations; block-time effects matter

---

## Recommended Modeling Approach

For long-term fee estimation, combine:

1. **Tassy-White Markov Framework** for log-growth computation
2. **LVR σ²/8 Formula** for short-horizon intuition  
3. **Fritz et al. Regime Analysis** for understanding time-scale effects
4. **Bergault et al. Optimal Stopping** for finite-horizon with exit option ⭐ NEW
5. **Empirical Calibration** from real LP data (51% unprofitable per Bancor study)

### Proposed Long-Term Model Structure
```
LP_Wealth(T) = Initial × exp(∫₀ᵀ μ_LP(t) dt + stochastic_term)

where μ_LP(t) ≈ fee_yield(t) - LVR_rate(t)
            ≈ γ × volume_rate(t) / liquidity(t) - σ(t)² L(t) / 8
```

But this linear model breaks down at long horizons — need Markov chain or reflected diffusion approach.

---

## NEW: Optimal Stopping Framework (Bergault et al., 2025) ⭐

**Paper**: arxiv:2509.06510 — "Optimal Exit Time for Liquidity Providers in AMMs"

### Key Innovation
Models LP withdrawal as **optimal stopping problem** rather than fixed-horizon analysis:
- LP continuously decides: "Should I exit now or continue?"
- Value function satisfies Hamilton-Jacobi-Bellman quasi-variational inequality
- Captures the real-world LP decision process

### Mathematical Framework
```
V(x) = sup_τ E[ ∫₀^τ (fee_rate - IL_rate) dt + exit_value(τ) ]

where τ is the stopping (exit) time
```

### Key Findings for Long-Term Analysis

1. **Optimal Exit Depends On**:
   - Oracle price volatility (higher σ → earlier exit)
   - Fee levels (higher fees → stay longer)
   - Arbitrageur vs noise trader mix (more arb → higher IL → earlier exit)
   - Pool state variables and price misalignment

2. **Optimal Fee Discovery**:
   - Given optimal exit strategy, paper derives optimal fee level
   - First paper to jointly optimize BOTH exit time AND fee level

3. **Sustainability Insight**:
   - Under some regimes, passive LP strategies are sustainable
   - Under others, active management (optimal exit) is required for profitability

### Bridge: One-Step → Finite Horizon → Infinite Horizon

| Framework | Horizon | Key Question | Method |
|-----------|---------|--------------|--------|
| One-step (LVR) | Instantaneous | What's the loss rate now? | σ²L/8 |
| Optimal Stopping (Bergault) | Finite + exit option | When should I exit? | HJB equation |
| Log-Growth (Tassy-White, Tung) | Infinite, no exit | What's my asymptotic growth? | Markov chain |

**Key Insight**: The three frameworks are complementary layers of long-term analysis!

---

## Synthesis: Unified Long-Term Fee Framework

### Step 1: One-Step Foundation
- LVR = σ²L/8 per unit time
- Fee income = γ × volume_rate / liquidity

### Step 2: Time Regime Awareness (Fritz)
- Short/medium/long horizons have different IL/LVR relationships
- Cannot simply multiply one-step by time T

### Step 3: Optimal Stopping Layer (Bergault)
- LP can exit at any time
- Optimal exit time τ* balances fee accumulation vs IL risk
- Provides finite-horizon expected return

### Step 4: Asymptotic Growth (Tassy-White, Tung)
- If LP commits forever: log-growth rate calculable via Markov chain
- Provides break-even fee conditions for infinite horizon

### Step 5: Empirical Calibration
- 51% of LPs unprofitable (real-world validation)
- Compare theoretical predictions to actual outcomes

---

## Next Steps

1. [ ] Deep-read Tung et al. (2403.18177) for explicit growth rate formula
2. [ ] Deep-read Bergault et al. (2509.06510) for optimal stopping framework ⭐ NEW
3. [ ] Derive conditions for positive long-term LP return
4. [ ] Compare theoretical predictions to empirical LP data
5. [ ] Model fee compounding effects explicitly
6. [ ] Investigate block-time impact on fee accumulation
7. [ ] Build unified model combining optimal stopping + log-growth rate ⭐ NEW

---

## NEW: Infinite-Horizon Utility Maximization (Yang et al., 2024) ⭐

**Paper**: arxiv:2404.13291 — "Optimal Design of AMMs on Decentralized Exchanges"

### Key Innovation
First paper to model LP as **risk-averse agent maximizing discounted infinite-horizon utility**:
- LP allocates wealth between: DEX liquidity provision, CEX trading, risk-free asset
- Consumption in each period
- Maximizes `E[∑_{t=0}^∞ β^t u(c_t)]` where β = discount factor

### Key Long-Term Findings

1. **Optimal Fee Scales with Volatility**:
   - Higher volatility → higher optimal trading fee
   - Intuition: Must compensate LP for increased IL/LVR exposure
   
2. **Optimal Pricing Function**:
   - AMM should choose pricing function that makes asset allocation **efficient for LP**
   - Joint optimization of mechanism design + LP strategy

3. **Cross-Market Effects**:
   - LP's CEX activity affects optimal DEX provision
   - Cannot analyze LP profits in isolation

### Contribution to Long-Term Framework

This provides the **fourth layer** of analysis:

| Layer | Framework | Horizon | LP Behavior |
|-------|-----------|---------|-------------|
| 1 | LVR | Instant | Static |
| 2 | Optimal Stopping (Bergault) | Finite + exit | Active exit timing |
| 3 | Log-Growth (Tassy-White) | Infinite, no exit | Passive forever |
| **4** | **Utility Optimization (Yang)** | **Infinite + consumption** | **Active allocation + consumption** |

### Implication for Break-Even Analysis
The Yang framework suggests LP should:
- Set fees proportional to volatility
- Dynamically rebalance across DEX/CEX
- Consume some profits rather than fully reinvesting

This is more realistic than passive log-growth assumptions.

---

## Active Rebalancing Trap: Exponential Decay (NEW — Feb 2026) ⭐⭐

**Paper**: arxiv:2501.12583 — "Chasing Price Drains Liquidity" (Jan 2025)

### Critical Finding for Long-Term LP Strategy

**Theorem**: Under GBM price dynamics in Uniswap v3 CLMMs, the strategy of adjusting liquidity position to track the current price leads to **deterministic and exponentially fast decay** of liquidity.

### Mathematical Result
```
L(t) ~ L(0) × exp(-λ × t)

where λ > 0 depends on volatility and repositioning parameters
```

### Why This Matters for Long-Term Fees

1. **Active Management Paradox**:
   - Intuition: "Concentrate liquidity near current price for more fees"
   - Reality: Repositioning costs compound exponentially over time
   - Long-term result: Liquidity depletes to zero!

2. **Hidden Costs of Rebalancing**:
   - Each reposition loses value to arbitrageurs
   - Losses compound multiplicatively, not additively
   - Fee income cannot offset exponential decay

3. **Optimal Long-Term Strategy Implications**:
   - Wide passive ranges may preserve wealth better than concentrated active strategies
   - "Set and forget" strategies have mathematical advantages
   - Concentrated liquidity (v3 style) requires very careful rebalancing

### Connection to Time Regimes (Fritz)
This result explains WHY long-horizon IL/LVR differs from short-horizon:
- Short: Each rebalance has small loss
- Long: Losses compound exponentially
- The Fritz "different means in long regime" may partially reflect this

### Connection to Optimal Stopping (Bergault)
The optimal exit time framework becomes even more important:
- If staying means exponential decay, early exit may be optimal
- Fee accumulation must outpace decay rate for positive returns
- Reinforces need for dynamic exit analysis

---

## Competitive Dynamics: JIT LP Effects (NEW)

**Paper**: arxiv:2509.16157 — "Strategic Analysis of JIT Liquidity in CLMMs"

### Why This Matters for Long-Term Fees

JIT (Just-In-Time) LPs are strategic agents who:
- Provide liquidity for **single trades only**
- Capture disproportionate fees relative to capital committed
- Erode passive LP returns by up to **44% per trade**

### Long-Term Implications

1. **Adverse Selection Intensifies Over Time**:
   - Passive LPs face competition from JIT LPs
   - Fee share captured by passive LPs declines
   - Long-term profitability harder than theoretical models suggest

2. **Market Efficiency Trade-off**:
   - JIT LPs reduce slippage for traders
   - But reduce returns for passive LPs
   - Equilibrium fee levels may need to increase

3. **Implication for Tassy-White Model**:
   - Original model assumes homogeneous LPs
   - With JIT competition, need to model LP types separately
   - Expected long-term growth differs by LP type

---

## Updated Synthesis: Five-Layer Long-Term Framework

For comprehensive long-term fee revenue estimation:

### Layer 1: Instantaneous (σ²L/8)
- Baseline loss rate
- Valid for infinitesimal horizons only

### Layer 2: Time-Regime Awareness (Fritz)
- Short/medium/long have different IL/LVR relationships
- Non-linear extrapolation required

### Layer 3: Optimal Stopping (Bergault)
- When to exit?
- Finite-horizon expected return with endogenous exit

### Layer 4: Asymptotic Log-Growth (Tassy-White, Tung)
- Infinite-horizon committed LP
- Markov chain/reflected diffusion approach

### Layer 5: Utility Optimization (Yang)
- Risk-averse LP with consumption
- Cross-market (DEX/CEX) allocation
- Most realistic model of LP behavior

### Modifying Factors
- **JIT Competition**: Reduces passive LP fee share
- **Block-time Effects**: Discretization matters (Tung)
- **Volatility Regime Changes**: Non-stationary dynamics
- **Rebalancing Decay** ⭐ NEW: Active repositioning causes exponential liquidity decay (Cao et al.)

---

## Remaining Research Gaps

1. **Unified Closed-Form**: No single formula for long-term expected return
2. **Regime-Switching Models**: How to handle changing volatility/volume?
3. **LP Type Heterogeneity**: Passive vs JIT vs active rebalancers
4. **Empirical Validation**: Connect theoretical models to 51% unprofitable observation
5. **Fee Reinvestment**: Most models assume no compounding; reality differs
6. **Optimal Repositioning Frequency** ⭐ NEW: Given exponential decay from rebalancing, what is the optimal repositioning strategy?

---

## NEW: Perpetual Option Framework (Singh et al., Aug 2025) ⭐⭐

**Paper**: arxiv:2508.02971 — "Modeling LVR via Continuous-Installment Options"

### Key Breakthrough for Long-Term Analysis

This paper provides the first **infinite time horizon** option-theoretic framework for AMM positions:

1. **Models AMM as Perpetual Option Portfolio**:
   - CFAMM position = portfolio of perpetual American continuous-installment (CI) options
   - Replicates LP delta at each point over infinite time horizon
   - Captures perpetual nature of LP positions (no fixed expiry)

2. **Fundamental Equivalence Result**:
   ```
   LVR ≡ θ (theta) of at-the-money CI option
   ```
   - LVR is analytically identical to time decay of the embedded option
   - This connects AMM adverse selection directly to options pricing theory
   - Enables use of established option mathematics for LP analysis

3. **Constant LVR Derivation**:
   - Derives LP profile with **approximately constant LVR** over arbitrarily long forward window
   - Bounded residual error
   - Practical framework for estimating future adverse-selection costs

4. **Practical Implications**:
   - Volatility calibration from term structure of implied vols
   - Error bounds for both IV calibration and LVR residual
   - Actionable guidance for LP position parameter optimization

### Integration with Unified Framework

| Layer | Framework | Connection to Perpetual Option |
|-------|-----------|-------------------------------|
| 1 | One-step (LVR) | LVR = θ of ATM CI option |
| 2 | Time-Regimes (Fritz) | Different θ profiles across horizons |
| 3 | Optimal Stopping (Bergault) | Exit = exercise of CI option |
| 4 | Log-Growth (Tassy-White) | Infinite θ accumulation → asymptotic growth |
| 5 | Utility Optimization (Yang) | Portfolio of options + consumption |
| 6 | Rebalancing Decay (Cao) | Repositioning = buying new option positions |

**This is a major unifying result**: The perpetual option interpretation provides a single mathematical object (the CI option) that connects instantaneous LVR to infinite-horizon analysis.

---

## Key Takeaway for Practitioners (Feb 2026)

**Three game-changing results for long-term LP strategy**:

1. **"Chasing price" causes exponential decay** (arxiv:2501.12583):
   - Price-tracking strategies → L(t) ~ L(0)×exp(-λt)
   - Active management has hidden compounding costs

2. **LVR = Option Theta** (arxiv:2508.02971):
   - AMM position behaves like perpetual option portfolio
   - Enables mature options mathematics for LP analysis
   - Can derive constant-LVR profiles for extended horizons

3. **Optimal fee scales with volatility** (Yang 2024, validated by SSRN 4591447):
   - Adaptive fees outperform fixed by 9-44% annually
   - LP should demand higher fees in volatile regimes

**Combined implication**: For long-term profitability, LPs should:
- Use wide passive ranges (avoid price-chasing)
- Select pools with volatility-adaptive fees
- Consider optimal exit timing (Bergault framework)
- Calibrate expected LVR from options market (Singh framework)

---

*Last updated: 2026-02-07 (added perpetual CI option framework from arxiv:2508.02971)*
