# Research State — AMM LVR Mitigation

## Current Focus

**Phase 1: Literature Review — COMPLETE ✅**
**Phase 2: Deep Reading & Synthesis — IN PROGRESS**
**Phase 2b: Unified Theory Framework — DRAFT COMPLETE ✓**

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

- [2026-02-08] **Daily research update #18** (Sunday, 3:15 AM)
  - Searched all key terms: LVR AMM, impermanent loss mitigation, dynamic fees AMM, CoW AMM, Angstrom Sorella
  - Reviewed arXiv q-fin.TR recent submissions (Feb 7-8, 2026): No new AMM/LVR papers this window
  - **Found 1 significant paper previously not indexed:**
    1. **Menasché et al. (AFT 2025) — JIT Liquidity Analysis** [arXiv:2509.16157]
       - First formal transaction-level model of Just-In-Time (JIT) LP behavior in CLMMs
       - Optimal JIT strategy proven to exist; current JIT bots suboptimal by ~69%
       - **Key finding**: JIT erodes passive LP profits by up to 44% per trade
       - JIT improves market efficiency (lower slippage) but at passive LP expense
       - Reveals passive LPs face **dual threat**: arbitrageurs (LVR) AND sophisticated LPs (JIT)
  - Added 3 new ideas (#38-40) to synthesis: JIT-resistant design, defensive withdrawal, am-AMM extension for JIT
  - Updated protection stack: Added Layer 5 (time-weighted fees to neutralize JIT)
  - **Industry searches**: Quiet week continues; no major new implementations announced
  - **Status**: Literature comprehensive; JIT paper fills important gap in LP threat model
- [2026-02-08] **Daily research update #17** (Sunday, 2:15 AM)
  - Searched all key terms: LVR AMM, impermanent loss mitigation, dynamic fees AMM, CoW AMM, Angstrom Sorella
  - Reviewed arXiv q-fin.TR recent submissions (Feb 6-7, 2026): No new AMM/LVR papers
  - **Found 3 significant papers previously not indexed:**
    1. **Bergault et al. (2025) — Optimal Exit Time** [arXiv:2509.06510]
       - LP exit as optimal stopping problem with HJB quasi-variational inequality
       - Derives optimal fee level given exit strategy; key for LP management
    2. **Brini et al. (2025) — DRL for Efficient LP** [arXiv:2501.07508]
       - PPO-trained agent for Uniswap v3 position management
       - Accepted at AAAI 2025 Workshop; practical implementation
    3. **Berezovskiy (2025) — τ-Reset Strategies** [arXiv:2505.15338]
       - ML-based optimal LP in CLMMs; novel historical liquidity approximation
       - Custom backtesting framework for concentrated liquidity
  - **Industry update**: CoW DAO transferred MEV Blocker RPC to Consensys SMG
    - 4.5M users, 6,177 ETH returned; CoW focusing on core protocol MEV capabilities
    - Institutional (Consensys) backing signals MEV protection maturation
  - Added 6 new ideas (#32-37) to synthesis: Optimal exit protocol, DRL vaults, τ-reset framework
  - Identified synthesis opportunity: Complete LP management stack (entry → management → exit)
  - **Status**: Literature comprehensive; found 3 important optimization papers; quiet week for new LVR-specific research
- [2026-02-08] **Daily research update #16** (Sunday, 1:16 AM)
  - Searched all key terms: LVR AMM, impermanent loss mitigation, dynamic fees AMM, CoW AMM, Angstrom Sorella
  - Reviewed arXiv q-fin new submissions (Feb 6, 2026): 4 new papers + 2 cross-lists
    - 2602.05155 (network-based insurance — not AMM)
    - 2602.05898 (rough path signatures — math finance, not AMM)
    - Reviewed replacements: 2601.20336 (whitepaper narrative analysis — tangential)
  - **No new LVR-specific academic papers** — quiet period continues (3rd consecutive week)
  - **Industry update**: Coin Bureau DEX roundup (Feb 8) reconfirms: "Uniswap V4 hooks and Balancer V3 weighted pools allow dynamic fee models, concentrated liquidity, and programmable strategies that rival institutional-grade systems"
  - **Status**: Literature comprehensive; deep-read phase ongoing; academic quiet period
  - Next priority: Begin implementation experiments with MEV tax hook on testnet
- [2026-02-08] **Daily research update #15** (Sunday, 12:15 AM)
  - Searched all key terms: LVR AMM, impermanent loss mitigation, dynamic fees AMM, CoW AMM, Angstrom Sorella
  - Reviewed arXiv q-fin submissions (Feb 3-7, 2026): 63 total papers
    - 2602.05542 (voting), 2602.05241 (skew), 2602.05112 (bioeconomy), 2602.05007 (music royalties), 2602.04464 (grocery retail), 2602.03884 (labor economics) — none DeFi/AMM related
  - **No new LVR-specific academic papers this week** — quiet period continues (3rd consecutive week)
  - **Industry notes**:
    - Coin Bureau DEX roundup updated (Feb 7): Confirms v4 hooks + dynamic fees as "converging best practices"
    - xAI hiring crypto experts for MEV/market microstructure AI training
    - Flashbots Protect milestone: 2.1M unique accounts protected, $43B DEX volume, 313 ETH refunded via MEV-Share
    - Aster L1 testnet launched; mainnet expected Q1 2026 (MEV protection as selling point)
    - nasscom DEX overview confirms hybrid AMM + order book models emerging in 2026
  - **Status**: Literature comprehensive; 3rd quiet academic week; deep-read phase ongoing
  - Next priority: Begin implementation experiments with MEV tax hook on testnet
- [2026-02-07] **Daily research update #14** (Saturday, 11:15 PM)
  - Searched all key terms: LVR AMM, impermanent loss mitigation, dynamic fees AMM, CoW AMM, Angstrom Sorella
  - Reviewed arXiv q-fin submissions (Feb 3-6, 2026): 63 total papers
    - 2602.05542 (voting), 2602.05241 (skew), 2602.05112 (bioeconomy), 2602.05007 (music royalties), 2602.03903 (VaR conformal) — none DeFi/AMM related
  - Reviewed ethresear.ch — no new LVR posts since mid-2024
  - **No new LVR-specific academic papers this week** — very quiet period
  - **Industry notes**:
    - Coin Bureau DEX roundup (Feb 7): Confirms v4 hooks + dynamic fees as converging best practice
    - xAI hiring crypto experts for MEV/market microstructure AI training
  - **Status**: Literature comprehensive; quiet academic week; deep-read phase continues
  - Next priority: Begin implementation experiments with MEV tax hook on testnet
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
- [2026-02-07] **Daily research update #11** (Saturday evening, 8:15 PM)
  - Searched all key terms: LVR, impermanent loss, dynamic fees, CoW AMM, Angstrom Sorella
  - Reviewed arXiv q-fin Feb 5-6 submissions — none DeFi/AMM related
  - **Added missing foundational reference**: Paradigm "Priority Is All You Need" (June 2024)
    - MEV tax mechanism: AMMs capture LVR by charging fees proportional to priority fee
    - Works on OP Stack L2s today (Base, OP Mainnet, Blast)
    - Key insight: No oracle or batching needed — just fee = f(priority_fee)
    - Added to INDEX.md under Dynamic Fees section
  - **New ideas added** (#30-31): Priority-fee-based LVR capture, hybrid MEV tax + dynamic fee
  - **Industry notes**:
    - Unichain uses Flashbots verifiable builder in TEE for MEV mitigation
    - Optimism Superchain buyback program passed (50% sequencer revenue → OP buybacks)
  - **Status**: Literature comprehensive; added important missing Paradigm reference
- [2026-02-07] **Daily research update #12** (Saturday, 9:15 PM)
  - Searched all key terms: LVR AMM, impermanent loss mitigation, dynamic fees AMM, CoW AMM, Angstrom Sorella
  - Reviewed arXiv q-fin submissions (Feb 3-6, 2026):
    - 2602.05542: Trimming extreme votes — not relevant
    - 2602.05241: Skew stickiness ratio (Fukasawa) — TradFi vol modeling, not AMM
    - 2602.04791: Fair pricing in long-term insurance — not relevant
    - 2602.03776: DiffLOB (diffusion for LOB counterfactuals) — interesting generative modeling for order books, but not AMM-specific
  - **No new LVR-specific academic papers this week**
  - **Industry notes**:
    - **Flow Network milestone**: 40M users, 950M transactions; touting MEV resistance as key DeFi feature
    - **VibeSwap proposal on Nervos**: "Fair price discovery as a human right" — MEV-resistant DEX concept
    - **Coin Bureau DEX roundup** confirms industry trend: CoW Protocol batch auctions + Uniswap v4 hooks + dynamic fees = converging best practices
  - **Status**: Quiet academic week; deep-read phase continues; literature coverage comprehensive
- [2026-02-07] **Daily research update #13** (Saturday, 10:15 PM)
  - Searched all key terms: LVR AMM, impermanent loss mitigation, dynamic fees AMM, CoW AMM, Angstrom Sorella
  - Reviewed arXiv q-fin.TR recent submissions (Feb 3-7, 2026):
    - 2601.23172: Unified theory of order flow (Szymanski) — market microstructure, not AMM-specific
    - 2602.00082: LLM multi-agent for REITs — not relevant to LVR
    - Papers already in INDEX confirmed (2602.00776, 2602.00101)
  - **No new LVR-specific academic papers this week** — quiet period continues
  - **Industry developments**:
    - **1inch Aqua launched**: Shared liquidity layer addressing LP efficiency/utilization
      - Research claims 83-95% of DeFi liquidity sits idle ($12B underutilized)
      - Focus on utilization, not LVR — complements LVR solutions
      - Introduces "TVU" (Total Value Unlocked) metric vs TVL
    - **UNIfication passed**: Uniswap fee switch now active with UNI burn mechanism
    - Uniswap v4 hooks adoption continues; dynamic fee hooks in production
  - **Status**: Very quiet academic week; no new papers to add; deep-read phase ongoing

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
- [ ] **NEW**: Prototype MEV tax hook for Uniswap v4 on OP Stack (from Paradigm "Priority Is All You Need")
- [ ] **NEW**: Compare MEV tax vs FM-AMM vs dynamic fees — which captures more LVR?
- [ ] **NEW**: Study Bergault optimal exit framework — implement numerical solver
- [ ] **NEW**: Evaluate DRL LP agent (Brini) feasibility for vault deployment
- [ ] **NEW**: Design complete LP lifecycle management protocol (entry → management → exit)
- [ ] **NEW**: Deep-read JIT liquidity paper (arxiv 2509.16157) — understand optimal JIT strategy
- [ ] **NEW**: Model combined LVR + JIT impact on passive LP profitability
- [ ] **NEW**: Prototype time-weighted fee distribution hook to neutralize JIT

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
11. **JIT = Second LP threat** — Menasché et al. prove JIT liquidity erodes passive LP profits by up to 44% per trade, separate from LVR. Passive LPs face dual threat from arbitrageurs AND sophisticated LPs.
