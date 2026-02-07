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
- [ ] **NEW**: Deep-read Herlihy defensive rebalancing paper (arxiv 2601.19950) — HIGH PRIORITY
- [ ] **NEW**: Analyze feasibility of on-chain convex optimization for rebalancing
- [ ] **NEW**: Compare L1 vs L2 MEV/LVR empirically (use L2 sandwich paper methodology)

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
