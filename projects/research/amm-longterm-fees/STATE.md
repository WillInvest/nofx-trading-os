# Research State — AMM Long-Term Fee Revenue

## Current Focus
**Long-term fee estimation** — finding papers that estimate fees over extended periods (not just one-step analysis).

### Key Paper Found
- **"Growth rate of LP wealth in G3Ms"** (arxiv 2403.18177) — long-term logarithmic growth analysis

### Search Priority
Papers that:
1. Estimate long-term (multi-period) fee revenue
2. Analyze compounding effects over time
3. Model fee accumulation under GBM/arbitrage
4. Extend one-step analysis to long horizons

## Research Questions
1. What determines long-term LP fee revenue sustainability?
2. How do different AMM designs affect fee capture over time?
3. What is the empirical data on LP profitability across market cycles?
4. How does compounding work in AMM LP positions?
5. What strategies optimize long-term fee revenue?

## Recent Progress
- [2026-02-05] Project created, beginning initial literature search
- [2026-02-07] **Major breakthrough** — identified core long-term fee literature:
  - Tassy-White (2020): Foundation paper on asymptotic LP wealth growth
  - Tung et al. (2403.18177): Extension to G3Ms using reflected diffusion
  - Fritz et al. (2502.04097): Critical 3-regime time analysis (IL/LVR diverge at long horizons!)
  - Created THEORY.md with framework for extending one-step to long-term
- [2026-02-07] **NEW: Optimal Stopping Framework discovered** — Bergault et al. (arxiv:2509.06510)
  - Frames LP withdrawal as stochastic control / optimal stopping problem
  - Solves for optimal exit time given fees, volatility, arbitrageur behavior
  - Jointly optimizes exit time AND fee level — first paper to do this!
  - Key bridge between one-step analysis and long-term estimation
  - Updated THEORY.md with unified framework: one-step → optimal stopping → log-growth
- [2026-02-07] **Added infinite-horizon utility framework** — Yang et al. (arxiv:2404.13291)
  - Risk-averse LP maximizing `E[∑ β^t u(c_t)]` over infinite horizon
  - First to jointly optimize AMM design + LP strategy over infinite horizon
  - Key finding: optimal fee increases with volatility
  - Added as 4th layer in unified long-term framework
- [2026-02-07] **Identified JIT LP competition effects** — arxiv:2509.16157
  - JIT LPs erode passive LP profits by up to 44% per trade
  - Important for realistic long-term profitability estimates
  - Original Tassy-White model needs modification for LP type heterogeneity
- [2026-02-07] **MAJOR: Discovered exponential decay from rebalancing** — arxiv:2501.12583 ⭐⭐
  - "Chasing Price Drains Liquidity" proves that active position tracking → exponential liquidity decay
  - L(t) ~ L(0) × exp(-λt) for price-chasing strategies under GBM
  - Game-changing result: passive wide-range strategies may be optimal for long-term
  - Added to THEORY.md as new critical layer of analysis
- [2026-02-07] **Added empirical fee optimization support** — SSRN 4591447
  - "Structural Model of AMM" confirms adaptive fees outperform fixed by 9-44%
  - Validates Yang (2024) theoretical result about volatility-scaling fees
- [2026-02-07] (Daily routine) Confirmed literature comprehensive; added Milionis et al. (2305.14604) on ergodic stationary distribution for arbitrage profits with discrete block times
  - Key insight: Process is ergodic → unique stationary distribution exists
  - Faster blockchains → reduced LP losses
  - Connects to long-term analysis via stationary distribution framework
- [2026-02-07 PM] **MAJOR: Discovered perpetual option framework** — Singh et al. (arxiv:2508.02971) ⭐⭐
  - Models AMM as **perpetual American continuous-installment options**
  - Proves LVR = theta (time decay) of at-the-money CI option
  - First infinite time horizon option-theoretic framework!
  - Derives constant-LVR profiles over arbitrarily long forward windows
  - Added to THEORY.md as seventh layer of analysis
- [2026-02-07 PM] Added three more relevant papers:
  - Drissi et al. (arxiv:2309.08431): Continuous-time wealth dynamics, forthcoming SIAM
  - Xu et al. (arxiv:2411.12375): Risk-neutral LP pricing via stopping time
  - Risk et al. (arxiv:2509.05013): Liquidity surface dynamics (AR+GARCH)

