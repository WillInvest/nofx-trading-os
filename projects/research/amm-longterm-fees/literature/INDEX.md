# Literature Index — AMM Long-Term Fee Revenue

## Key Finding
Over 50% of Uniswap v3 LPs are **unprofitable** due to impermanent loss exceeding fee income. Long-term LP profitability is a significant challenge.

---

## Categories
- [LP Profitability Studies](#lp-profitability-studies)
- [Optimal Fee Research](#optimal-fee-research)
- [Impermanent Loss Analysis](#impermanent-loss-analysis)
- [LP Strategy Optimization](#lp-strategy-optimization)

---

## LP Profitability Studies

### Measuring Arbitrage Losses and Profitability of AMM Liquidity (Apr 2024)
- **URL**: https://arxiv.org/html/2404.05803v1
- **Key contribution**: Measures whether trading fees compensate for arbitrage losses
- **Key question**: Do fees sufficiently compensate LPs for incurred arbitrage losses?
- **Relevance**: Direct study of LP profitability vs losses

### Half of Uniswap LPs Losing Money (Bancor/IntoTheBlock Study)
- **URL**: https://www.nasdaq.com/articles/half-of-uniswap-liquidity-providers-are-losing-money
- **Key finding**: 51% of Uniswap v3 LPs were unprofitable
- **Key insight**: No statistical evidence that frequent position adjustments help
- **Relevance**: Empirical evidence of LP unprofitability at scale

### Impermanent Loss in Uniswap v3 (Nov 2021)
- **URL**: https://arxiv.org/pdf/2111.09192
- **Key finding**: Uniswap V3 generated $199.3m in fees but incurred $260.1m in IL
- **Result**: 49.5% of LPs with negative returns
- **Relevance**: Quantifies the fee vs IL trade-off

---

## Optimal Fee Research

### Optimal Fees for Liquidity Provision in AMMs (Aug 2025)
- **URL**: https://arxiv.org/abs/2508.08152
- **Key contribution**: Characterizes optimal AMM fee as function of market conditions
- **Key trade-off**: Fees must be low enough to attract volume, high enough to earn revenue
- **Practical insight**: Setting AMM fee to 70-80% of CEX fee yields near-optimal results
- **Priority**: HIGH

### Role of Fee Choice in Revenue Generation of AMMs (Jun 2024)
- **URL**: https://arxiv.org/html/2406.12417v1
- **Key finding**: Dynamical directional fees optimize revenue from arbitrage
- **Relevance**: Alternative fee structures for better LP outcomes

### Dynamic Fee System Based on Risk Prediction (OpenGradient, Aug 2025)
- **URL**: https://www.opengradient.ai/blog/dynamic-amm-fee-research
- **Key finding**: Dynamic fees increase profitability by adjusting to volatility
- **Relevance**: Fee adaptation improves long-term LP returns

---

## Impermanent Loss Analysis

### Impermanent Loss and Risk Profile of LP (Jun 2021)
- **URL**: https://arxiv.org/pdf/2106.14404
- **Key contribution**: Improved IL formula, risk profiles for v2 and v3
- **Key insight**: v2 is approached in the limit of range going to infinity
- **Relevance**: Mathematical foundation for IL understanding

### Uniswap v3 IL Modeling and Swap Fees Asymptotic Analysis
- **URL**: https://hal.science/hal-04214315v3/document
- **Key contribution**: Detailed mathematical modeling of v3 IL
- **Relevance**: Precise fee vs IL trade-off analysis

### Understanding Returns (Uniswap Official)
- **URL**: https://docs.uniswap.org/contracts/v2/concepts/advanced-topics/understanding-returns
- **Key formula**: `IL = 2 * sqrt(price_ratio) / (1+price_ratio) - 1`
- **Relevance**: Official documentation on LP returns

---

## LP Strategy Optimization

### Automated Market Makers: More Profitable LP Strategies (Jan 2025)
- **URL**: https://arxiv.org/html/2501.07828v1
- **Key insight**: Concentrated liquidity enables higher returns but adverse selection problem
- **Relevance**: Strategy optimization for long-term profitability

### Strategies for Mitigating IL Across Uniswap v3 (Amberdata, Jun 2025)
- **URL**: https://blog.amberdata.io/strategies-for-mitigating-impermanent-loss-across-uniswap-v3
- **Key contribution**: Practical IL mitigation strategies
- **Relevance**: Actionable tactics for LP profitability

### Analytic Approach to Maximize Profit in AMM Pools (DeFi Prime)
- **URL**: https://defiprime.com/amm-liquidity-pools
- **Key metric**: V/R ratio (Volume/Reserve) determines fee APY
- **Key insight**: V/R ratio of 1 = 109% APY at 0.3% fee
- **Relevance**: Practical metrics for LP profitability

---

## Critical Statistics

| Metric | Value | Source |
|--------|-------|--------|
| % Uniswap v3 LPs unprofitable | 51% | Bancor/IntoTheBlock |
| v3 Fees (period) | $199.3M | arXiv 2111.09192 |
| v3 IL (period) | $260.1M | arXiv 2111.09192 |
| Optimal fee vs CEX | 70-80% | arXiv 2508.08152 |

---

## Research Gaps Identified

1. **Long-term compounding studies**: Few papers track LP positions over multiple market cycles
2. **Cross-AMM comparison**: Limited empirical comparison of v2 vs v3 vs Curve long-term
3. **Reinvestment strategies**: Impact of fee reinvestment on long-term returns
4. **Market regime analysis**: LP profitability in bull/bear/sideways markets

---

---

## Additional Sources (Sweep 2)

### Strategic Liquidity Provision in Uniswap v3 (Aug 2024)
- **URL**: https://arxiv.org/html/2106.12033v5
- **Key contribution**: Dynamic allocation strategies based on LP price beliefs
- **Key finding**: Large gains over baseline uniform allocation strategies
- **Relevance**: Active management for long-term returns

### Risks and Returns of Uniswap V3 LPs (May 2022)
- **URL**: https://arxiv.org/pdf/2205.08904
- **Key contribution**: Simulates LP strategies with historical data
- **Relevance**: Empirical strategy evaluation framework

### Follow-Up Analyses of LP Profitability (CrocSwap, Jan 2023)
- **URL**: https://crocswap.medium.com/follow-up-analyses-of-lp-profitability-in-uniswap-v3
- **Key finding**: Polygon LPs lose 10-20% less than mainnet LPs
- **Relevance**: Cross-chain LP profitability comparison

### When Uniswap v3 Returns More Fees for Passive LPs (Uniswap Official, Jun 2022)
- **URL**: https://uniswap.org/blog/fee-returns
- **Key contribution**: Identifies conditions where passive LPs outperform
- **Relevance**: Understanding passive vs active trade-offs

### LiqBoost: Enhancing Liquidity Provision (ScienceDirect, Aug 2025)
- **URL**: https://www.sciencedirect.com/science/article/abs/pii/S0957417425028465
- **Key contribution**: Addresses cyclical liquidity challenges
- **Relevance**: Long-term DEX sustainability

### Liquidity Pools, Correlation, and Compound Interest (Apr 2025)
- **URL**: https://medium.com/@jeff.paul/liquidity-pools-correlation-and-compound-interest
- **Key insight**: Compound interest through reinvested fees can enhance long-term returns
- **Trade-off**: Must be weighed against IL and market fluctuations
- **Relevance**: Direct study of fee compounding

### KyberSwap Reinvestment Curve Documentation
- **URL**: https://docs.kyberswap.com/reference/legacy/kyberswap-elastic/concepts/reinvestment-curve
- **Key feature**: Auto-compounding yields, fees immediately reinvested
- **Relevance**: Implementation example of fee compounding

---

---

## Long-Term Fee Revenue Papers ⭐ (Priority Focus)

### Growth Rate of LP Wealth in G3Ms (Mar 2024) ⭐⭐⭐
- **URL**: https://arxiv.org/abs/2403.18177
- **Authors**: Tung et al.
- **Key contribution**: Uses **stochastic reflected diffusion** to compute long-term logarithmic growth rate of LP wealth
- **Key finding**: Extends Tassy-White (2020) results from CPMM to general G3Ms
- **Method**: Calculates `lim(T→∞) (1/T) E[log W_T]` explicitly
- **Priority**: CRITICAL — this is the primary long-term fee framework

### Tassy-White (2020) — Foundation Paper
- **URL**: https://benchugg.com/research_notes/tassy_white_amms/ (exposition)
- **Key contribution**: Original **asymptotic growth rate** analysis for xy=k AMMs
- **Method**: Markov chain on fee-bounded price ratio states
- **Key formula**: Product X_t × Y_t grows by C^n after n trades, where C = exp(δ(1-γ)/(1+γ))
- **Priority**: HIGH — theoretical foundation for long-term analysis

### Optimal Fees for Geometric Mean Market Makers (Apr 2021)
- **URL**: https://arxiv.org/abs/2104.00446
- **Authors**: Evans et al.
- **Key contribution**: Framework for optimal fee selection under general diffusions
- **Key finding**: LP with mean-variance utility prefers G3M as fees → 0
- **Relevance**: Connects to long-term utility optimization

### IL and LVR I: Statistical Properties (Oct 2024) ⭐⭐ NEW
- **URL**: https://arxiv.org/abs/2410.00854
- **Authors**: Fritz et al.
- **Key finding**: For Brownian motion, IL and LVR have **identical expectation values but vastly different distribution functions**
- **Method**: Statistical analysis using random walk properties + CFMM mechanics
- **Relevance**: Foundation for time-regime analysis in Part II
- **Priority**: HIGH — establishes statistical baseline

### IL and LVR II: Three Time Regimes (Feb 2025) ⭐⭐
- **URL**: https://arxiv.org/abs/2502.04097
- **Authors**: Fritz et al.
- **Key finding**: IL/LVR relationship changes across THREE time regimes
- **Regimes**: (i) short: IL≡LVR; (ii) intermediate: same mean, different distributions; (iii) long: distinct means AND distributions
- **Implication**: One-step σ²/8 analysis does NOT extrapolate linearly!
- **Priority**: HIGH — crucial for long-term understanding

### CLMM Dynamics in Continuous Time (Dec 2024)
- **URL**: https://arxiv.org/abs/2412.18580
- **Authors**: Tung et al. (same group as G3M growth paper)
- **Key finding**: Fees preclude diffusion terms — prevents infinite fee generation
- **Implication**: Pure GBM models are approximations; block-time matters
- **Priority**: HIGH — continuous-time framework

### Equilibrium Reward for LPs in AMMs (Mar 2025)
- **URL**: https://arxiv.org/abs/2503.22502
- **Key contribution**: Leader-follower stochastic game for LP rewards
- **Key finding**: Equilibrium contract depends on external price, pool reference price, and reserves
- **Relevance**: Dynamic optimization over time

### Liquidity Provision of Utility Indifference Type (Feb 2025, Digital Finance 2025) ⭐⭐ NEW
- **URL**: https://arxiv.org/abs/2502.01931
- **Authors**: Masaaki Fukasawa, Basile Maire, Marcus Wunsch
- **Key contribution**: Rigorous mathematical framework for CFMMs of utility indifference type
- **Key findings**:
  - IL can be **super-hedged** by model-free rebalancing strategy irrespective of fee size (if external price is continuous)
  - **No LVR under nonzero fee** if external price process is continuous
  - Proves optimality of **Uniswap v3 concentrated liquidity construction** in a precise sense
  - Multi-LP analysis reduces to representative LP (liquidity pooling theorem)
- **Published**: Digital Finance (Springer), May 2025
- **Relevance**: Foundational mathematical framework; connects hedging, LVR, and AMM design
- **Priority**: HIGH — complements Singh (option-theta) and Fritz (time-regimes) approaches

---

## Loss Versus Rebalancing (LVR) Papers

### LVR Paper — Milionis et al. (2022)
- **URL**: https://anthonyleezhang.github.io/pdfs/lvr.pdf
- **Key formula**: LVR = σ²L/8 per unit time (instantaneous rate)
- **Key insight**: LVR persists even if price reverts; IL doesn't
- **Priority**: CRITICAL — standard one-step loss metric

### LVR with Fees and Discrete Blocks — Milionis et al. (May 2023, updated Jul 2025) ⭐ NEW
- **URL**: https://arxiv.org/abs/2305.14604
- **Key contribution**: Extends LVR model to include **fees and discrete Poisson block times**
- **Method**: Computes expected instantaneous arbitrage profit in **closed form**
- **Key findings**:
  - Process is **ergodic** with unique stationary distribution
  - Fees scale down arbitrage profits by fraction of blocks with profitable opportunities
  - **Faster blockchains → reduced LP losses** (critical practical insight)
  - Lower gas fees → smaller LP losses
- **Relevance**: Provides stationary distribution framework for long-term analysis
- **Priority**: HIGH — bridges continuous-time theory with discrete blockchain reality

### LVR under Deterministic and Generalized Block-Times (May 2025)
- **URL**: https://arxiv.org/abs/2505.05113
- **Key contribution**: Extends LVR analysis to realistic block timing
- **Relevance**: Bridge between continuous-time theory and discrete blockchain reality

---

## Optimal Stopping & Dynamic Exit Papers ⭐ NEW

### Optimal Exit Time for Liquidity Providers in AMMs (Sep 2025) ⭐⭐⭐ NEW
- **URL**: https://arxiv.org/abs/2509.06510
- **Authors**: Philippe Bergault et al.
- **Key contribution**: Frames LP withdrawal as **optimal stopping/stochastic control** problem
- **Method**: Hamilton-Jacobi-Bellman quasi-variational inequality; Euler + Longstaff-Schwartz solvers
- **Key findings**:
  - Optimal exit depends on: oracle price volatility, fee levels, arbitrageur/noise trader behavior
  - LP balances fees (positive) vs IL (negative) based on pool state and price misalignment
  - Derives **optimal fee level** when LP plays optimal exit strategy
  - Provides sustainability insights for passive LP strategies under different market regimes
- **Why Critical for Long-Term**: Directly answers "When should an LP exit?" — the core long-term profitability question
- **Priority**: HIGH — new framework for dynamic long-term LP decisions

### Optimal Decisions for Liquid Staking: Allocation and Exit Timing (Jul 2025)
- **URL**: https://arxiv.org/abs/2507.14810
- **Key contribution**: Stochastic control for LST allocation + exit timing
- **Key finding**: Identifies fee threshold for LST liquidity provision
- **Relevance**: Extension of optimal stopping to staking context

---

## Long-Term Liquidity Decay Papers ⭐⭐ NEW (Feb 2026)

### Chasing Price Drains Liquidity (Jan 2025) ⭐⭐⭐ CRITICAL NEW
- **URL**: https://arxiv.org/abs/2501.12583
- **Authors**: Yizhou Cao, Yepeng Ding, Ruichao Jiang, Long Wen
- **Key contribution**: Proves that **active LP strategies tracking price lead to exponential liquidity decay**
- **Model**: Uniswap v3 style CLMM under GBM price process
- **Key finding**: Strategy that adjusts liquidity position to track current price leads to **deterministic and exponentially fast decay** of liquidity
- **Formula**: Liquidity decays as L(t) ~ L(0) × exp(-λt) for price-tracking strategies
- **Why Critical**: 
  - Shows that "active management" intuition can be catastrophically wrong
  - Passive wide-range strategies may preserve long-term wealth better
  - Fundamental limitation on concentrated LP rebalancing strategies
- **Implication for Long-Term Fees**: Active repositioning strategies have hidden long-term costs that compound over time
- **Priority**: CRITICAL — major finding for long-term LP strategy evaluation

---

## Optimal Fee Design Papers (Feb 2026 Update)

### A Structural Model of Automated Market Making (Oct 2023, updated Nov 2025) NEW
- **URL**: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4591447
- **Authors**: David Cao, Leonid Kogan, Gerry Tsoukalas, Brett Hemenway Falk
- **Key contribution**: Characterizes optimal **volatility-sensitive fee schedule**
- **Key finding**: Fixed fees are inefficient; adaptive fees increase annual revenue by **9-44%** and liquidity supply by **2-10%**
- **Method**: Structural econometric model tested on ETH-USDC data
- **Relevance**: Empirical validation of Yang (2024) theoretical result that optimal fees scale with volatility
- **Priority**: HIGH — empirical support for volatility-adaptive fees

---

## Multi-Period Optimization & Design Papers (Feb 2026 Update)

### Optimal Design of AMMs on DEXs (Apr 2024) ⭐⭐ NEW
- **URL**: https://arxiv.org/abs/2404.13291
- **Authors**: Chen Yang et al.
- **Key contribution**: **Infinite horizon utility maximization** for LP
- **Framework**: Risk-averse LP decides wealth allocation to DEX liquidity, CEX trading, and consumption across multiple periods
- **Key findings**:
  - Optimal unit trading fee **increases with volatility**
  - Optimal pricing function makes asset allocation efficient for LP
  - First paper to jointly optimize AMM design + LP strategy over infinite horizon
- **Priority**: HIGH — direct long-term utility optimization framework

### Strategic Analysis of JIT Liquidity Provision (Sep 2025) NEW
- **URL**: https://arxiv.org/abs/2509.16157
- **Key contribution**: First formal transaction-level model of JIT LPs in CLMMs
- **Key finding**: JIT LPs can increase earnings 69% by accounting for price impact; erode passive LP profits by 44%
- **Relevance**: Adversarial environment affects long-term passive LP profitability
- **Priority**: MEDIUM — important for understanding competitive dynamics

### Pooling Liquidity Pools (Mar 2025) NEW
- **URL**: https://arxiv.org/abs/2503.09765
- **Key contribution**: Global Market Maker (GMM) to aggregate liquidity across AMMs
- **Key findings**: Eliminates arbitrage opportunities, reduces sandwich attacks, minimizes IL
- **Relevance**: Market structure improvements for long-term LP profitability
- **Priority**: MEDIUM — design-level improvement

---

---

## Perpetual / Infinite Horizon Papers ⭐ NEW (Feb 2026)

### Modeling LVR via Continuous-Installment Options (Aug 2025) ⭐⭐⭐ CRITICAL NEW
- **URL**: https://arxiv.org/abs/2508.02971
- **Authors**: Srisht Fateh Singh et al.
- **Key contribution**: Models CFAMM position as **perpetual American continuous-installment (CI) options**
- **Why Critical for Long-Term**:
  - Replicates AMM position's delta over **infinite time horizon**
  - Accounts for perpetual nature of LP positions
  - Proves LVR = theta (time decay) of at-the-money CI option embedded in replicating portfolio
  - Derives LP profile with **approximately constant LVR** over arbitrarily long forward window
- **Key Result**: Provides practical framework for estimating future adverse-selection costs over extended horizons
- **Priority**: CRITICAL — first infinite-horizon option-theoretic framework for AMMs

### Risk-Neutral Pricing of Uniswap LP Position: Stopping Time Approach (Nov 2024) NEW
- **URL**: https://arxiv.org/abs/2411.12375
- **Authors**: Guosong Xu et al.
- **Key contribution**: Frames LP position valuation using **Martingale Stopping Theorem**
- **Key finding**: Provides risk-neutral valuation framework with Greek sensitivities
- **Relevance**: Complements Bergault optimal stopping with risk-neutral pricing
- **Priority**: MEDIUM — useful for hedging strategies

### Predictable Loss and Optimal Liquidity Provision (Sep 2023, SIAM J. Fin. Math.) ⭐⭐ NEW
- **URL**: https://arxiv.org/abs/2309.08431
- **Authors**: Fayçal Drissi et al.
- **Key contribution**: Characterizes **continuous-time wealth dynamics** of strategic LPs
- **Key findings**:
  - Closed-form optimal strategy for range width based on fees, PL, concentration risk
  - Shows how to optimally skew range when drift is stochastic
  - **Empirical finding**: LPs have traded at significant loss on average
- **Formula**: Wealth = fee income - holdings value - rebalancing costs
- **Relevance**: Connects short-term decisions to long-term wealth trajectory
- **Priority**: HIGH — bridges instantaneous to extended horizons

### Dynamics of Liquidity Surfaces in Uniswap v3 (Sep 2025) NEW
- **URL**: https://arxiv.org/abs/2509.05013
- **Authors**: Jimmy Risk et al.
- **Key contribution**: Models liquidity as time-tick surface L_t(x) using FPCA
- **Key finding**: Liquidity dynamics follow AR(1) + GARCH structure
- **Relevance**: Understanding how aggregate liquidity evolves over time
- **Priority**: MEDIUM — useful for market structure analysis

---

## Equilibrium & Long-Run Convergence Papers ⭐ NEW (Feb 7, 2026)

### Liquidity Fragmentation or Optimization? (Oct 2024, updated Mar 2025) ⭐⭐ NEW
- **URL**: https://arxiv.org/abs/2410.10324
- **Authors**: Krzysztof Gogol et al.
- **Key contribution**: Shows that **in equilibrium, AMM LP returns converge to a reference rate** (staking)
- **Method**: Lagrangian optimization for optimal liquidity allocation across L1/L2
- **Key findings**:
  - LP returns converge to staking rate in equilibrium (long-run target)
  - Ethereum L1 pools are **oversubscribed** vs L2s
  - L1 pools often yield **lower than staking**
  - LPs could improve returns by reallocating >2/3 of liquidity to L2s
  - Trading volume elasticity wrt TVL is low on established chains
- **Why Critical for Long-Term**: Provides **equilibrium bound** for long-term LP returns!
- **Priority**: HIGH — equilibrium convergence to staking rate is key insight

### Liquidity Pools as Mean Field Games (Dec 2024) ⭐⭐ NEW
- **URL**: https://arxiv.org/abs/2412.09180
- **Authors**: Agustin Muñoz Gonzalez et al.
- **Key contribution**: First application of **mean field games** to AMM liquidity pools
- **Key findings**:
  - Proves existence of MFG solutions for AMM LP optimization
  - Shows existence of approximate Nash equilibria
  - Extends traditional order book MFG models to AMM setting
- **Why Relevant for Long-Term**: MFG provides framework for understanding LP behavior with many strategic agents over time
- **Priority**: MEDIUM-HIGH — new theoretical lens for equilibrium analysis

### Game Theoretic Liquidity Provisioning in CLMMs (Nov 2024) NEW
- **URL**: https://arxiv.org/abs/2411.10399
- **Authors**: Weizhao Tang et al.
- **Key contribution**: Nash equilibrium analysis of LP strategies in CLMMs
- **Key findings**:
  - Nash equilibrium follows **waterfilling strategy**
  - Low-budget LPs use full budget; rich LPs do not
  - Real-world LPs deviate significantly from Nash (use wider, fewer ranges)
  - Adjusting to Nash equilibrium improves median daily returns by $116 (~0.009%)
- **Why Relevant for Long-Term**: Understanding equilibrium LP behavior informs long-run profitability
- **Priority**: MEDIUM — provides empirical evidence on LP behavior vs theory

---

---

## LVR Extensions & New AMM Designs (Feb 2026 Update)

### Arbitrage with Bounded Liquidity (Jul 2025, updated Dec 2025) NEW
- **URL**: https://arxiv.org/abs/2507.02027
- **Authors**: Christoph Schlegel et al.
- **Key contribution**: Extends LVR to arbitrage between **two imperfectly liquid** markets (no infinite liquidity reference)
- **Key finding**: LVR depends on relative liquidity and relative trading volume between the two markets
- **Assumption**: Quadratic trading costs on at least one market (holds for most markets except highly liquid CEX pairs)
- **Relevance**: More realistic LVR model when no truly liquid reference market exists
- **Priority**: MEDIUM — refinement of LVR for real-world conditions

### am-AMM: An Auction-Managed AMM (Mar 2024, updated Feb 2025) ⭐⭐ NEW
- **URL**: https://arxiv.org/abs/2403.03367
- **Authors**: Ciamac Moallemi et al. (same group as LVR paper!)
- **Key contribution**: Single mechanism targeting BOTH informed orderflow losses AND uninformed orderflow revenue
- **Innovation**: Runs censorship-resistant auction for the right to be "pool manager" 
- **Pool manager benefits**: Sets swap fees, receives accrued fees, can capture arbitrage
- **Key finding**: Proves this AMM has **higher equilibrium liquidity** than any fixed-fee AMM
- **Relevance**: Design that could improve long-term LP profitability structurally
- **Priority**: HIGH — from the leading LVR research group

### Better Market Maker Algorithm (BMM) (Feb 2025) NEW
- **URL**: https://arxiv.org/abs/2502.20001
- **Authors**: Nate Leung et al.
- **Key contribution**: Power-law invariant AMM (X^n Y = K, n=4) + dynamic rebate system
- **Key findings**:
  - Reduces IL by 36% compared to XY=K
  - Retains 3.98x more liquidity during volatility
  - 40% higher user engagement vs static fee models
- **Method**: Market segmentation (high/mid/low volatility regimes)
- **Relevance**: Alternative AMM design for improved long-term LP returns
- **Priority**: MEDIUM — novel design approach

### Concentrated Liquidity with Leverage (Sep 2024) NEW
- **URL**: https://arxiv.org/abs/2409.12803
- **Authors**: Atis Elsts et al.
- **Key contribution**: Formalizes leveraged CL positions with overcollateralized lending
- **Key findings**:
  - Proves leveraged LP positions possess safety properties (bounded margin)
  - Formalizes margin level, assets, and debt for leveraged CL
- **Relevance**: Higher capital efficiency for concentrated liquidity — affects long-term return calculation
- **Priority**: MEDIUM — practical extension of CL

---

---

## NEW Papers (Feb 7, 2026 Evening Sweep)

### Optimal Exiting for Liquidity Provision in CFMs (Feb 2025) ⭐⭐ NEW
- **URL**: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5148585
- **Authors**: Agostino Capponi, Brian Zhu
- **Key contribution**: Concurrent work to Bergault on optimal exit time from CFMs
- **Key finding**: Determines optimal exit strategy for liquidity providers under IL
- **Relevance**: Alternative approach to Bergault for finite-horizon LP optimization
- **Priority**: HIGH — complement to Bergault framework

### Optimal Dynamic Fees in Automated Market Makers (Jun 2025) ⭐⭐ NEW
- **URL**: https://arxiv.org/abs/2506.02869
- **Authors**: Leonardo Baggiani, Martin Herdegen, Leandro Sánchez-Betancourt
- **Key contribution**: Derives optimal dynamic fee structure via stochastic control
- **Key finding**: **Dynamic fees linear in inventory + price-sensitive ≈ optimal**
- **Implication**: Good approximation for practical fee design
- **Relevance**: Direct application for long-term fee optimization
- **Priority**: HIGH — practical optimal fee design

### The Price of Liquidity: Implied Volatility of AMM Fees (Sep 2025) ⭐⭐ NEW
- **URL**: https://arxiv.org/abs/2509.23222
- **Authors**: Maxim Bichuch, Zachary Feinstein
- **Key contribution**: Reinterprets LVR as **implied fee stream** from options perspective
- **Key finding**: Links AMM fee structure to implied volatility pricing
- **Relevance**: Connects options market data to LP expected returns
- **Priority**: MEDIUM-HIGH — novel options-theoretic interpretation

### Improving DeFi Accessibility with Deep RL (Jan 2025) NEW
- **URL**: https://arxiv.org/abs/2501.07508
- **Authors**: (multiple)
- **Key contribution**: Applies deep RL to optimize LP in Uniswap v3
- **Key finding**: Active LP outperforms heuristic passive strategies in 7/11 test windows
- **Relevance**: RL-based approach to long-term LP strategy optimization
- **Priority**: MEDIUM — empirical/algorithmic approach

### Optimal Execution on Uniswap v2/v3 Under Transient Impact (Jan 2026) NEW
- **URL**: https://arxiv.org/abs/2601.03799
- **Authors**: (multiple)
- **Key contribution**: Optimal liquidation on AMMs with transient price impact
- **Key finding**: Derives optimal execution schedule accounting for AMM mechanics
- **Relevance**: Understanding execution costs affects LP net returns
- **Priority**: MEDIUM — execution side rather than provision side

---

---

## NEW Papers (Feb 7, 2026 11:46PM Routine)

### Defensive Rebalancing for Automated Market Makers (Jan 2026) ⭐⭐ NEW
- **URL**: https://arxiv.org/abs/2601.19950
- **Authors**: Maurice Herlihy et al.
- **Key contribution**: Novel mechanism for protecting CFMMs from arbitrage via **defensive rebalancing**
- **Key findings**:
  - Direct asset transfers between CFMMs can eliminate arbitrage configurations
  - Proves existence of Pareto-efficient rebalancing that increases liquidity without harming any participant
  - For log-concave trading functions (including CPMM): optimal rebalancing is **convex optimization** with unique solution
  - Extends to "mixed rebalancing" — harvesting arbitrage from non-participating CFMMs and CEXs
- **Long-term relevance**: Proactive defense against arbitrage could structurally reduce LVR for participating pools
- **Priority**: MEDIUM-HIGH — novel mechanism design for LP protection

---

## Papers (Feb 7, 2026 8:45PM Routine)

### Automated Liquidity: Market Impact, Cycles, and De-pegging Risk (Jan 2026) ⭐⭐
- **URL**: https://arxiv.org/abs/2601.11375
- **Key contribution**: Derives market impact function for **optimal-growth liquidity providers**
- **Key finding**: For standard random walk, recovers classic **square-root market impact**
- **Relevance**: Connects LP wealth dynamics to market impact theory
- **Priority**: HIGH — links optimal-growth LP framework to established market microstructure

### A Formal Approach to AMM Fee Mechanisms with Lean 4 (Feb 2026) NEW
- **URL**: https://arxiv.org/abs/2602.00101
- **Authors**: Dessalvi et al. (DTU Denmark)
- **Key contribution**: Formal verification of AMM fee mechanisms using Lean 4 theorem prover
- **Key findings**:
  - Extends foundational AMM model with trading fee parameter φ ∈ (0,1]
  - Formally proves properties of swap behavior under fees
  - Proves arbitrage solution differs from equilibrium solution when fees present
- **Relevance**: Mathematically rigorous foundation for fee analysis
- **Priority**: MEDIUM — verification rather than new insights, but useful for rigor

### Stochastic Optimization for Profitable Liquidity Concentration (Apr 2025) NEW
- **URL**: https://arxiv.org/abs/2504.16542
- **Key contribution**: Stochastic optimization framework for CL position sizing
- **Key finding**: Provides foundation for more profitable liquidity concentration decisions
- **Relevance**: Optimization approach to concentrated liquidity profitability
- **Priority**: MEDIUM — adds to strategy optimization literature

### Liquidity Provision with τ-Reset Strategies (May 2025) NEW
- **URL**: https://arxiv.org/abs/2505.15338
- **Authors**: Rostislav Berezovskiy et al.
- **Key contribution**: ML-based optimization of LP strategies using periodic reset schedules
- **Key innovation**: Historical liquidity approximation without requiring liquidity data
- **Method**: τ-reset strategies = LP repositions at fixed intervals with ML-optimized parameters
- **Key finding**: Outperforms uniform benchmark across multiple Uniswap v3 pairs
- **Relevance**: Practical approach to long-term LP strategy optimization
- **Priority**: MEDIUM — practical ML approach to address optimal repositioning frequency

---

## Next Steps
1. Deep-read Tung et al. (2403.18177) for explicit long-term growth formula
2. Deep-read Fritz et al. (2502.04097) for time-regime analysis
3. **Deep-read Bergault et al. (2509.06510) for optimal exit/stopping framework** ⭐
4. **Deep-read Capponi & Zhu (SSRN 5148585) for comparison** ⭐ NEW
5. **Deep-read Yang et al. (2404.13291) for infinite-horizon utility optimization** ⭐
6. **Deep-read Singh et al. (2508.02971) for perpetual CI option model** ⭐⭐
7. **Deep-read Baggiani et al. (2506.02869) for optimal dynamic fees** ⭐ NEW
8. Derive conditions for positive long-term LP return (fee vs LVR)
9. Compare theoretical predictions to empirical LP data
10. Model block-time effects on long-term fee accumulation
11. **Integrate optimal stopping into long-term fee estimation framework** ⭐
12. **Examine JIT LP effects on passive LP long-term returns**
13. **Connect perpetual option theta to long-term fee estimation** ⭐
14. **NEW: Evaluate am-AMM auction mechanism for LP profitability** ⭐
15. **NEW: Assess implied volatility approach (Bichuch-Feinstein)** NEW
