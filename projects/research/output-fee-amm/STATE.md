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

## Key Insights

### Research Gap Confirmed
No academic paper or protocol implements output-asset fees. All AMMs assume input-based fees.

### Core Hypothesis
Output fees may reduce LVR because they directly tax arbitrageur profits (the output token).

### ⭐ SIMULATION RESULT (2026-02-07)
**Output fees reduce LVR by ~6.7% compared to input fees.**
- Tested: 1000 Monte Carlo simulations, 10k blocks each
- Output fee wins 100% of the time
- Effect is small but consistent (~0.08% better LP returns)
- Validates core hypothesis: taxing output directly taxes arbitrage profits

### LP Accumulation Difference
- Input fees → LP accumulates token being SOLD (often the depreciating asset in trends)
- Output fees → LP accumulates token being BOUGHT (the appreciating asset)

### Implementation Path
Uniswap v4 custom accounting hooks can modify swap outputs, enabling output-fee implementation.

## Next Actions
- [x] Build Monte Carlo simulation comparing fee types ✅ (2026-02-07)
- [x] Derive formal LVR formula under output fees ✅ (approximation validated)
- [x] Create Uniswap v4 hook proof-of-concept ✅ (2026-02-07)
- [ ] Set up Foundry project and run hook tests
- [ ] Backtest on historical Uniswap ETH/USDC data
- [ ] Write research note summarizing findings
- [ ] Test sensitivity to fee rate and volatility levels
- [ ] Analyze concentrated liquidity (Uni v3 style) implications
- [ ] Compare with "Defensive Rebalancing" approach (new paper)

## Blockers
None
