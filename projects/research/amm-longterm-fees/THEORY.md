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

## Fritz et al. Two-Part Analysis (2024-2025) ⭐⭐

### Part I: Statistical Properties (arXiv:2410.00854, Oct 2024)
**Key Finding**: For Brownian motion with a given volatility:
- IL and LVR have **identical expectation values**
- BUT **vastly different distribution functions**

This establishes that while E[IL] = E[LVR], the risk profiles differ significantly. The distributions have different variances, skewness, and tail behavior.

### Part II: Three Time Regimes (arXiv:2502.04097, Feb 2025)

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

## NEW: Equilibrium Convergence Framework (Gogol et al., 2024/2025) ⭐

**Paper**: arxiv:2410.10324 — "Liquidity Fragmentation or Optimization?"

### Key Insight for Long-Term Fees

This paper provides a fundamental **equilibrium bound** for long-term LP returns:

**In equilibrium, AMM LP returns converge to the staking (reference) rate.**

### Mathematical Implication

Over the long run:
```
E[LP_return] → staking_rate (in equilibrium)
```

This suggests:
1. LP profits above staking are competed away over time
2. LP profits below staking cause capital outflow until rates equalize
3. **Long-term fee revenue = just enough to match staking after LVR**

### Why This Matters

This provides an **upper bound** for sustainable long-term LP returns:
- If `fee_revenue - LVR > staking_rate`, capital floods in, returns fall
- If `fee_revenue - LVR < staking_rate`, capital exits, returns rise
- Equilibrium: `fee_revenue - LVR ≈ staking_rate`

### Empirical Findings
- Ethereum L1 pools are **oversubscribed** (too much capital chasing fees)
- L1 pool returns often **below staking** (already past equilibrium)
- L2 pools offer better risk-adjusted returns (under-subscribed)

### Connection to Other Frameworks

| Framework | Horizon | Bound Type |
|-----------|---------|------------|
| LVR (σ²L/8) | Instant | Lower bound on loss rate |
| Tassy-White | Infinite | Asymptotic log-growth rate |
| **Gogol et al.** | **Equilibrium** | **Convergence target = staking** |

---

## NEW: Mean Field Games Approach (Muñoz Gonzalez et al., 2024) 

**Paper**: arxiv:2412.09180 — "Liquidity Pools as Mean Field Games"

### Contribution to Long-Term Analysis

Mean field games (MFG) provide a framework for:
- Modeling many interacting LPs
- Finding equilibrium strategies
- Understanding long-run market structure

### Why This Matters

The MFG approach:
1. Proves existence of equilibrium solutions
2. Shows approximate Nash equilibria exist
3. Extends traditional order-book MFG to AMM context

### Long-Term Implication

With many strategic LPs over long horizons:
- Market reaches mean-field equilibrium
- Individual LP returns converge to population average
- Outlier strategies get competed away

---

## Unified Long-Term Framework: EIGHT Layers (Updated Feb 2026)

| Layer | Framework | Horizon | Key Question | Key Formula/Insight |
|-------|-----------|---------|--------------|---------------------|
| 1 | LVR | Instant | Loss rate now? | σ²L/8 |
| 2 | Time-Regimes (Fritz) | Short/Med/Long | How does IL/LVR scale? | Non-linear! |
| 3 | Optimal Stopping (Bergault) | Finite + exit | When to exit? | HJB equation |
| 4 | Log-Growth (Tassy-White) | Infinite passive | Asymptotic growth? | Markov chain |
| 5 | Utility Optimization (Yang) | Infinite + consumption | Optimal allocation? | Risk-averse utility |
| 6 | Rebalancing Decay (Cao) | Long, active | Cost of repositioning? | exp(-λt) decay |
| 7 | Perpetual Option (Singh) | Infinite | LVR via options? | LVR = θ of CI option |
| **8** | **Equilibrium Convergence (Gogol)** | **Long-run equilibrium** | **What's the target?** | **Converges to staking rate** ⭐ NEW |

---

## Synthesis: The Long-Term Fee Revenue Picture

Combining all frameworks, we can now say:

### Short-Term (hours to days)
- Use LVR = σ²L/8 for loss rate
- Fee income = γ × volume / liquidity
- Net = Fee - LVR

