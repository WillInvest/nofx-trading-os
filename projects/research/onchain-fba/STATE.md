# Research State — On-Chain Trustless FBA

**Last Updated**: 2026-02-07 (Cron daily update, 3:00 PM)

## Current Focus
**ECOSYSTEM CONVERGENCE**: The pieces are coming together! EIP-8105 proposes native encrypted mempool for Ethereum, Uniswap CCA proves uniform clearing works in production, and Jump's DFBA adds flow separation.

**OUR NICHE**: Build the **Trustless Uniform Clearing Layer** that:
1. Integrates with EIP-8105's encrypted mempool
2. Extends Uniswap CCA's clearing to general DEX trading
3. Incorporates DFBA's maker/taker flow separation
4. Addresses a16z's concerns via defense-in-depth

## Research Questions

### Primary (UPDATED 2026-02-07 PM)
**How do we extend Uniswap CCA's uniform clearing to continuous DEX trading with BEAST-MEV/EIP-8105 encrypted orders?**

### Sub-questions
1. ✅ What are current solutions' trust assumptions? → All require trusting some third party
2. ✅ What does academic literature say? → SoK confirms no complete solution exists
3. ✅ What cryptographic primitives enable hiding order contents? → **BEAST-MEV solves this!**
4. ✅ How can batch boundaries be determined without trusted coordinator? → Block boundaries + threshold encryption
5. ✅ Is uniform clearing practical in production? → **Uniswap CCA proves yes!**
6. 🔄 What's the gas cost tradeoff for on-chain clearing price computation?
7. 🔄 Can ZK proofs make clearing verification practical?
8. 🔄 How to handle partial fills fairly in uniform-price auctions?
9. ❓ Can fraud-proof clearing compete with ZK approaches?
10. 🆕 How to integrate with EIP-8105's key provider registry?
11. 🆕 Can DFBA's flow separation reduce clearing complexity?
12. 🆕 How to extend CCA from token launches to continuous trading?

## Recent Progress
- [2026-02-04] Project initialized
- [2026-02-04] Initial literature search completed
  - Found 7 key academic papers
  - Analyzed Flashbots, CoW Protocol, Chainlink FSS
  - Critical finding: SoK paper (Heimbach 2022) confirms no existing scheme meets all requirements
  - Identified trust assumptions in all current solutions
- [2026-02-04] **Daily research update - SIGNIFICANT DISCOVERY**
  - Found Paradigm "Leaderless Auctions" paper (Feb 2024)
  - This is the strongest existing design for trustless auction bid privacy
  - 4-round protocol using threshold encryption + fault economics
  - Solves "last look" problem without trusted party
  - Key gap: doesn't address uniform price clearing or permissionless participation
- [2026-02-04] **Evening update - BREAKTHROUGH PAPERS**
  - Found **Silent Setup** (ePrint 2024/263): NO interactive threshold setup!
    - Joint pubkey computed deterministically → enables PERMISSIONLESS
  - Found **BTE** (ePrint 2024/669): O(n) batched decryption, not O(nB)
    - Makes mempool encryption practical for high-throughput chains
  - Found **Shutter Network**: Production implementation on Gnosis Chain
  - **New approach**: "Silent Batch Auction" = Silent Setup + BTE + Uniform Clearing
- [2026-02-07] **🔥 CRITICAL DISCOVERY: BEAST-MEV EXISTS**
  - Found **BEAST-MEV** (ePrint 2025/1419) — combines Silent Setup + BTE
  - Same authors as original papers (Choudhuri, Faust, Garg, Policharla)
  - Our "Silent Batch Auction" core concept is already implemented!
  - Security proven in Generic Group Model
- [2026-02-07] **Additional major papers found:**
  - **Weighted BTE** (2025/2115): 6× improvement, PoS stake-weighted support
  - **Silent Threshold Crypto** (2025/1547, Waters & Wu): Standard model security!
  - **USENIX Security '25**: BTE formal publication
  - **HAL paper**: Gas-optimized sealed-bid auctions
  - **Accountability papers**: SSS, self-incriminating proofs, traceable TE
- [2026-02-07] **PIVOTED research direction:**
  - BEAST-MEV handles Layer 1 (encrypted mempool)
  - Our contribution: Layer 2 (uniform price clearing on top of decrypted orders)
  - New ideas: ZK-verified clearing, fraud-proof clearing
