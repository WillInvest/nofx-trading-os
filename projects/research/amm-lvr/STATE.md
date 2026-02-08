# Research State — AMM LVR Mitigation

## Current Focus

**Phase 1: Literature Review — COMPLETE ✅**
**Phase 2: Deep Reading & Synthesis — IN PROGRESS**

Focus on:
1. Deep-read FM-AMM paper (Canidio & Fritsch 2023)
2. Analyze CoW AMM production implementation
3. Study Angstrom hook architecture
4. Model threshold-dynamic fee strategies

## Research Questions

### Primary
How can AMM design be improved to reduce LP losses from adverse selection (LVR) while maintaining decentralization and capital efficiency?

### Sub-questions
1. What is the theoretical lower bound on LVR for CFMMs? **→ LVR = σ²/8 × L × dt**
2. How much LVR can oracle-based pricing eliminate? **→ ~100% if oracle accurate**
3. Can dynamic fees fully capture arbitrage surplus? **→ ~50-80% with good thresholds**
4. Does batching orders help LPs? **→ YES, FM-AMM eliminates LVR**
5. Are there curve designs that naturally resist LVR? **→ Not really; curve shape ≠ LVR**
6. Can hybrid designs reduce adverse selection? **→ Promising: Oracle + Batch + Fees**

## Recent Progress

- [2026-02-04] Project created
- [2026-02-04] **Comprehensive literature sweep COMPLETE**
  - 25+ papers/sources catalogued
  - 6 solution categories identified
  - Gap analysis completed
  - INDEX.md, IDEAS.md, THEORY.md populated
- [2026-02-07] **Daily research update**
  - Found 2 new relevant papers:
    1. Bartoletti et al. (2026) — Formal AMM fee verification in Lean 4
    2. Volatility Buffering paper (Computational Economics) — V-S pool buffering effect
  - Added 3 new ideas: size-dependent fees, volatility-aware vault, AR-based fee adjustment
  - Updated theory with fee non-additivity proof and IL forecasting model
- [2026-02-07] **Daily research update #2** ⭐
  - Found 2 significant new papers:
    1. **Herlihy (2026) — Defensive Rebalancing** [arXiv:2601.19950]
       - Major new framework: multi-pool coordination beats single-pool defense
       - Pareto efficiency ⟺ arbitrage-free (beautiful result)
       - Optimal rebalancing is convex optimization
    2. **Gogol et al. (2026) — L2 Sandwich Analysis** [arXiv:2601.19570]
       - L2 private mempools make sandwiching unprofitable
       - Median L2 sandwich return is negative
       - Good news for rollup-based AMM deployments
  - Added 3 new ideas: coordinated CFMM coalition, rebalancing DAO, L2-native LVR-resistant AMM
  - Key insight: multi-pool coordination is an unexplored design space
- [2026-02-07] **Daily research update #3** (afternoon)
  - Light week for new academic papers — no major LVR-specific publications
  - Added **Sandmark "Toxic Flow" article** — excellent industry summary:
    - Wu et al. 2025 data: Wintermute + SCP + Kayle = 90% of Q1 2025 arbitrage value
    - Confirms concentration of MEV extraction in few actors
  - Added **arXiv 2602.00776** (Bieganowski) — crypto microstructure study
    - Flash crash analysis validates adverse selection theory empirically
    - Useful for future empirical validation of our work
  - No blockers; continuing deep-read phase
- [2026-02-07] **Daily research update #4** (Saturday)
  - Light week continues — no new LVR-specific papers found
  - **Industry development**: Uniswap CCA (Continuous Clearing Auctions) on Base
    - Similar to FM-AMM concepts but for token launches
    - Block-by-block price discovery with automatic v4 pool seeding
    - Aztec Network raised $59-61M using CCA — $557M FDV, 16,700+ participants
    - **Relevance**: Validates batch auction approach for fair pricing
  - **New tangential papers catalogued**:
    - arXiv 2602.03874 (ASRI) — Aggregated Systemic Risk Index for DeFi
    - arXiv 2602.01317 (TxRay) — Agentic postmortem system for DeFi exploits
  - Deep-read phase continues; focus remains on FM-AMM and Herlihy papers