### Medium-Term (weeks to months)
- Fritz time-regime effects matter
- IL and LVR diverge from one-step predictions
- Consider optimal exit (Bergault)

### Long-Term (months to years, passive)
- If you never exit: Tassy-White log-growth rate applies
- If you actively reposition: Cao exponential decay kicks in
- **Equilibrium bound**: Returns converge to staking rate (Gogol)

### Very Long-Term (market equilibrium)
- Capital flows equalize returns across DeFi
- LP return → staking return (risk-adjusted)
- Excess fee revenue is competed away

### Practical Implication

**For long-term profitability:**
1. Use wide passive ranges (avoid rebalancing decay)
2. Pick pools with volatility-adaptive fees
3. Expect returns to converge toward staking rate
4. Outperformance requires either:
   - First-mover advantage (before equilibrium)
   - Superior information (better entry/exit timing)
   - Undersubscribed pools (L2s, new pools)

---

## NEW: Structural Improvement via AMM Design (Feb 2026 Evening) ⭐⭐

### am-AMM: Higher Equilibrium Liquidity (arxiv:2403.03367)

**Key Insight**: The Moallemi group (authors of original LVR paper) proposes a mechanism that **structurally improves** long-term LP profitability, not through strategy but through design.

### How am-AMM Works
1. **Auction for Pool Management**: Onchain auction for right to be "pool manager"
2. **Pool Manager Powers**:
   - Sets swap fee rate
   - Receives all accrued swap fees
   - Can trade against pool to capture arbitrage
3. **LPs Pay Manager**: Via auction proceeds and share of fees

### Why This Matters for Long-Term Fees

**Theorem (Moallemi et al.)**: Under certain assumptions, am-AMM has **higher liquidity in equilibrium** than any standard fixed-fee AMM.

**Intuition**:
- Pool manager internalizes LVR (captures arbitrage themselves)
- Can set dynamic fees based on market conditions
- Competition among potential managers extracts value for LPs

### Connection to Long-Term Framework

This adds a **ninth layer** — mechanism design:

| Layer | Framework | What It Addresses |
|-------|-----------|-------------------|
| 1-8 | (existing layers) | LP strategy & market dynamics |
| **9** | **am-AMM Design** | **Mechanism that structurally improves equilibrium** |

**Key Takeaway**: Long-term LP profitability is not just about strategy or timing — AMM mechanism design can create fundamentally better outcomes.

---

## Bounded Liquidity Reality (arxiv:2507.02027)

### Practical LVR Refinement

Standard LVR (σ²L/8) assumes:
- Infinitely liquid reference market (CEX)
- Arbitrageur trades against this perfect reference

Reality:
- Both markets have finite liquidity
- LVR depends on **relative liquidity** of AMM vs reference market
- LVR depends on **relative trading volume** between venues

**Implication for Long-Term Estimation**:
- If AMM liquidity is small relative to CEX: standard σ²L/8 applies
- If AMM liquidity is large or CEX illiquid: LVR is modulated
- For newer/smaller tokens: bounded liquidity model more accurate

---

## Synthesis: Complete Long-Term Picture (Feb 2026)

### The Full Stack

**Instantaneous Analysis**:
- LVR = σ²L/8 (or bounded liquidity variant)
- Fee income = γ × volume / liquidity
- Net instantaneous P&L = Fee - LVR

**Time-Scale Effects**:
- Fritz regimes: short/medium/long behave differently
- Cao decay: active rebalancing → exponential loss
- Singh option theta: LVR = time decay of CI option

**Finite-Horizon Optimization**:
- Bergault optimal stopping: when to exit?
- Yang utility optimization: how to allocate?

**Infinite-Horizon Convergence**:
- Tassy-White log-growth: asymptotic growth rate
- Gogol equilibrium: returns converge to staking rate

**Mechanism Design Layer**:
- am-AMM: auction mechanism → higher equilibrium liquidity
- Adaptive fees: volatility-scaling → 9-44% improvement

### Practitioner Decision Tree

