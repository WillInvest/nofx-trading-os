# Literature Index — AMM LVR Mitigation

## Categories
- [Foundational Theory](#foundational-theory)
- [Oracle-Based AMMs](#oracle-based-amms)
- [Batch/Auction-Based AMMs](#batchauction-based-amms)
- [Dynamic Fees](#dynamic-fees)
- [Novel AMM Designs](#novel-amm-designs)
- [Insurance/Compensation](#insurancecompensation)
- [Hedging Strategies](#hedging-strategies)
- [Production Protocols](#production-protocols)
- [Survey/Overview](#surveyoverview)

---

## Foundational Theory

### Automated Market Making and Loss-Versus-Rebalancing (Milionis et al., 2022)
- **arXiv**: 2208.06046
- **URL**: https://arxiv.org/abs/2208.06046
- **Authors**: Jason Milionis, Ciamac Moallemi, Tim Roughgarden, Anthony Lee Zhang
- **Key contribution**: Introduces LVR as the "Black-Scholes for AMMs" — formalizes LP adverse selection cost
- **Core insight**: LVR = σ²/8 * L per unit time (for constant-product AMM)
- **Relevance**: THE foundational paper; all solutions benchmark against this

### Automated Market Making and Arbitrage Profits in the Presence of Fees (Milionis et al., 2023)
- **URL**: https://moallemi.com/ciamac/papers/lvr-fee-model-2023.pdf
- **Key contribution**: Extends LVR model to include swap fees
- **Core insight**: Fees can partially offset LVR but cannot eliminate it under continuous trading

### Impermanent Loss and Loss-vs-Rebalancing II (2025)
- **arXiv**: 2502.04097v2
- **URL**: https://arxiv.org/html/2502.04097v2
- **Key contribution**: Statistical properties of IL vs LVR, impact of fees and block times
- **Core insight**: Continuous-time limit analysis; block time affects LVR extraction rate

---

## Oracle-Based AMMs

### UAMM: Price-oracle based Automated Market Maker (Im et al., 2023)
- **arXiv**: 2308.06375
- **URL**: https://arxiv.org/abs/2308.06375
- **Key contribution**: AMM that uses oracle prices to set swap prices
- **Core insight**: Eliminates arbitrage when oracle prices are efficient
- **Limitation**: Trust in oracle; oracle latency creates brief arbitrage windows
- **Relevance**: Direct approach — if you trust oracles, LVR vanishes

### Dynamic Curves for Decentralized Autonomous Cryptocurrency Exchanges (2021)
- **URL**: https://drops.dagstuhl.de/storage/01oasics/oasics-vol092-fab2021/OASIcs.FAB.2021.5/OASIcs.FAB.2021.5.pdf
- **Venue**: FAB 2021 (Financial Cryptography)
- **Key contribution**: Bonding curve adjusted by oracle price feed
- **Core insight**: Pool price = market price → no arbitrage opportunity
- **Limitation**: Requires high-frequency oracle updates

### Dynamic Automated Market Makers (USC)
- **URL**: https://anrg.usc.edu/www/papers/dynamicautomation.pdf
- **Key contribution**: Continuous curve adjustment to market price
- **Core insight**: No room for arbitrage benefits both LPs and traders

---

## Batch/Auction-Based AMMs

### Arbitrageurs' profits, LVR, and sandwich attacks: batch trading as an AMM design response (Canidio & Fritsch, 2023)
- **arXiv**: 2307.02074
- **URL**: https://arxiv.org/abs/2307.02074
- **Venue**: AFT 2023
- **Key contribution**: FM-AMM (Function-Maximizing AMM) — batches trades, eliminates LVR
- **Core insight**: Competition between arbitrageurs in batch → fair price discovery
- **Breakthrough**: Proves LVR elimination is possible without oracles!
- **Relevance**: Theoretical foundation for CoW AMM

### am-AMM: An Auction-Managed Automated Market Maker (Adams et al., 2024)
- **arXiv**: 2403.03367
- **URL**: https://arxiv.org/abs/2403.03367
- **Authors**: Austin Adams, Ciamac Moallemi
- **Key contribution**: Harberger lease auction for pool management rights
- **Core insight**: Manager pays rent to LPs, captures arbitrage, sets dynamic fees
- **Trade-off**: Complexity; requires active manager market

### MEV capturing AMM (McAMM) (Herrmann, 2022)
- **URL**: https://ethresear.ch/t/mev-capturing-amm-mcamm/13336
- **Key contribution**: Auction first-trade-of-block rights
- **Core insight**: LVR extraction is predictable → can auction it

---

## Dynamic Fees

### Priority Is All You Need: MEV Taxes (Robinson & White, Paradigm, 2024) ⭐ NEW
- **URL**: https://www.paradigm.xyz/2024/06/priority-is-all-you-need
- **Authors**: Dan Robinson, Dave White (Paradigm)
- **Date**: June 2024
- **Key contribution**: Introduces MEV taxes — applications capture their own MEV by charging fees as function of priority fee
- **Core insights**:
  - On chains with competitive priority ordering (OP Stack L2s), apps can tax searchers
  - AMMs can charge `applicationFee = 99 × priorityFee` to capture 99% of MEV
  - Works without oracles or custom infrastructure — hooks into block proposer's auction
  - Can mitigate DEX router slippage, AMM LVR, and backrunning
- **Limitation**: Requires trusted priority ordering (centralized sequencer today)
- **Implementation**: Already possible on OP Mainnet, Base, Blast
- **Relevance**: Direct mechanism for AMMs to capture LVR without oracle trust
- **Connection to LVR**: "allowing AMMs to reduce the arbitrage losses of their LPs" — explicit use case

### Optimal Fees for Liquidity Provision in AMMs (Campbell, Bergault, Milionis, Nutz, 2025)
- **arXiv**: 2508.08152
- **URL**: https://arxiv.org/abs/2508.08152
- **Key contribution**: Rigorous optimal fee calculation framework
- **Core insight**: Optimal fee ≈ CEX trading cost normally; spike during volatility
- **Implication**: Threshold-type dynamic fees are near-optimal
- **Relevance**: Theoretical backing for Uniswap v4 dynamic fee hooks

### Optimal Dynamic Fees in Automated Market Makers (2025)
- **arXiv**: 2506.02869
- **URL**: https://arxiv.org/html/2506.02869v2
- **Key contribution**: Fee optimization under continuous-time dynamics
- **Core insight**: Dynamic fees linear in inventory + price-sensitive are good approximation

---

## Novel AMM Designs

### Maverick AMM — Dynamic Distribution AMM
- **Docs**: https://docs.mav.xyz/
- **Key contribution**: Directional liquidity + automated reconcentration
- **Core insight**: LP can bet on price direction; AMM follows price to capture fees
- **Modes**: Left, Right, Both, Static
- **Maverick v2**: Adds directional fees (asymmetric by swap direction)
- **Relevance**: Doesn't eliminate LVR but maximizes fee capture

### Ambient (CrocSwap) — Hybrid Concentrated + Ambient Liquidity
- **Docs**: https://docs.ambient.finance/
- **GitHub**: https://github.com/CrocSwap/CrocSwap-protocol
- **Key contribution**: Single-contract architecture; ambient + concentrated + knockout liquidity
- **Core insight**: Ambient liquidity auto-compounds; low gas; flexible strategies
- **Relevance**: Efficiency gains, not direct LVR mitigation

### Angstrom by Sorella Labs — Uniswap v4 Hook
- **URL**: https://sorellalabs.xyz/writing/introducing-sorella
- **GitHub**: https://github.com/sorellaLabs/Angstrom
- **Audit**: Cantina
- **Key contribution**: Native MEV protection via Uniswap v4 hook
- **Core insight**: Groups all transactions of an asset at same price per block
- **Status**: Live on mainnet (July 2025)
- **Funding**: $7.5M seed (Paradigm)
- **Relevance**: Production MEV/LVR protection integrated with Uniswap

---

## Insurance/Compensation

### Bancor v3 — Impermanent Loss Protection
- **Docs**: https://docs.bancor.network/
- **GitHub**: https://github.com/bancorprotocol/contracts-v3
- **Key contribution**: 100% IL protection via BNT minting
- **Mechanism**: Protocol-held liquidity compensates LPs for IL
- **Limitation**: Depends on BNT token value; paused IL protection in June 2022 bear market
- **Lesson**: Insurance model breaks under extreme market stress

---

## Hedging Strategies

### Unified Approach for Hedging Impermanent Loss of Liquidity Provision (2024)
- **arXiv**: 2407.05146
- **URL**: https://arxiv.org/html/2407.05146v1
- **Key contribution**: IL protection claim — financial instrument to hedge IL
- **Core insight**: IL = short a portfolio of puts and calls (Fukasawa et al.)
- **Implication**: Can hedge statically with options basket

### Hedging IL with Power Perpetuals (Deri Protocol)
- **URL**: https://deri-protocol.medium.com/hedging-impermanent-loss-with-power-perpetuals-2d54c16d6a23
- **Key contribution**: Gamma hedging via power perpetuals (e.g., Squeeth)
- **Core insight**: LP position has negative gamma; buy positive gamma to hedge
- **Limitation**: Requires active rebalancing; hedging costs

### Dynamic Hedging Strategies for Uniswap v3
- **URL**: https://atise.medium.com/liquidity-provider-strategies-for-uniswap-v3-dynamic-hedging-9e6858bea8fa
- **Key contribution**: Practical hedging with options + perpetuals
- **Core insight**: LPs profitable when fee income > σ² loss (volatility drag)

---

## Production Protocols

### CoW AMM (CoW Protocol)
- **Docs**: https://docs.cow.fi/cow-amm
- **GitHub**: https://github.com/cowprotocol/cow-amm
- **Status**: Production on Ethereum mainnet
- **Key contribution**: First production FM-AMM implementation
- **Mechanism**: Batch auctions via CoW Protocol solvers
- **Result**: Zero swap fees; surplus → LPs instead of arbitrageurs
- **Limitation**: Relies on CoW Protocol infrastructure

### Swaap Finance — Market-Neutral AMM
- **URL**: https://www.swaap.finance/
- **Network**: Polygon, Ethereum
- **Key contribution**: Oracle + dynamic spread → no IL
- **Mechanism**: Chainlink feeds determine prices; spread adapts to volatility
- **Status**: Live, growing TVL
- **Limitation**: Oracle dependency

### Uniswap v4 — Hook-Based Customization
- **Docs**: https://docs.uniswap.org/contracts/v4/overview
- **Key contribution**: Modular AMM via hooks at swap/LP lifecycle points
- **LVR-relevant hooks**: Dynamic fees, custom accounting, TWAMM
- **Ecosystem**: Angstrom, various dynamic fee hooks
- **Status**: Mainnet 2024

---

## Survey/Overview

### Current Understanding of Impermanent Loss Risk in AMMs (2025)
- **URL**: https://www.sciencedirect.com/science/article/pii/S2096720925000879
- **Key contribution**: Systematic literature review
- **Finding**: 55.7% of research focuses on CPMMs
- **9 IL causes**: Price volatility (top), asset imbalance, risk/return management
- **Mitigation strategies**: Investment strategies, decentralized tools, pool design, hedging

### Ending LP's Losing Game (Fenbushi VC, 2024)
- **URL**: https://fenbushi.vc/2024/01/20/ending-lps-losing-game-exploring-the-loss-versus-rebalancing-lvr-problem-and-its-solutions/
- **Key contribution**: Practitioner overview of LVR solutions
- **Approaches covered**: McAMM, dynamic fees, oracle-based, batch auctions

### The AMM Renaissance (Arrakis Finance)
- **URL**: https://arrakis.finance/blog/the-amm-renaissance-how-mev-auctions-and-dynamic-fees-prevent-lvr
- **Key contribution**: Industry perspective on LVR solutions
- **Coverage**: Dynamic fees, MEV auctions, Sorella Angstrom

---

## Key Papers to Deep-Read

1. **Milionis et al. 2022** (LVR) — foundational theory
2. **Canidio & Fritsch 2023** (FM-AMM) — batch auction solution
3. **Campbell et al. 2025** (Optimal Fees) — dynamic fee theory
4. **Adams et al. 2024** (am-AMM) — auction-managed design
5. **Im et al. 2023** (UAMM) — oracle-based approach

---

## Gap Analysis

| Approach | LVR Eliminated? | Trust Required | Capital Efficient | Production Ready |
|----------|----------------|----------------|-------------------|------------------|
| Standard CFMM | ❌ No | ✅ None | ✅ Yes | ✅ Yes |
| Oracle-based | ✅ Yes* | ❌ Oracle | ✅ Yes | ⚠️ Partial |
| FM-AMM/Batch | ✅ Yes | ⚠️ Solver/sequencer | ⚠️ Latency | ✅ CoW AMM |
| Dynamic Fees | ⚠️ Partial | ✅ None | ✅ Yes | ⚠️ Emerging |
| Auction Rights | ✅ Yes | ⚠️ Auction mechanism | ✅ Yes | ❌ Concept |
| Insurance | ❌ (compensates) | ⚠️ Protocol solvency | ✅ Yes | ⚠️ Risky |
| Hedging | ❌ (external) | ⚠️ Derivatives market | ❌ Capital cost | ✅ Yes |

*When oracle is accurate and timely

---

## Research Frontier

**Open questions:**
1. Can dynamic fees fully capture LVR without external price information?
2. What is the optimal batch duration for FM-AMMs?
3. Can Angstrom-style hooks scale to high-volume pairs?
4. Is there a pure on-chain solution without any trust assumptions?
5. Can concentrated liquidity + dynamic fees outperform FM-AMM?

**Promising directions:**
- **Hybrid oracle + batch**: Use oracle for continuous pricing, batch for rebalancing
- **Priority ordering exploitation**: Paradigm's MEV tax concept
- **Threshold-dynamic fees**: Near-optimal with simple implementation

---

## New Additions (2026-02-08, Update #3)

### Optimal Exit Time for Liquidity Providers in Automated Market Makers (Bergault et al., 2025) ⭐ NEW
- **arXiv**: 2509.06510
- **URL**: https://arxiv.org/abs/2509.06510
- **Authors**: Philippe Bergault, Sébastien Bieber, Leandro Sánchez-Betancourt
- **Date**: September 8, 2025 (v2 October 20, 2025)
- **Key contribution**: Characterizes optimal LP exit as stochastic control problem with endogenous stopping time
- **Core insights**:
  - LP's value function satisfies HJB quasi-variational inequality (unique viscosity solution)
  - Optimal exit depends on oracle price vol, fee levels, and trader behavior mix
  - Arbitrage generates both fees AND IL — LP optimally balances these opposing effects
  - Derives optimal fee level for representative LP playing optimal exit strategy
  - Two numerical approaches: Euler scheme with operator splitting + Longstaff-Schwartz regression
- **Implication**: LPs should actively manage exit timing, not just set-and-forget
- **Relevance**: Actionable framework for LP position management; complements LVR theory with exit optimization

### Improving DeFi Accessibility through Efficient Liquidity Provisioning with Deep Reinforcement Learning (Brini et al., 2025) ⭐ NEW
- **arXiv**: 2501.07508
- **URL**: https://arxiv.org/abs/2501.07508
- **Authors**: Alessio Brini et al.
- **Date**: January 13, 2025
- **Venue**: AAAI 2025 Workshop (AI for Social Impact)
- **Key contribution**: DRL agent for dynamic LP position management in Uniswap v3
- **Core insights**:
  - Models LP as MDP; trains agent with PPO algorithm
  - Agent dynamically adjusts positions using price dynamics
  - Balances fee maximization vs IL mitigation
  - Rolling window approach captures regime shifts
  - Outperforms passive retail LP strategies
- **Implication**: Data-driven LP management can improve accessibility for small participants
- **Relevance**: Practical implementation path for automated LP optimization

### Liquidity Provision with τ-Reset Strategies (Berezovskiy, 2025) ⭐ NEW
- **arXiv**: 2505.15338
- **URL**: https://arxiv.org/abs/2505.15338
- **Author**: Rostislav Berezovskiy
- **Date**: May 21, 2025
- **Key contribution**: ML-based methodology for optimal LP in CLMMs within τ-reset strategy family
- **Core insights**:
  - Novel method to approximate historical liquidity without requiring liquidity data
  - Uses parametric model + ML to find optimal strategies
  - Custom backtesting framework for CLMMs developed
  - Validated across multiple Uniswap v3 trading pairs
  - τ-reset: Periodic strategy that resets position parameters every τ interval
- **Implication**: Practical, backtested approach to concentrated liquidity optimization
- **Relevance**: Ready-to-implement LP strategy framework with empirical validation

### Strategic Analysis of Just-In-Time Liquidity Provision in CLMMs (Menasché et al., AFT 2025) ⭐ NEW
- **arXiv**: 2509.16157
- **URL**: https://arxiv.org/abs/2509.16157
- **Venue**: AFT 2025 (Pittsburgh)
- **Date**: September 19, 2025
- **Key contribution**: First formal, transaction-level model of JIT liquidity provision in CLMMs (Uniswap v3-style)
- **Core insights**:
  - JIT LPs momentarily supply concentrated liquidity for single swaps to extract disproportionate fees
  - Optimal JIT strategy exists (proven); formulated as non-linear optimization
  - **Current JIT LPs are suboptimal**: Could increase earnings by up to 69% by properly accounting for price impact
  - JIT improves market efficiency (lower slippage for traders)
  - **BUT erodes passive LP profits by up to 44% per trade**
- **Relevance to LVR**: JIT is a form of "informed LP" that front-runs passive LPs — similar to how arbitrageurs front-run on price discovery. JIT exacerbates passive LP losses beyond LVR from arbs.
- **Connection**: Defensive strategies against JIT should complement LVR mitigation
- **Implication**: Passive LPs face dual threat from both arbitrageurs (LVR) AND sophisticated LPs (JIT)

---

## New Additions (2026-02-08)

### A Derivative Pricing Perspective on Liquidity Tokens in CPMMs (Bichuch & Feinstein, 2026) ⭐ NEW
- **arXiv**: 2409.11339
- **URL**: https://arxiv.org/abs/2409.11339
- **Authors**: Maxim Bichuch, Zachary Feinstein
- **Revised**: January 23, 2026 (v4)
- **Key contribution**: Treats LP tokens as derivative positions; derives Black-Scholes-like pricing/hedging formulas
- **Core insights**:
  - LP token should be valued as derivative of underlying assets
  - Under risk-neutral pricing, hedged position grows at risk-free rate
  - Prevailing on-chain LP token price doesn't reflect this (mispriced!)
  - Method to calibrate "implied volatility" from LP token behavior
  - Novel AMM design considerations from derivative-pricing perspective
- **Relevance**: Provides rigorous valuation framework for LP positions; could inform sophisticated hedging strategies
- **Connection**: Complements LVR theory by giving LP a proper derivative pricing lens

### Modeling Loss-Versus-Rebalancing via Continuous-Installment Options (Singh et al., 2025) ⭐ NEW
- **arXiv**: 2508.02971
- **URL**: https://arxiv.org/abs/2508.02971
- **Author**: Srisht Fateh Singh et al.
- **Date**: August 5, 2025
- **Key contribution**: Models CFAMM position as portfolio of exotic options (perpetual American continuous-installment options)
- **Core insights**:
  - **LVR = Theta of embedded CI option** (formally proven!)
  - AMM's adverse selection cost is identical to time decay of at-the-money CI option
  - Derives liquidity profiles that achieve approximately constant LVR over arbitrary time windows
  - Provides practical framework for estimating future adverse-selection costs
  - Method to calibrate constant volatility from implied vol term structure
- **Implication**: LP can now choose position parameters to target specific, predictable LVR
- **Relevance**: Major theoretical advancement — connects LVR rigorously to options theory; actionable for position optimization

---

## New Additions (2026-02-07)

### Defensive Rebalancing for Automated Market Makers (Herlihy, 2026) ⭐ NEW
- **arXiv**: 2601.19950
- **URL**: https://arxiv.org/abs/2601.19950
- **Author**: Maurice Herlihy (Brown University)
- **Date**: January 26, 2026
- **Key contribution**: Introduces "defensive rebalancing" — direct asset transfers between CFMMs to reach arbitrage-free state
- **Core insights**:
  - Any arbitrage-prone configuration has a rebalancing that strictly improves some CFMMs without hurting others
  - **Pareto efficiency ⟺ arbitrage-free** under rebalancing
  - For log-concave trading functions (including CPMM), optimal rebalancing is a **convex optimization** with unique solution
  - "Mixed rebalancing" can harvest arbitrage from non-participants and CEXs
- **Implication**: CFMMs could coordinate to proactively defend LPs rather than passively losing to arbitrageurs
- **Relevance**: Novel theoretical framework — could inspire new protocol designs where pools cooperate
- **Connection**: Relates to Angstrom's same-price-per-block concept but at protocol level

### How to Serve Your Sandwich? MEV Attacks in Private L2 Mempools (Gogol et al., 2026) ⭐ NEW
- **arXiv**: 2601.19570
- **URL**: https://arxiv.org/abs/2601.19570
- **Date**: January 27, 2026
- **Key contribution**: Formal analysis of sandwich attack feasibility on L2 rollups
- **Core insights**:
  - Private mempools make sandwiching **probabilistic, not deterministic**
  - Empirical analysis: most flagged sandwich patterns are **false positives**
  - **Median net return for L2 sandwiches is negative**
  - Sandwiching is rare and largely unprofitable on rollups
- **Implication**: L2s may naturally resist MEV/LVR extraction; design insight for sequencing policies
- **Relevance**: Suggests L2 deployment may inherently reduce LP adverse selection costs

### A Formal Approach to AMM Fee Mechanisms with Lean 4 (Bartoletti et al., 2026)
- **arXiv**: 2602.00101
- **URL**: https://arxiv.org/abs/2602.00101
- **Authors**: Massimo Bartoletti et al.
- **Key contribution**: Machine-checked formal verification of AMM fee mechanisms using Lean 4 proof assistant
- **Core insights**:
  - Trading fees break additivity: single large swap yields strictly more than split trades when φ < 1
  - Output-boundedness and monotonicity preserved under fees
  - Derives closed-form solution to arbitrage problem with fees (unique)
- **Relevance**: Provides rigorous mathematical foundation for fee mechanism analysis; could inform smart contract verification

### The Impact of Volatility Buffering in the Transition to Impermanent Loss Risk (Computational Economics, 2026)
- **URL**: https://link.springer.com/article/10.1007/s10614-025-11297-1
- **Venue**: Computational Economics (Springer)
- **Key contribution**: Empirical study of how different volatility sources affect IL in Uniswap V2
- **Core insights**:
  - **Volatility buffering effect**: V-S (volatile-stable) pools mitigate external volatility → IL transmission vs V-V pools
  - IL has autoregressive structure — cumulative exposure matters for hedging
  - Traditional market volatility (VIX, OVX) also affects crypto IL
- **Methodology**: Quantile regression, ARX models, PCA, dominance decomposition
- **Relevance**: Practical guidance for LP strategy — V-S pools offer natural hedge; informs pool selection

---

## Industry & Practitioner Sources

### Toxic Flow: The Hidden Cost of Providing Liquidity (Sandmark, Feb 2026) ⭐ NEW
- **URL**: https://www.sandmark.com/news/features/toxic-flow-hidden-cost-providing-liquidity
- **Date**: February 3, 2026
- **Key contribution**: High-quality industry explainer of LVR/toxic flow concepts
- **Notable data points**:
  - References Wu et al. 2025 showing **Wintermute + SCP + Kayle = ~90% of arbitrage value** in Q1 2025
  - Su Zhu's casino analogy: market makers are casinos, arbitrageurs are card counters
  - DMMs provide liquidity on single-stock stress but consume liquidity during multi-stock stress
- **Solutions surveyed**: Dynamic asymmetric fees, external price references, batch auctions, intent-based architectures
- **Relevance**: Excellent accessible overview; confirms concentration of MEV extraction

### Explainable Patterns in Cryptocurrency Microstructure (Bieganowski et al., 2026)
- **arXiv**: 2602.00776
- **URL**: https://arxiv.org/abs/2602.00776
- **Date**: January 31, 2026
- **Key contribution**: Universal microstructure features across crypto assets; flash crash analysis
- **Core insights**:
  - SHAP feature importance is stable across BTC, LTC, ETC, ENJ, ROSE
  - Flash crash analysis validates adverse selection theory empirically
  - Taker vs maker strategy divergence during stress confirms MM vulnerability
- **Relevance**: Tangential — validates theoretical underpinnings of LVR; useful for empirical work

### ASRI: Aggregated Systemic Risk Index for Cryptocurrency Markets (Farzulla, 2026)
- **arXiv**: 2602.03874
- **URL**: https://arxiv.org/abs/2602.03874
- **Date**: February 1, 2026
- **Key contribution**: Composite risk index for DeFi ecosystem monitoring
- **Core insights**:
  - Four weighted sub-indices: Stablecoin (30%), DeFi Liquidity (25%), Contagion (25%), Regulatory (20%)
  - Validated against Terra/Luna, Celsius/3AC, FTX, SVB crises (all detected, t-stats 5.47-32.64)
  - HMM identifies Low/Moderate/Elevated risk regimes with >94% persistence
  - Captures DeFi-specific vulnerabilities: composability risk, flash loans, RWA linkages
- **Relevance**: Tangential — systemic risk monitoring; could inform LP risk management strategies
- **Live dashboard**: https://asri.dissensus.ai

### TxRay: Agentic Postmortem of Live Blockchain Attacks (Wang et al., 2026)
- **arXiv**: 2602.01317
- **URL**: https://arxiv.org/abs/2602.01317
- **Date**: February 1, 2026
- **Key contribution**: LLM-based system for automated DeFi exploit analysis
- **Core insights**:
  - Introduces "Anyone-Can-Take" (ACT) opportunity taxonomy
  - 92.11% end-to-end reproduction rate on 114 DeFiHackLabs incidents
  - 40min median latency for root cause, 59min for executable PoC
- **Relevance**: Tangential — attack detection/response; not directly about LVR but useful for security

### DeXposure-FM: Time-series Graph Foundation Model for DeFi Credit Exposure (He et al., 2026) ⭐ NEW
- **arXiv**: 2602.03981
- **URL**: https://arxiv.org/abs/2602.03981
- **Date**: February 3, 2026
- **Key contribution**: First foundation model for DeFi inter-protocol credit exposure forecasting
- **Core insights**:
  - Graph-tabular encoder trained on 43.7M data entries across 4,300+ protocols
  - Enables protocol-level systemic importance scoring
  - Sector-level spillover and concentration metrics
  - Outperforms SOTA graph neural networks on forecasting benchmarks
- **Model**: https://huggingface.co/EVIEHub/DeXposure-FM
- **Code**: https://github.com/EVIEHub/DeXposure-FM
- **Relevance**: Tangential — systemic risk monitoring; could inform LP risk management for cross-protocol exposure

---

## New Additions (2026-02-08, Update #2)

### Automated Liquidity: Market Impact, Cycles, and De-pegging Risk (Meister, 2026) ⭐ NEW
- **arXiv**: 2601.11375
- **URL**: https://arxiv.org/abs/2601.11375
- **Author**: Bernhard Meister
- **Date**: January 16, 2026
- **Key contribution**: Novel thermodynamic perspective on CPMMs
- **Core insights**:
  - **CPMM as Carnot engine**: Multi-phase cycle where one phase = liquidity taker swap, another = LP deposit/withdrawal
  - **Market impact for optimal-growth LPs**: Derives square-root impact for random walk, extends to fractional O-U processes
  - **Breaks with linearized liquidity models** used in most DEXs
  - **Stablecoin de-pegging as catastrophe risk**: Links default odds to catastrophe bond pricing
- **Relevance**: Provides thermodynamic lens on AMM efficiency; suggests linearized models underestimate impact
- **Connection to LVR**: The "entropy leak" concept maps to LVR — LPs are under-compensated for variance drag

---

## Industry Developments

### Whetstone Research / Doppler Protocol (February 2026) ⭐ NEW
- **URL**: https://whetstone.cc / https://doppler.lol
- **Funding**: $9M Seed led by Pantera Capital (Variant, Figment, Coinbase Ventures)
- **Founder**: Austin Adams (former Uniswap Labs, author of am-AMM paper)
- **Key contribution**: Price discovery and liquidity bootstrapping protocol on Uniswap ecosystem
- **Core features**:
  - **Price discovery auctions** designed to limit sniper impact
  - **Protocol-owned liquidity** from day 1
  - Compresses token deployment, vesting, liquidity bootstrapping into single interface
  - Integrated with aggregators, routers, explorers
- **Stats**: 40,000+ assets created daily, $1.5B+ value, $1B+ cumulative volume
- **Business model**: Trading fees on all assets created, regardless of trading venue
- **Relevance**: Austin Adams bringing am-AMM theoretical work to production; validates batch auction concepts
- **Connection to LVR**: Fair launch mechanism reduces initial MEV extraction; could extend to continuous trading

### Sorella Labs Funding Update (February 2026)
- **Source**: SEC Filing (Feb 2, 2026)
- **New funding**: $5.2M (10 investors; $5.5M total offering)
- **Total raised**: $12.4M
- **Implication**: Continued investment in Angstrom development; expanding team
- **Relevance**: Confirms industry confidence in hook-based MEV protection approach

### Bitwise Files S-1 for Uniswap ETF (February 2026)
- **Source**: SEC S-1 Filing (Feb 6, 2026)
- **URL**: https://www.hokanews.com/2026/02/defi-goes-wall-street-bitwise-files-for.html
- **Key development**: First direct attempt to package DEX exposure in traditional ETF format
- **Implications**:
  - Signals institutional appetite for DeFi protocol exposure
  - If approved, validates Uniswap as institutional-grade asset
  - Regulatory scrutiny will focus on governance, decentralization, smart contract risks
  - Could accelerate similar filings for other DeFi protocols
- **Relevance**: While not directly about LVR, institutional adoption of Uniswap increases importance of LP protection mechanisms — funds allocating to UNI ETF will care about LP profitability

### 1inch Aqua — Shared Liquidity Layer (February 2026) ⭐ NEW
- **URL**: https://blog.1inch.com/lp-efficiency-loss-and-what-aqua-changes/
- **Date**: February 3, 2026
- **Key contribution**: Protocol addressing LP capital utilization (complementary to LVR mitigation)
- **Core insights**:
  - 1inch research: 83-95% of liquidity in major pools sits idle (~$12B underutilized)
  - Introduces "TVU" (Total Value Unlocked) metric as alternative to TVL
  - Shared liquidity allows same assets to be deployed across strategies atomically
  - LPs connect wallet once; Aqua reallocates to wherever demand exists
- **Mechanism**: Atomic execution + automatic reallocation across venues
- **Distinction from LVR**: Addresses utilization/fragmentation, not adverse selection
- **Relevance**: Complementary solution — if LP capital is utilized more, fee income can better offset LVR
- **Connection**: Could combine with LVR-mitigating venues (CoW AMM, Angstrom) for full LP protection

### CoW DAO Transfers MEV Blocker to Consensys SMG (February 2026) ⭐ NEW
- **Source**: https://cow.fi/learn/special-mechanisms-group-acquires-mev-blocker-rpc-to-advance-state-of-the-art-backrunning-auction-infrastructure
- **Date**: February 2026
- **Key development**: CoW DAO hands off MEV Blocker RPC to Consensys' Special Mechanisms Group (SMG)
- **MEV Blocker stats**: 4.5M+ users benefited, 6,177 ETH returned to users
- **Implications**:
  - CoW DAO refocusing on CoW Swap and CoW Protocol's core MEV capabilities
  - SMG to enhance user-centric backrunning auction infrastructure
  - Signals maturation of MEV protection as standalone product category
  - Institutional backing (Consensys) for MEV protection tooling
- **Relevance**: MEV protection infrastructure now spans multiple organizations; ecosystem diversification

### UNIfication Governance Passed (January 2026) ⭐ NEW
- **Source**: https://coinmetrics.substack.com/p/state-of-the-network-issue-346
- **URL**: OpenZeppelin audit: https://www.openzeppelin.com/news/uniswap-labs-phoenix-fees-audit
- **Key development**: Uniswap "fee switch" now active
- **Mechanism**:
  - Protocol fees from v2/v3 on Ethereum mainnet activated
  - Fees route to UNI burn mechanism
  - Central controller governs fee policies per version
- **Relevance**: Fee revenue now directly tied to protocol health; increases stakes for LP profitability research

### Uniswap CCA on Base (February 2026)
- **Source**: https://www.ainvest.com/news/uniswap-cca-base-game-changer-chain-token-launches-2601/
- **What it is**: Continuous Clearing Auctions for token launches
- **Mechanism**:
  - Block-by-block price discovery
  - Bidders submit max price limits
  - Each block clears at market-clearing price
  - Automatic Uniswap v4 pool seeding post-auction
- **Case study**: Aztec Network raised $59-61M, $557M FDV, 16,700+ participants
- **Relevance to LVR**: Validates batch auction approach (like FM-AMM) for fair pricing
- **Key insight**: CCA is for launches, FM-AMM is for ongoing trading — different use cases, same theoretical foundation
