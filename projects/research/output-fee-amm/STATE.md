# Research State — Output-Asset AMM Fees

## Current Focus
**Simulation phase complete.** Core hypothesis validated. Now: empirical backtesting and implementation.

## Research Questions
1. Do any AMMs currently use output-asset fees? **NO - research gap identified**
2. What is the theoretical difference in LP returns? **Theory drafted**
3. How does fee asset choice affect arbitrage dynamics? **Hypothesis: reduces LVR**
4. Impact on impermanent loss and LVR? **To be simulated**
5. Mathematical formulation of output-fee AMM? **THEORY.md drafted**

## Recent Progress
- [2026-02-05] Project created
- [2026-02-05] Literature review: 15+ papers catalogued
- [2026-02-05] **Key finding: NO existing research on output-asset fees**
- [2026-02-05] IDEAS.md: Core hypotheses formulated
- [2026-02-05] THEORY.md: Mathematical framework drafted
- [2026-02-05] Identified Uniswap v4 hooks as implementation path
- [2026-02-07] **Added 2 new papers to INDEX:** Fritz 2025 (IL-LVR regimes), Nezlobin-Tassy 2025 (closed-form LVR)
- [2026-02-07] **Built Monte Carlo simulation** (experiments/simulations/amm_fee_comparison.py)
- [2026-02-07] **KEY RESULT: Output fees reduce LVR by ~6.7%** (1000 simulations, 100% win rate)
- [2026-02-07] **NEW PAPER FOUND:** Herlihy et al. "Defensive Rebalancing for AMMs" (arXiv:2601.19950) — complementary LVR mitigation approach via inter-CFMM transfers
- [2026-02-07] **Created Uniswap v4 hook implementation:** `implementation/code/OutputFeeHook.sol`
- [2026-02-07] **Created test suite:** `implementation/tests/OutputFeeHook.t.sol`
- [2026-02-07] **Added new paper:** Tung et al. "Growth Rate of LP's Wealth in G3Ms" — extends LP theory to general G3Ms
- [2026-02-07] **SENSITIVITY ANALYSIS COMPLETE** — Effect is regime-dependent:
  - Fee 0.3%: 8.2% LVR reduction, 100% win rate
  - Fee 0.1%: 0.3% reduction; Fee 0.5%+: benefit diminishes
  - Volatility 1%: 8.2% reduction; other volatilities: 2-4% reduction
  - **Key insight: Output fee advantage strongest at standard fee levels (0.3%) and moderate volatility**
- [2026-02-07 PM] **THEORY.md updated:** Added formal explanation of regime dependence (fee-to-profit ratio, volatility effects)
- [2026-02-07 PM] Literature search: No new papers found; arXiv:2602.00101 (Formal AMM Fees with Lean 4) already indexed
- [2026-02-07 PM] **Defensive rebalancing comparison:** Created synthesis note comparing output fees with Herlihy et al.'s approach — they are COMPLEMENTARY mechanisms
- [2026-02-07 PM] **Concentrated liquidity analysis:** Created synthesis note exploring how output fees interact with Uniswap v3-style concentrated liquidity — may provide "natural hedge" for range LPs
- [2026-02-07 PM] Literature search: No new papers on output-based fees (gap confirmed); reviewed Campbell 2025 (Optimal Fees) and Feinstein 2025 (Price of Liquidity) — both already indexed
- [2026-02-07 3:30 PM] **CONCENTRATED LIQUIDITY SIMULATION COMPLETE** — see `experiments/simulations/concentrated_liquidity.py`
  - Output fees still win 64-74% of simulations across all range widths
  - LVR reduction scales with in-range time: 0% at ±2.5%, 1.7% at ±50%
  - Key insight: Effect is proportional to trading activity (narrow ranges earn fewer fees)
  - Full-range (±50%) approaches our 6.7% constant-product result
- [2026-02-07 3:30 PM] Literature search: No new papers this week on AMM fees/LVR
- [2026-02-07 4:30 PM] **Created historical backtest framework** (experiments/simulations/historical_backtest.py)
  - Fetches real Uniswap v3 swap data from The Graph subgraph
  - Replays swaps under both fee models for comparison
  - Includes fee sensitivity analysis mode
  - Tested with synthetic data: ~30% LVR reduction (validates core mechanism)