1. **Which pool?**
   - Avoid oversubscribed L1 pools (below staking return)
   - Seek undersubscribed L2 pools or new protocols
   - Prefer am-AMM or adaptive fee mechanisms if available

2. **Which strategy?**
   - Wide passive ranges (avoid Cao decay)
   - Use optimal stopping framework for exit timing

3. **What to expect?**
   - Short-term: volatile, use LVR for loss rate
   - Long-term: expect convergence toward staking rate
   - Outperformance requires edge (timing, information, mechanism)

---

---

## NEW: Optimal Dynamic Fee Structure (Baggiani et al., Jun 2025) ⭐⭐

**Paper**: arxiv:2506.02869 — "Optimal Dynamic Fees in Automated Market Makers"

### Key Finding for Long-Term Fee Design

Via stochastic control, this paper derives the **optimal fee structure** for AMMs:

**Result**: Dynamic fees that are:
1. **Linear in inventory** (pool imbalance)
2. **Sensitive to external price changes**

are a **good approximation of the optimal fee structure**.

### Practical Implication

For long-term LP profitability, pools should implement:
```
fee(t) = f₀ + α × inventory_imbalance(t) + β × |ΔP_external(t)|
```

This operationalizes Yang (2024)'s theoretical result that optimal fees scale with volatility.

### Connection to Capponi-Zhu Framework

Baggiani et al. note that Capponi & Zhu (2025) take the complementary approach:
- Capponi-Zhu: Fixed fee, LP optimizes exit timing
- Baggiani: LP stays, AMM optimizes dynamic fee

Both approaches improve long-term LP outcomes.

---

## NEW: Implied Volatility Interpretation (Bichuch & Feinstein, Sep 2025)

**Paper**: arxiv:2509.23222 — "The Price of Liquidity: Implied Volatility of AMM Fees"

### Novel Interpretation

Reinterprets LVR as the **implied fee stream** that would make LP indifferent:
- What fee rate makes LP position worth exactly its current value?
- Connects to implied volatility pricing in options markets

### Key Insight for Long-Term Estimation

If options market data is available:
- Can infer implied volatility from AMM fee structure
- Or conversely, set AMM fees based on options-implied vol
- Provides market-based calibration for long-term LVR estimates

### Integration with Singh (2508.02971)

Both papers connect AMM pricing to options theory:
- Singh: LVR = θ (theta) of CI option
- Bichuch-Feinstein: LVR → implied volatility

**Together**: AMM LP position is fully characterized by options Greeks.

---

## Dual Optimal Stopping Approaches (Feb 2026 Update)

Two concurrent papers on optimal exit:

| Paper | Authors | Key Approach |
|-------|---------|--------------|
| arxiv:2509.06510 | Bergault et al. | HJB quasi-variational inequality + Euler/Longstaff-Schwartz |
| SSRN:5148585 | Capponi & Zhu | Alternative stopping framework for CFMs |

Both address the same question: **When should LP exit?**

Differences in modeling assumptions and solution techniques, but converging conclusions:
- Exit timing depends on volatility, fees, arbitrageur behavior
- Passive strategies not always sustainable
- Active exit timing improves long-term returns

---

## Updated Synthesis: TEN-Layer Framework (Feb 2026)

| Layer | Framework | Horizon | Key Question |
|-------|-----------|---------|--------------|
| 1 | LVR | Instant | Loss rate now? |
| 2 | Time-Regimes (Fritz) | Short/Med/Long | How does IL/LVR scale? |
| 3 | Optimal Stopping (Bergault, Capponi-Zhu) | Finite + exit | When to exit? |
| 4 | Log-Growth (Tassy-White) | Infinite passive | Asymptotic growth? |
| 5 | Utility Optimization (Yang) | Infinite + consumption | Optimal allocation? |
| 6 | Rebalancing Decay (Cao) | Long, active | Cost of repositioning? |
| 7 | Perpetual Option (Singh) | Infinite | LVR = option theta? |
| 8 | Equilibrium Convergence (Gogol) | Long-run | Target = staking rate? |
| 9 | Mechanism Design (am-AMM) | Structural | Better AMM design? |
| **10** | **Optimal Dynamic Fees (Baggiani)** | **Continuous** | **Best fee function?** ⭐ NEW |