- [2026-02-07 PM] **🚀 ECOSYSTEM VALIDATION — Major Production Discoveries**
  - **EIP-8105**: Native encrypted mempool proposed for Ethereum Hegotá fork!
    - Technology-agnostic key provider registry
    - Sub-slot decryption key inclusion
    - This is the Layer 0/1 we'll build on
  - **TrX** (ePrint 2025/2032): Production-ready encrypted mempool in BFT
    - Only 27ms overhead (14%)! Proves viability.
    - Authors include Policharla (BEAST-MEV)
  - **Uniswap CCA**: Continuous Clearing Auctions LIVE on Uniswap v4
    - Uniform clearing price per block ✅
    - ZK Passport for privacy (with Aztec) ✅
    - $59M Aztec token launch
    - **This is our Layer 2 concept in production!**
  - **Jump Crypto DFBA**: Dual Flow Batch Auction design
    - Maker/taker flow separation
    - Sub-100ms batch auctions
    - Addresses toxic flow problem
  - **a16z "Limits" paper**: Critical analysis we must address
    - Speculative MEV, strong trust assumptions, practical concerns
  - **Shutter+Primev**: First encrypted mempool in Ethereum PBS underway
- [2026-02-07 PM] **📣 EIP-8105 & FOCIL: AllCoreDevs Update**
  - EIP-8105 formally presented at Jan 29 ACD meeting as Hegotá headliner candidate!
  - **Jannik Luhn** (Shutter) presented: "it relies on trusted parties, which is bad for decentralisation"
  - **EIP-8141** (Frame Transactions) also proposed: post-quantum + account abstraction
    - Vitalik personally endorsed: "satisfies entire list of goals of account abstraction"
  - FOCIL + encrypted mempool positioned as **complementary** features for Hegotá
  - Uniswap CCA now live on **Base** (permissionless deployment, Jan 22)
  - Uniswap web app has **auction UI** (Feb 2, 2026)
  - **Consensys acquired MEV Blocker** from CoW Protocol (Jan 26, 2026)
- [2026-02-07 Eve] **📊 Daily Cron Research Update**
  - **Rainbow RNBW CCA auction completed** — first major post-launch auction
    - Clearing price: **$0.13** (started at $0.10, 30% discovery)
    - Timeline: Pre-bid Feb 2 → Auction Feb 3 → Clearing Feb 5
    - **Live production validation of uniform clearing mechanism**
  - **Chainlink acquires Atlas** (Jan 22, 2026)
    - FastLane Labs transaction-ordering protocol
    - Integrates with SVR for OEV capture
    - Live on 5 chains (Arbitrum, Base, BNB, Ethereum, HyperEVM)
    - **Chainlink positioning as MEV infrastructure layer**
  - **Consensys/SMG acquires MEV Blocker** (confirmed Jan 26)
    - Stats: 4.5M+ users, 6,177 ETH rebates
    - CoW DAO focusing on core protocol
    - **Consolidation in MEV protection space**
  - **New ePrint papers found:**
    - 2026/021: Post-quantum threshold KEM (18× smaller ciphertexts)
    - 2026/031: ThFHE security (finds attacks in prior work!)
    - 2026/190: Three-round robust threshold ECDSA
    - 2026/094: Hardware-friendly threshold ECDSA
  - **Glamsterdam update**: bals-devnet-2 launched Feb 4, H1 2026 target
  - **Hegotá update**: Headliner deadline passed Feb 4; EIP-8105, FOCIL, Frame Tx leading
  - **Shade Network**: New competitor with encrypted mempool testnet (Jan 19)
- [2026-02-07 3PM] **📊 Saturday Cron Research Update**
  - **Critical academic finding**: arXiv 2601.14996 (Albrecht & Karame)
    - Mempool auditing has **25%+ false positive rate** for censorship detection
    - **30-second threshold** for reliable transaction ordering
    - Batch-fair ordering can only guarantee fairness for limited transaction subset
    - **Validates our thesis**: Ordering fairness is fundamentally limited → uniform clearing essential
  - **Glamsterdam details confirmed**:
    - EIP-7732 (ePBS) + EIP-7928 (Block-Level Access Lists)
    - Gas limit: 60M → 200M (3× increase for parallel execution)
    - Timeline: May/June 2026 mainnet, scope freeze end of Feb
  - **Hegota competition intensifying**:
    - FOCIL gaining consensus as #1 headliner (censorship resistance)
    - EIP-8105 (encrypted mempool) positioned as #2 complementary feature
    - EIP-8141 (Frame Tx) has Vitalik endorsement for post-quantum
  - **VibeSwap proposal**: MEV-resistant batch DEX on Nervos (non-EVM validation)
  - **INDEX.md updated**: Now 60+ sources catalogued