- [2026-02-07 5:30 PM] **Literature search**: Added new paper "Equilibrium Reward for LPs in AMMs" (Aqsha et al., arXiv:2503.22502)
  - Leader-follower game theory model for LP reward design
  - Relevant for understanding how fee structures affect LP behavior
  - "Output fee" search returns zero results — gap strongly confirmed
- [2026-02-07 6:30 PM] **Literature search**: 
  - Added "Automated Liquidity: Market Impact, Cycles, and De-pegging Risk" (Meister, arXiv:2601.11375) — market impact framework for LPs using growth optimization
  - Searched for new LVR/fee mechanism papers — no relevant new findings this week
  - "Output-based fee" searches still return zero results — gap confirmed at 4th check
- [2026-02-07 7:30 PM] **Literature search**: 
  - Checked arXiv, web for new AMM/LVR/fee papers — no new relevant findings
  - "Output fee" / "output-based fee" AMM search: ZERO results (5th confirmation)
  - Reviewed Sandmark toxic flow article (good industry summary, no new research)
  - Found ASRI systemic risk paper (arXiv:2602.03874) — not relevant to fee design
  - **Research gap remains strongly confirmed**

## Key Insights

### Research Gap Confirmed
No academic paper or protocol implements output-asset fees. All AMMs assume input-based fees.

### Core Hypothesis
Output fees may reduce LVR because they directly tax arbitrageur profits (the output token).

### ⭐ SIMULATION RESULT (2026-02-07)
**Output fees reduce LVR by ~6.7% compared to input fees** (at optimal parameters).
- Tested: 1000 Monte Carlo simulations, 10k blocks each
- Output fee wins 100% of the time
- Effect is small but consistent (~0.08% better LP returns)
- Validates core hypothesis: taxing output directly taxes arbitrage profits

### ⭐⭐ REGIME DEPENDENCE (2026-02-07)
**The output fee advantage is parameter-sensitive:**
- **Sweet spot:** 0.3% fee, ~1% block volatility → **8.2% LVR reduction**
- At 0.1% fee: only 0.3% reduction
- At 0.5%+ fees: benefit diminishes or reverses
- At very low/high volatility: reduced effect
- **Implication:** Best suited for standard ETH/USDC-style pools, not exotic pairs

### LP Accumulation Difference
- Input fees → LP accumulates token being SOLD (often the depreciating asset in trends)
- Output fees → LP accumulates token being BOUGHT (the appreciating asset)

### Implementation Path
Uniswap v4 custom accounting hooks can modify swap outputs, enabling output-fee implementation.

## Next Actions
- [x] Build Monte Carlo simulation comparing fee types ✅ (2026-02-07)
- [x] Derive formal LVR formula under output fees ✅ (approximation validated)
- [x] Create Uniswap v4 hook proof-of-concept ✅ (2026-02-07)
- [x] Test sensitivity to fee rate and volatility levels ✅ (2026-02-07)
- [x] Write research note summarizing findings ✅ (2026-02-07)
- [x] Compare with "Defensive Rebalancing" approach ✅ (2026-02-07 PM) — see `synthesis/notes/defensive_rebalancing_comparison.md`
- [x] Analyze concentrated liquidity implications ✅ (2026-02-07 PM) — see `synthesis/notes/concentrated_liquidity_analysis.md`
- [x] Extend Monte Carlo to concentrated liquidity model ✅ (2026-02-07 3:30 PM) — see `synthesis/notes/concentrated_liquidity_simulation_results.md`
- [x] **Draft ethresear.ch post** — see `synthesis/ETHRESEARCH_DRAFT.md` (v0.1)

### Ready for Review
- [ ] **USER REVIEW NEEDED**: Polish ethresear.ch draft for publication
- [ ] **Install Foundry** and run hook tests (`curl -L https://foundry.paradigm.xyz | bash`)
- [~] Backtest on historical Uniswap ETH/USDC data — **framework built**, run: `python3 historical_backtest.py --pool ETH-USDC-0.3%` (blocked: needs Graph Network API key or alternative data source)

### Future Work
- [ ] Model JIT LP behavior under output fees (simulation shows effect diminishes at narrow ranges)
- [ ] Consider academic submission to arXiv or DeFi venue

## Blockers
- **The Graph subgraph deprecated**: Need Graph Network API key or alternative data source (Dune/Flipside/direct RPC) for real historical data