**Critical Finding 12: Near-Optimal Fee Structure**
```
fee(t) = f₀ + α × inventory(t) + β × |ΔP(t)|
```
Linear in inventory, sensitive to price changes. Practical approximation to optimal.

---

## NEW: Super-Hedging & No-LVR Result (Fukasawa et al., Feb 2025) ⭐⭐

**Paper**: arxiv:2502.01931 — "Liquidity Provision of Utility Indifference Type" (Digital Finance 2025)

### Key Mathematical Result

**Theorem (Super-Hedging)**: Under continuous external price process, impermanent loss can be **model-free super-hedged** by a rebalancing strategy in the external market, irrespective of fee size.

**Corollary**: There is **no loss-versus-rebalancing** under nonzero fee if the external market price is continuous.

### Why This Matters

1. **Resolution of LVR Puzzle**:
   - LVR formula σ²L/8 arises from arbitrageur capturing price jumps
   - If price is continuous (diffusion), arbitrageur cannot "front-run" LP
   - Fee captures all the value; no loss to arbitrage

2. **Block-Time Critical**:
   - In reality, price has discrete jumps (block boundaries)
   - This is where LVR "lives" — in the discrete jumps
   - Confirms Tung (2412.18580) insight about fees precluding diffusion

3. **Optimality of Uniswap v3**:
   - Paper proves the concentrated liquidity construction is optimal in a specific sense
   - Answers "why v3 works" mathematically

### Connection to Unified Framework

| Framework | Price Assumption | LVR Result |
|-----------|------------------|------------|
| Milionis LVR | Jump process | σ²L/8 per unit time |
| Fukasawa | Continuous diffusion | **LVR = 0** (super-hedged) |
| Reality (blockchain) | Discrete + jumps | LVR ∈ (0, σ²L/8) depending on block time |

### Integration with Other Results

- **Singh (option-theta)**: LVR = θ for jump processes; extends to θ → 0 for continuous
- **Fritz (time-regimes)**: Long-horizon divergence may stem from cumulative jump effects
- **Milionis (discrete blocks)**: Faster blocks → smaller jumps → lower LVR → approaches Fukasawa limit

### Practical Implication

**Block time matters for long-term LVR estimation**:
- Ethereum L1 (~12s blocks): Significant LVR
- L2s (~1s blocks): Lower LVR (closer to Fukasawa limit)
- Theoretical limit: Continuous oracle → zero LVR

---

## Updated Synthesis: ELEVEN-Layer Framework (Feb 2026)

| Layer | Framework | Horizon | Key Question |
|-------|-----------|---------|--------------|
| 1 | LVR | Instant | Loss rate now? |
| 2 | Time-Regimes (Fritz) | Short/Med/Long | How does IL/LVR scale? |
| 3 | Optimal Stopping (Bergault, Capponi-Zhu) | Finite + exit | When to exit? |
| 4 | Log-Growth (Tassy-White) | Infinite passive | Asymptotic growth? |
| 5 | Utility Optimization (Yang) | Infinite + consumption | Optimal allocation? |
| 6 | Rebalancing Decay (Cao) | Long, active | Cost of repositioning? |
| 7 | Perpetual Option (Singh) | Infinite | LVR = option theta? |
| 8 | Equilibrium Convergence (Gogol) | Long-run | Target = staking rate? |
| 9 | Mechanism Design (am-AMM) | Structural | Better AMM design? |
| 10 | Optimal Dynamic Fees (Baggiani) | Continuous | Best fee function? |
| **11** | **Super-Hedging (Fukasawa)** | **Continuous price** | **LVR = 0 in limit?** ⭐ NEW |

**Critical Finding 13: Block-Time Determines LVR Magnitude**
- Continuous price → LVR super-hedged to 0
- Discrete blocks → LVR ∈ (0, σ²L/8)
- Faster blocks → lower LVR → better LP long-term returns

---

---

## NEW: Market Impact for Optimal-Growth LPs (Feb 2026) ⭐

**Paper**: arxiv:2601.11375 — "Automated Liquidity: Market Impact, Cycles, and De-pegging Risk"

### Key Connection to Long-Term Analysis