## Key Findings from Literature

### All Current Solutions Fail Trustlessness
1. **Flashbots**: Builders/relays see transactions → can front-run
2. **CoW Protocol**: Solvers are trusted third parties
3. **Chainlink FSS**: Oracle network is trusted (better, but still trust)
4. **L2 Sequencers**: Same problem as miners, just different party

### Promising Cryptographic Directions
1. **Commit-Reveal**: Simple, no new assumptions, but has griefing risk
2. **Threshold Encryption**: Needs m-of-n key holders → who holds keys?
3. **Time-Lock Puzzles/VDFs**: No trusted party, but computational cost
4. **On-Chain Uniform Clearing**: Make order irrelevant via same price

### Critical Gap in Literature
The Heimbach 2022 SoK paper concludes: "Currently no scheme fully meets all the demands of the blockchain ecosystem. All approaches demonstrate unsatisfactory performance in at least one area."

This confirms our research addresses an **unsolved problem**.

## Next Actions

### Immediate (This Week)
- [x] ~~Download and deep-read SoK paper (arXiv:2203.11520)~~ (summary in INDEX.md)
- [x] ~~Find if Silent Setup + BTE combination exists~~ → BEAST-MEV!
- [x] ~~Search for production implementations~~ → Found Uniswap CCA!
- [x] ~~Track EIP-8105 progress~~ → Formal Hegotá headliner presentation Jan 29!
- [ ] Deep-read BEAST-MEV paper and implementation code
- [ ] Study Weighted BTE for PoS chain compatibility
- [ ] Review HAL gas-optimization paper for clearing algorithms
- [ ] Clone Uniswap CCA repo (now on Base!), study clearing price computation
- [ ] Review Jump DFBA for maker/taker separation mechanics
- [ ] **NEW**: Read EIP-8141 Frame Transaction spec (Vitalik-endorsed)
- [ ] **NEW**: Explore Brevis ProverNet for decentralized ZK proving

### Short-term (This Month)
- [ ] Design uniform clearing algorithm optimized for EVM
- [ ] Prototype ZK circuit for clearing price verification
- [ ] Estimate gas costs: direct vs ZK vs fraud-proof approaches
- [ ] Compare with CoW Protocol's Uniform Directed Prices (UDP) implementation
- [ ] Study Penumbra's in-protocol arbitrage mechanism
- [ ] **NEW**: Address a16z "Limits" concerns in our design doc
- [ ] **NEW**: Spec how our clearing layer integrates with EIP-8105
- [ ] **NEW**: Design DFBA-style flow separation for our clearing layer

### Medium-term
- [ ] Draft THEORY.md: "BEAST-MEV + Uniform Clearing" formal spec
- [ ] Implement clearing layer prototype on testnet
- [ ] Benchmark end-to-end latency and gas
- [ ] Write paper draft or spec document
- [ ] **NEW**: Contribute to EIP-8105 discussion (execution layer perspective)

## Blockers
- ~~Brave API rate limited~~ → User upgraded to Pro! 🎉
- None currently

## Key Insights

### Insight 1: The Trust Spectrum
Not binary trustless/trusted. There's a spectrum:
- Full trust in single party (worst)
- Distributed trust among competing parties (CoW)
- Threshold trust (FSS)
- Economic/cryptographic trust (commit-reveal with penalties)
- Fully trustless (goal)

### Insight 2: The Timing Problem
All batch auctions need to answer: "When does the batch close?"
- Block boundaries? (natural but coarse)
- Fixed intervals? (who enforces?)
- Smart contract state? (can be manipulated?)

### Insight 3: Griefing is the Achilles' Heel
Commit-reveal is simple but:
- If you don't reveal, batch can't execute
- Penalizing non-reveal requires deposits
- Deposits create capital inefficiency
- May need "forced reveal" via time-lock encryption

### Insight 4: Paradigm's Fault Economics
Paradigm's Leaderless Auctions solves the griefing problem elegantly:
- **Absence fault**: If your bid is missing from f+1 bid sets, you pay penalty
- **Penalty > option value**: Makes cancellation economically unviable
- **Threshold encryption**: Forces reveal without explicit reveal phase
- This is "forced reveal via cryptography + economics" — exactly what we speculated!