## Next Actions
- [x] Search for papers on LP profitability and fee revenue
- [x] Find long-term fee estimation frameworks
- [x] Find optimal stopping / dynamic exit framework ⭐
- [x] Find infinite-horizon utility optimization framework ⭐
- [x] Identify competitive dynamics (JIT LPs) ⭐
- [x] Find exponential decay from rebalancing result ⭐⭐ (arxiv:2501.12583)
- [x] Find empirical validation for volatility-adaptive fees ⭐ (SSRN 4591447)
- [x] **Find perpetual option framework for infinite horizon** ⭐⭐ (arxiv:2508.02971) NEW
- [ ] Deep-read arxiv:2403.18177 (Tung) for explicit growth rate formula
- [ ] Deep-read arxiv:2502.04097 (Fritz) for 3-regime analysis
- [ ] Deep-read arxiv:2509.06510 (Bergault) for optimal stopping
- [ ] Deep-read arxiv:2404.13291 (Yang) for infinite-horizon utility
- [ ] Deep-read arxiv:2501.12583 (Cao) for exponential decay proof
- [ ] **Deep-read arxiv:2508.02971 (Singh) for LVR = option theta** ⭐⭐ NEW PRIORITY
- [ ] Derive break-even fee conditions for positive long-term return
- [ ] Compare theoretical predictions to empirical data (51% unprofitable)
- [ ] Model block-time effects on fee accumulation
- [ ] Build unified model combining all frameworks (now SEVEN layers)
- [ ] Model LP type heterogeneity (passive vs JIT)
- [ ] Analyze optimal repositioning frequency given exponential decay
- [ ] **Connect theta-based LVR to long-term fee estimation** ⭐ NEW

## Blockers
None

## Key Insights

### Critical Finding 1: Three Time Regimes (Fritz et al.)
One-step analysis (σ²/8) does NOT extrapolate linearly to long horizons!
- Short: IL ≡ LVR
- Intermediate: Same mean, different distributions
- Long: Different means AND distributions

### Critical Finding 2: Tassy-White Framework
Long-term LP wealth growth can be computed via Markov chain:
- States = price ratio relative to LP ratio (within no-arb zone)
- Stationary distribution → expected log growth rate
- Product X_t × Y_t grows by factor C^n after n trades

### Critical Finding 3: Continuous-Time Subtlety (Tung 2024)
Fees preclude continuous diffusion in price process!
- GBM is an approximation; block-time effects are real
- Reflected diffusion is more appropriate model

### Formula Summary
- One-step LVR: E[LVR] = σ²L/8
- Long-term growth: lim(T→∞) (1/T) E[log W_T] — requires Markov chain or reflected diffusion
- Fee-growth factor: C = exp(δ(1-γ)/(1+γ)) per trade
- Optimal stopping value: V(x) = sup_τ E[∫₀^τ (fee - IL) dt + exit_value(τ)]
- **Rebalancing decay**: L(t) ~ L(0) × exp(-λt) for price-tracking strategies
- **LVR = θ (theta)**: LVR ≡ time decay of ATM perpetual CI option ⭐⭐ NEW

### Unified Framework (SEVEN Complementary Layers)
| Layer | Horizon | Method | Question |
|-------|---------|--------|----------|
| One-step | Instant | σ²L/8 | What's loss rate now? |
| Time-Regimes | Short/Med/Long | Fritz analysis | How does IL/LVR scale? |
| Optimal Stopping | Finite + exit | HJB equation | When to exit? |
| Log-Growth | Infinite, passive | Markov chain | Asymptotic growth rate? |
| Utility Optimization | Infinite + consumption | Yang framework | How to allocate optimally? |
| Rebalancing Decay | Long, active | Cao exp(-λt) | What if I reposition? |
| **Perpetual Option** | **Infinite** | **LVR = θ of CI option** | **Use options math for LP** ⭐ NEW |

### Critical Finding 4: JIT LP Competition (Sep 2025)
Strategic JIT LPs erode passive LP profits by up to **44% per trade**:
- JIT LPs provide liquidity for single trades, capture disproportionate fees
- Passive LP long-term profitability worse than theoretical models suggest
- Need to model LP type heterogeneity for realistic estimates

### Critical Finding 5: Optimal Fee Scales with Volatility (Yang 2024)
In infinite-horizon utility framework:
- Optimal trading fee **increases with price volatility**
- First joint optimization of AMM design + LP strategy
- More realistic than passive log-growth assumptions

### Critical Finding 6: Exponential Decay from Rebalancing (Cao et al. 2025) ⭐⭐ NEW
**GAME-CHANGING RESULT**: Active LP strategies that track price lead to exponential liquidity decay!
- L(t) ~ L(0) × exp(-λt) for price-chasing strategies
- Each reposition loses value to arbitrageurs
- Losses compound multiplicatively, not additively
- **Implication**: Passive wide-range strategies may preserve long-term wealth better than concentrated active strategies

### Critical Finding 7: Adaptive Fees Validated Empirically (Cao, Kogan et al. 2023)
Structural model on ETH-USDC data confirms:
- Adaptive (volatility-sensitive) fees outperform fixed fees by **9-44% annual revenue**
- Liquidity supply increases **2-10%** under adaptive fees
- Validates theoretical prediction that optimal fee scales with volatility

### Critical Finding 8: LVR = Option Theta (Singh et al. 2025) ⭐⭐ NEW
**Major unifying result**:
- AMM LP position ≡ portfolio of perpetual American continuous-installment options
- LVR is analytically identical to theta (time decay) of at-the-money CI option
- Enables use of established options pricing mathematics for LP analysis
- Can derive LP profiles with approximately **constant LVR** over arbitrarily long horizons
- First infinite time horizon option-theoretic framework for AMMs