For **optimal-growth liquidity providers**:
- Market impact function can be derived analytically
- For standard random walk price process: recovers classic **square-root impact**
  ```
  impact ~ √(trade_size)
  ```

### Why This Matters

1. **Links LP Wealth to Market Microstructure**:
   - Optimal-growth LP (Kelly criterion) is exactly the Tassy-White framework!
   - Square-root impact is a fundamental market microstructure result
   - Confirms theoretical consistency across literatures

2. **Practical Implication**:
   - Large LP positions face non-linear costs when entering/exiting
   - Entry/exit timing matters even more for large positions
   - Connects to Bergault optimal stopping: exit cost is non-linear

3. **Extension Possibilities**:
   - Paper also studies market cycles and de-pegging risk
   - Stablecoin pools have distinct long-term dynamics

---

---

## NEW: Periodic Reset Strategies for LP Optimization (May 2025)

**Paper**: arxiv:2505.15338 — "Liquidity Provision with τ-Reset Strategies"

### Practical Approach to Repositioning

This paper addresses a key gap — how to optimally reposition LP positions over time:

1. **τ-Reset Framework**:
   - LP repositions at fixed intervals (τ = reset period)
   - Parameters (range width, position size) optimized via ML
   - Avoids continuous repositioning (Cao decay issue)

2. **Key Innovation**:
   - Approximates historical liquidity without needing liquidity data
   - Parametric model for in-range liquidity dynamics
   - Enables practical backtesting and strategy optimization

3. **Results**:
   - Outperforms uniform benchmark across Uniswap v3 pairs
   - Provides concrete answer to "how often should I reposition?"

### Connection to Cao Decay Result

This approach partially mitigates the exponential decay from continuous repositioning:
- Discrete resets (periodic) vs continuous tracking
- τ-reset introduces "rebalancing friction" that limits decay rate
- Trade-off: less fee capture (wider ranges) vs less decay

---

## Literature Status (Feb 2026)

The literature on long-term AMM fee revenue is now **substantially comprehensive**:

### Theoretical Frameworks Covered
- ✅ Instantaneous loss rate (LVR)
- ✅ Multi-period time regimes (Fritz)
- ✅ Optimal stopping for exit timing (Bergault, Capponi-Zhu)
- ✅ Infinite-horizon log-growth (Tassy-White, Tung)
- ✅ Utility maximization with consumption (Yang)
- ✅ Active repositioning decay (Cao)
- ✅ Option-theoretic interpretation (Singh, Bichuch-Feinstein)
- ✅ Equilibrium convergence (Gogol, MFG approaches)
- ✅ Mechanism design (am-AMM, adaptive fees)
- ✅ Continuous-price limit and super-hedging (Fukasawa)
- ✅ Market impact for LP positions (2601.11375)

### Remaining Work
The primary remaining work is:
1. **Deep-reading** priority papers for detailed mathematical results
2. **Synthesis** of formulas into unified practical framework
3. **Empirical calibration** against real LP data
4. **Sensitivity analysis** across parameter regimes

---

## NEW: Defensive Rebalancing (Herlihy, Jan 2026) ⭐

**Paper**: arxiv:2601.19950 — "Defensive Rebalancing for Automated Market Makers"

### Mechanism for Proactive LVR Reduction

Instead of passively accepting arbitrage losses, this paper proposes **defensive rebalancing**:
- Direct asset transfers between cooperating CFMMs
- Bypasses normal trading protocols
- Eliminates arbitrage configurations proactively

### Key Mathematical Result

**Theorem**: For any arbitrage-prone configuration, there exists a rebalancing that:
1. Transitions to arbitrage-free state
2. Strictly increases some CFMMs' liquidity
3. Does not reduce any CFMM's liquidity

For log-concave trading functions (including CPMM): finding this optimal rebalancing is a **convex optimization problem** with unique solution.

### Long-Term Implication

If pools coordinate defensive rebalancing:
- LVR could be structurally reduced (not just mitigated via strategy)
- Adds to the mechanism design layer (alongside am-AMM, adaptive fees)
- Requires coordination infrastructure between pools

---

*Last updated: 2026-02-07 11:46PM (added defensive rebalancing mechanism)*