### Insight 5: Separation of Concerns
The problem splits into two parts:
1. **Bid Privacy**: How to hide bids until batch boundary (Paradigm solves this)
2. **Execution Fairness**: How to ensure fair price/order once revealed (still open!)
Our contribution: Layer uniform price clearing on top of Leaderless Auctions

### Insight 6: BEAST-MEV = Silent Batch Auction (NEW 2026-02-07)
Our conceptual synthesis has been implemented by the original paper authors!
- Silent Setup (Garg et al.) + BTE (Choudhuri et al.) = BEAST-MEV
- Same research group independently reached same conclusion
- Validates our research direction but shifts our contribution point

### Insight 7: The Execution Layer Gap (NEW 2026-02-07)
BEAST-MEV solves privacy → Our opportunity is fairness:
- BEAST-MEV decrypts transactions but doesn't specify execution order
- After decryption, transactions are visible — back-running still possible
- Uniform price clearing makes order irrelevant → eliminates back-running too
- **Architecture**: BEAST-MEV = Layer 1 (privacy), Our work = Layer 2 (fair execution)

### Insight 8: Accountability as Defense-in-Depth (NEW 2026-02-07)
New cryptographic primitives provide collusion deterrence:
- **Secret Sharing with Snitching**: Reconstruction creates proof of participation
- **Self-Incriminating Proofs**: At least one colluder exposed
- **Traceable TE with Public Tracing**: Smart contract enforcement
- Can combine with BEAST-MEV for stronger guarantees

### Insight 9: Weighted BTE for PoS Integration (NEW 2026-02-07)
Weighted BTE paper extends BEAST-MEV for proof-of-stake:
- Communication cost independent of total stake weight
- 50× improvement over naive virtualization
- Critical for Ethereum, Solana integration
- Makes "validators as Keypers" practical

### Insight 10: The Ecosystem Is Converging (NEW 2026-02-07 PM)
Multiple teams independently building toward same vision:
- **Shutter** → EIP-8105 for native encrypted mempool
- **Uniswap** → CCA for uniform clearing auctions
- **Jump** → DFBA for flow separation
- **Aptos** → TrX for production encrypted BFT
- **Thesis validated**: The pieces exist, need synthesis

### Insight 11: Encryption Alone Is Not Enough (a16z insight)
Critical reality check from a16z's "Limits" paper:
- Speculative MEV: Attackers can guess and try
- Threshold trust is STRONGER than consensus trust (undetectable violation)
- Solution: Defense in depth — encryption + uniform clearing + accountability
- Encryption makes MEV harder; clearing makes it pointless

### Insight 12: Production Validation (NEW 2026-02-07 PM)
Uniswap CCA proves key elements work:
- Single clearing price per block IS practical
- ZK privacy for participants IS achievable
- Automatic liquidity seeding IS valuable
- BUT: CCA is for token launches, not general DEX trading
- **Our gap**: Extend to continuous trading with encrypted orders

### Insight 13: Flow Separation Reduces Complexity (DFBA insight)
Jump's DFBA suggests maker/taker separation:
- Makers don't compete with each other on latency
- Takers don't suffer from toxic maker flow
- Two simpler auctions > one complex auction
- **Application**: Could split BEAST-MEV batches into maker/taker sub-batches

### Insight 14: Ethereum is Ready for This (ACD Update)
Jan 29, 2026 AllCoreDevs meeting validated our direction:
- EIP-8105 presented as Hegotá headliner (encryption layer)
- FOCIL presented as complement (censorship resistance)
- EIP-8141 endorsed by Vitalik (post-quantum readiness)
- **Implication**: L1 will have native encrypted mempool; Layer 2 execution is the gap
- **Timeline pressure**: Hegotá planning happening NOW — opportunity to contribute

### Insight 15: Production Deployments Enable Empirical Study
CCA on Base (Jan 22) and web app (Feb 2) mean:
- Can study live clearing price algorithms
- Can observe gas costs in production
- Can analyze user behavior patterns
- **Action**: Deploy monitoring to track CCA auctions