- [2026-02-08] **Daily research update #5** (Saturday afternoon)
  - Searched for new papers: LVR, impermanent loss, CoW AMM, Angstrom, dynamic fees
  - **No significant new LVR-specific papers this week** — quiet period
  - **New tangential paper added**:
    - arXiv 2602.03981 (DeXposure-FM) — Foundation model for DeFi credit exposure
    - First time-series graph model for inter-protocol exposure forecasting
    - Useful for systemic risk monitoring context
  - Reviewed recent q-fin arXiv listings — nothing LVR-related
  - Sandmark "Toxic Flow" article continues to be most cited recent industry piece
  - **Status**: Deep-read phase ongoing; awaiting new research to synthesize
- [2026-02-08] **Daily research update #6** (Saturday evening)
  - Found **2 important papers** previously missed in arXiv scans:
    1. **Singh et al. (2025) — LVR = Theta** [arXiv:2508.02971]
       - Major theoretical result: LVR is identical to theta of embedded CI option
       - Provides framework for constant-LVR LP position optimization
       - Actionable: LPs can now target specific adverse selection costs
    2. **Bichuch & Feinstein (2026) — LP as Derivative** [arXiv:2409.11339, v4]
       - Black-Scholes-like framework for LP token pricing
       - Shows on-chain LP prices may be mispriced vs. risk-neutral valuation
       - Method to calibrate implied LP volatility
  - Added 7 new ideas (#17-23) to synthesis:
    - Constant-LVR vaults, LVR insurance pricing, term-structure fees
    - LP token arbitrage, implied LP vol signals, full Greeks dashboard
    - Automated LP hedging protocol
  - **Key insight**: Option-theoretic framing of LVR is maturing rapidly
  - Industry searches: Quiet week; no major new implementations announced
- [2026-02-07] **Daily research update #7** (Saturday)
  - Searched: LVR, impermanent loss, dynamic fees AMM, CoW AMM, Angstrom Sorella
  - Reviewed arXiv q-fin recent submissions (Feb 3-6, 2026)
  - **No new LVR-specific academic papers this week**
  - Recent q-fin papers focused on: insurance pricing, skew stickiness, VaR conformal control
  - Industry: Uniswap v4 adoption continues (~9 hook integrations targeted by April '26)
  - **Status**: Quiet research week; continuing deep-read phase on existing priority papers
- [2026-02-07] **Daily research update #8** (Saturday afternoon/evening)
  - Found **1 new relevant paper**:
    1. **Meister (2026) — Automated Liquidity** [arXiv:2601.11375]
       - Novel thermodynamic perspective: CPMM as Carnot engine
       - Derives square-root market impact (breaks linearized models)
       - "Entropy leak" = LVR under this framework
       - Stablecoin depeg as catastrophe risk
  - **Major industry developments**:
    1. **Whetstone Research / Doppler**: $9M Seed led by Pantera Capital
       - Founded by Austin Adams (am-AMM paper author, ex-Uniswap)
       - Price discovery auctions with sniper prevention
       - 40K+ assets/day, $1.5B+ value
       - Validates batch auction approach in production
    2. **Sorella Labs**: $5.2M additional funding (total $12.4M)
       - Continued investment in Angstrom development
  - Added 6 new ideas (#24-29) to synthesis:
    - Thermodynamic efficiency metric, non-linear impact curves
    - Catastrophe-theoretic depeg insurance
    - am-AMM → Doppler production pipeline
    - Integrated token lifecycle LVR management
    - Unified LVR theory (multi-framework convergence)
  - **Key insight**: All recent theoretical advances (Singh, Bichuch, Meister, Milionis) converge on treating LPs as derivative holders — LVR = theta/entropy/adverse selection under different lenses
- [2026-02-07] **Daily research update #9** (Saturday evening, 6:15 PM)
  - Searched: LVR AMM, impermanent loss mitigation, dynamic fees AMM, CoW AMM, Angstrom Sorella
  - Reviewed arXiv q-fin recent submissions (Feb 3-7, 2026)
  - **No new LVR-specific academic papers this week**
  - Recent q-fin papers: skew stickiness (Fukasawa), fair insurance pricing, grocery retail — none DeFi-related
  - Industry: Quiet week for announcements; Sorella $5.2M funding already captured
  - **Status**: Literature coverage is comprehensive; continuing deep-read phase on priority papers
  - Confirmed Sandmark "Toxic Flow" article remains the most-cited recent industry summary
- [2026-02-07] **Daily research update #10** (Saturday evening, 7:15 PM)
  - Searched all key terms: LVR, impermanent loss, dynamic fees, CoW AMM, Angstrom Sorella
  - Reviewed arXiv q-fin submissions through Feb 7, 2026
  - **No new LVR-specific academic papers**
  - Recent q-fin papers reviewed: trimming/voting, skew stickiness, fair insurance pricing, DiffLOB (counterfactual LOB generation) — none AMM-related
  - **Industry development**: Bitwise filed S-1 for Uniswap ETF with SEC
    - Major institutional interest signal
    - First direct attempt to bring DEX exposure to traditional markets
    - Regulatory review expected to be lengthy
    - If approved: validates DeFi as institutional asset class
  - **Status**: Literature comprehensive; quiet academic week; deep-read phase continues

## Key Findings from Literature Review

### Solution Categories (ranked by promise)
1. **FM-AMM / Batch Auctions** — Eliminates LVR; production-ready (CoW AMM)
2. **Angstrom/Hook-Based** — Native Uniswap v4 MEV protection; live
3. **Dynamic Fees + Oracle** — Near-optimal theoretically; emerging
4. **Oracle-Based Pricing** — Works but trust required
5. **Hedging** — External solution; capital-intensive
6. **Insurance** — Unsustainable (Bancor lesson)

### Breakthrough Papers
- **Milionis et al. 2022**: LVR formula (foundational)
- **Canidio & Fritsch 2023**: FM-AMM proves LVR elimination possible
- **Campbell et al. 2025**: Threshold fees are near-optimal

### Gap Identified
**No existing solution is fully:**
- Trustless (no oracle/solver/sequencer trust)
- Permissionless
- Capital efficient
- Production ready

### Connection to FBA Project
Threshold encryption for fair ordering could enable trustless batch auctions!
See `../onchain-fba/` for potential synergy.

## Next Actions

- [ ] Deep-read FM-AMM paper (arxiv 2307.02074)
- [ ] Review CoW AMM GitHub implementation
- [ ] Study Angstrom hook code
- [ ] Model dynamic fee thresholds with historical data
- [ ] Write comparison analysis: CoW AMM vs Angstrom vs Swaap
- [ ] Explore encryption-based trustless batching
- [ ] Model size-dependent fee schedules (from Bartoletti insight)
- [ ] Backtest AR-based fee adjustment using IL autoregressive structure
- [ ] Deep-read Herlihy defensive rebalancing paper (arxiv 2601.19950) — HIGH PRIORITY
- [ ] Analyze feasibility of on-chain convex optimization for rebalancing
- [ ] Compare L1 vs L2 MEV/LVR empirically (use L2 sandwich paper methodology)
- [ ] **NEW**: Deep-read Singh CI option paper (arxiv 2508.02971) — theoretical foundation
- [ ] **NEW**: Implement constant-LVR boundary calculator
- [ ] **NEW**: Prototype LP Greeks dashboard concept
- [ ] **NEW**: Investigate LP token secondary markets for arbitrage feasibility
- [ ] **NEW**: Study Meister thermodynamic framework — implications for AMM design
- [ ] **NEW**: Analyze Doppler mechanism (Austin Adams' production implementation of am-AMM ideas)
- [ ] **NEW**: Develop unified LVR framework connecting options/entropy/adverse selection perspectives

## Blockers

None currently.

## Key Insights

1. **LVR is the "true cost"** — IL is just discrete sampling; LVR is continuous
2. **Batching works** — FM-AMM proves competition eliminates arbitrage profit
3. **Fees alone are insufficient** — Need ~σ information to set optimal fees
4. **Production solutions exist** — CoW AMM, Angstrom, Swaap are live
5. **Trust trade-offs everywhere** — Oracle vs Solver vs Sequencer
6. **Multi-pool coordination is unexplored** — Herlihy's defensive rebalancing suggests pools should cooperate, not just individually defend
7. **L2s may naturally resist MEV** — Private mempools make sandwiching unprofitable (good news!)
8. **LVR = Theta (option theory)** — Singh proves LVR is the time decay of an embedded exotic option; enables predictable, targetable adverse selection costs
9. **Thermodynamic perspective (Meister)** — CPMM as Carnot engine; LVR = "entropy leak"; suggests linearized liquidity models underestimate true costs
10. **Theoretical convergence** — Options (theta), thermodynamics (entropy), microstructure (adverse selection) all describe same phenomenon from different angles; unified framework emerging