### Insight 16: RNBW Auction Validates Price Discovery (NEW 2026-02-07 Eve)
Rainbow token CCA auction provides empirical data:
- Start price: $0.10 → Clearing price: $0.13 (30% price discovery)
- 3-day auction window (pre-bid → auction → clearing)
- All participants received same final price
- **Validation**: Uniform clearing works for real token launches
- **Limitation**: Token launch ≠ continuous DEX trading (different dynamics)

### Insight 17: MEV Infrastructure Consolidation (NEW 2026-02-07 Eve)
Two major acquisitions in January 2026:
1. Chainlink → Atlas (transaction ordering, OEV)
2. Consensys/SMG → MEV Blocker (backrunning auctions)
- **Implication**: Infrastructure layer consolidating around established players
- **Opportunity**: Our clearing layer could integrate with multiple providers
- **Risk**: Competition from well-funded incumbents

### Insight 18: Post-Quantum Considerations Emerging (NEW 2026-02-07 Eve)
New research signals post-quantum threshold crypto maturity:
- ePrint 2026/021: Lattice threshold KEM (18× smaller ciphertexts, 30 KiB)
- EIP-8141: Post-quantum account abstraction (Vitalik endorsed)
- **Design consideration**: Our clearing layer should be signature-agnostic
- **Timeline**: Not urgent (years away) but good to architect for

### Insight 19: Ordering Fairness Is Fundamentally Limited (NEW 2026-02-07 3PM)
Academic proof that mempool-based ordering cannot guarantee fairness:
- arXiv 2601.14996 (Albrecht & Karame): First rigorous analysis
- **30-second threshold**: Transactions must be 30+ seconds apart for reliable ordering
- **25%+ false positives**: Honest miners can be mislabeled as malicious
- **Direct quote**: "batch-fair ordering schemes can offer only strong fairness guarantees for a limited subset of transactions"
- **Critical implication**: Validates our thesis — uniform clearing > ordering fairness
- **Why this matters**: Even with perfect mempool visibility, ordering is probabilistic not deterministic
- **Our advantage**: Uniform price clearing makes ordering irrelevant

### Insight 20: Parallel Execution Changes MEV Dynamics (NEW 2026-02-07 3PM)
Glamsterdam's EIP-7928 (Block-Level Access Lists) enables:
- Parallel transaction execution (non-conflicting txs processed simultaneously)
- Pre-declared account access (proposers know what state will be touched)
- 3× gas limit increase (60M → 200M)
- **MEV implication**: Some ordering games become harder with parallelization
- **Open question**: Does parallel execution help or hurt uniform clearing?

## Literature Search Queries for Next Update
- "Uniswap CCA clearing price algorithm" — study Solidity implementation
- "EIP-8141 frame transaction" — track competing proposals
- "NIST MPTS 2026 threshold" — academic workshop on March 10-11
- "Brevis ProverNet ZK marketplace" — decentralized proof generation
- "Anoma intent architecture" — alternative MEV mitigation approach
- "Rainbow RNBW Base transaction" — empirical CCA data analysis
- "Chainlink Atlas SVR integration" — OEV capture mechanisms
- "Shade Network encrypted mempool" — new competitor analysis
- "ePrint 2026 batch threshold" — track new threshold crypto papers
- "Glamsterdam ePBS" — monitor H1 2026 upgrade progress
- "EIP-7928 Block-Level Access Lists parallel" — parallel execution MEV impact
- "batch-fair ordering 30 seconds" — follow-up on Albrecht-Karame result
- "Hegota headliner decision" — track which EIPs are selected

## Next Research Cycle (Feb 8-14)
### Priority 1: Empirical Analysis
- [ ] Fetch RNBW auction transactions from Base explorer
- [ ] Reverse-engineer CCA clearing price computation
- [ ] Document gas costs for production clearing
- [x] Study mempool auditing limitations (arXiv 2601.14996) ✅

### Priority 2: Technical Deep-Dives
- [ ] Study ePrint 2026/031 ThFHE attack implications
- [ ] Review ePrint 2026/021 for post-quantum threshold applicability
- [ ] Compare Chainlink Atlas vs CoW Protocol vs Flashbots architecture
- [ ] Analyze EIP-7928 BALs impact on MEV (parallel execution)

### Priority 3: Design Work
- [ ] Draft multi-provider clearing interface spec
- [ ] Sketch ZK clearing circuit requirements
- [ ] Outline formal security model for clearing layer
- [ ] Address 30-second ordering limitation in our spec (from arXiv 2601.14996)
