# Research State — On-Chain Trustless FBA

**Last Updated**: 2026-02-08 (Cron research update, 1:03 AM)

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
- [2026-02-07 4PM] **📊 Saturday Evening Cron Research Update**
  - **New cryptographic direction discovered**: ePrint 2026/175 (Witness Encryption)
    - Practical WE for SNARK verification — alternative to threshold encryption
    - Authors: Soukhanov, Rebenko, El Gebali, Komarov ([[alloc] init])
    - Potential: "Encrypt order until batch proof exists" — no committee!
  - **ePrint 2026/186**: Bitcoin PIPEs v2 — WE for covenants (validates WE maturity)
  - **NIST MPTS 2026**: Workshop already completed (Jan 26-29) — need to find recordings
  - **a16z "17 Things for 2026"** (Feb 6):
    - SNARKs going mainstream (1M× overhead dropping)
    - KYA (Know Your Agent) as critical primitive for agent economy
    - Stablecoins hit $46T volume (20× PayPal)
  - **Glamsterdam deep-dive** (CryptoAPIs):
    - Scope freeze end of February
    - Mainnet target: May/June 2026
    - ePBS + parallel execution via BALs
  - **Updated architecture**: Added Layer 4 (Agent Economy) to vision
  - **INDEX.md & IDEAS.md updated**: Now 65+ sources catalogued
- [2026-02-07 5PM] **📊 Saturday 5PM Cron Research Update**
  - **🚀 Arcium Mainnet Alpha** (Feb 2, 2026) — MPC-based encrypted computation on Solana!
    - First production encrypted execution layer
    - Umbra Private: anonymous transfers + swaps
    - 3,000+ nodes on testnet, permissioned mainnet
    - Alternative to threshold: MPC computes on encrypted data
  - **🔬 Fhenix DBFV** (Feb 6, 2026) — FHE breakthrough for blockchain!
    - Decomposable BFV solves noise scaling problem
    - Enables sustained encrypted workloads
    - Could eventually enable compute-on-encrypted clearing
  - **📦 Uniswap CCA v1.1.0** — Production code available!
    - MIT licensed, fully open source
    - Audited by OpenZeppelin (Jan 23) & Spearbit (Jan 22)
    - Bug bounty active via Cantina
    - Factory: 0xCCccCcCAE7503Cac057829BF2811De42E16e0bD5
  - **New ePrint papers:**
    - 2026/170: gcVM — MPC via garbled circuits (~500 cTPS)
  - **Academic validation:** arXiv 2302.01177 — formal FBA welfare analysis
  - **New insight**: Encryption tech diversifying (threshold, MPC, FHE, GC, WE, TEE)
  - **Design principle**: Build encryption-agnostic clearing layer
  - **INDEX.md & IDEAS.md updated**: Now 75+ sources catalogued
- [2026-02-07 7PM] **📊 Saturday 7PM Cron Research Update**
  - **🔬 New Accountability Primitives Discovered**:
    - **ePrint 2026/181**: Collaborative Traceable Secret Sharing (CTSS)
      - PUBLIC tracing without designated tracer!
      - Eliminates private trace/verification keys
      - Based on Shamir/Blakley schemes
      - Polynomial-time tracing, minimal overhead
    - **ePrint 2026/182**: Accountable UC Async Secure Distributed Computing
      - Universal compiler τ_{zk-scr} for accountability
      - Chainlink Labs co-author (potential collaboration!)
      - Externally verifiable proofs of misbehavior
      - Uses AUC framework (S&P 2023)
  - **🌊 Flow Network**: 40M users, claims native MEV resistance + VRF + scheduled transactions
  - **📢 Vitalik L2 Critique**: "copypasta L2 chains" comment continues to reverberate
    - Base/Polygon responding: "L2s can't just be cheaper"
    - Reinforces our L1-first strategy
  - **⏰ Glamsterdam Scope Freeze**: End of February (~3 weeks to influence)
  - **MPC Benchmarking**: ePrint 2026/183 evaluates HPMPC, MPyC, MP-SPDZ, MOTION
  - **INDEX.md updated**: Now 85+ sources catalogued
- [2026-02-08 9PM] **📊 Saturday Night Cron Research Update**
  - **📚 Foundational paper added**: Budish-Cramton-Shim "Frequent Batch Auctions" (QJE 2015)
    - Seminal academic paper for uniform-price batch auctions
    - 1000+ citations — theoretical foundation for all blockchain batch auction research
    - Key insight: Convert "speed competition → price competition"
    - Directly underlies Uniswap CCA and our work
  - **🔬 ePrint 2026 scan completed**: 
    - ePrint 2026/190 (Three-round threshold ECDSA) — O(1) communication, improves on NDSS24
    - ePrint 2026/186 (Bitcoin PIPEs v2) — WE for covenants now production-ready concept
    - ePrint 2026/175 (Witness Encryption) — SNARK-verifiable WE practical
    - ePrint 2026/192 (Verification Theater) — security warning on formal verification claims
  - **📦 Uniswap CCA deep-dive**:
    - v1.1.0 canonical address: 0xCCccCcCAE7503Cac057829BF2811De42E16e0bD5
    - MIT licensed, audited by OpenZeppelin + Spearbit + ABDK
    - Technical docs and whitepaper available for study
    - Factory pattern enables permissionless auction deployment
  - **🔍 Hegota headliner competition**: Frame Tx (EIP-8141) vs EIP-8105 narratives in tension
    - Both competing for "protocol-level MEV protection" positioning
    - FOCIL appears to be gaining consensus as #1
  - **📊 No major new developments today** — Sunday quiet period
  - **INDEX.md updated**: Now 100+ sources catalogued
- [2026-02-07 8PM] **📊 Saturday 8PM Cron Research Update**
  - **🤖 ERC-8004 DISCOVERY — Agent Economy Infrastructure LIVE!**
    - Deployed to Ethereum mainnet January 29, 2026
    - Developed by EF dAI Team + MetaMask + Google + Coinbase
    - Already adopted by Base, BNB Chain, Polygon
    - On-chain registries: Identity, Reputation, Discovery
    - Pairs with x402 protocol for agent-to-agent payments
    - **Critical for us**: Native infrastructure for agent-signed DEX orders!
  - **🏆 Hegota Competition Dynamics**:
    - FOCIL: Building consensus as #1 headliner candidate
    - EIP-8105: Championed by Jannik Luhn (Shutter)
    - EIP-8141: Vitalik personally endorsed for AA + post-quantum
  - **📅 Glamsterdam Scope Freeze Confirmed**: End of February 2026
  - **⚠️ Verification Theater Warning** (ePrint 2026/192):
    - 5 vulnerabilities in "formally verified" libcrux/hpke-rs
    - Reinforces multi-layer security approach
  - **New ePrint papers found**:
    - 2026/190: Three-round threshold ECDSA with O(1) communication
  - **INDEX.md updated**: Now 95+ sources catalogued
  - **IDEAS.md updated**: Added agent-compatible order format design
- [2026-02-08 12AM] **📊 Sunday Midnight Cron Research Update**
  - **🚀 ERC-8004 Adoption Explosion**:
    - Virtuals Protocol: All ACP agents auto-register on ERC-8004
    - Avalanche C-Chain: Now supports ERC-8004 (5+ chains total!)
    - Davide Crapis (EF dAI lead) interview on Unchained
    - Agent infrastructure reaching critical mass
  - **New ePrint papers (Feb 6-7)**:
    - ePrint 2026/194: Unified hardware for hash-based signatures
    - ePrint 2026/193: Atkin/Weber modular polynomials (39% improvement)
    - ePrint 2026/191: PEARL-SCALLOP active attack (4 oracle calls!)
    - ePrint 2026/189: Shared/leakage-free MAYO (PQ threshold sigs)
  - **NIST MPTS 2026 details**: Workshop completed Jan 26-29, talks identified
  - **Ecosystem status**: Glamsterdam/Hegotá timelines confirmed
  - **INDEX.md updated**: Now 120+ sources catalogued
- [2026-02-08 1AM] **📊 Sunday Early Morning Cron Research Update**
  - **No major new ePrint papers** — Sunday quiet period confirmed
  - **FairTraDEX paper added** (arXiv 2202.06384): Foundational FBA+ZK DEX work
    - Formal game-theoretic guarantees against MEV
    - Fixed-fee model independent of order size
    - Uses ZK set-membership proofs
  - **ERC-8004 architecture detailed** (from Odaily deep-dive):
    - Three registries: Identity (NFT), Reputation (reviews), Verification (ZK/TEE)
    - Designed as chain-agnostic universal standard
    - Vision extends beyond trading to full agent collaboration
  - **Hegota competition stable**: FOCIL vs EIP-8105 vs EIP-8141 dynamics unchanged
  - **Strategic window**: ~3 weeks until Feb 26 headliner decision
  - **INDEX.md updated**: Now 125+ sources catalogued
- [2026-02-07 11PM] **📊 Late Saturday Cron Research Update**
  - **🏛️ EF Checkpoint #8 Deep-Dive** (Jan 20, 2026 blog post):
    - Glamsterdam headliners CONFIRMED: ePBS (EIP-7732) + BALs (EIP-7928)
    - **FOCIL moved OUT of Glamsterdam** to Hegotá (scope reduction!)
    - Hegotá headliner decision: **Feb 26, 2026** (3 weeks away)
    - Non-headliner EIP deadline: 30 days after headliner decision
    - 17 Considered EIPs for Glamsterdam (down from 50!)
    - Fusaka successfully shipped PeerDAS; BPO forks now reality
  - **📊 Hegotá Competition Clarified**:
    - FOCIL vs EIP-8105 explicitly competing for headliner slot
    - Only "one competing proposal" besides FOCIL per EF blog
    - EIP-8141 (Frame Tx) mentioned but not in direct headliner race
    - Community feedback period: Feb 5-26
  - **🔬 Research Coverage Confirmed**:
    - All major search queries returning known sources
    - No significant new ePrint papers since 10PM update
    - Uniswap CCA documentation comprehensive and available
    - ERC-8004 adoption trajectory confirmed (24k+ agents)
  - **⏰ Timeline Pressure**:
    - Glamsterdam scope freeze: End of February
    - Hegotá headliner decision: Feb 26
    - Our opportunity window for influence: ~3 weeks
- [2026-02-08 10PM] **📊 Saturday Night Cron Research Update**
  - **🤖 ERC-8004 Adoption Accelerating**:
    - **24,000+ agents registered** on mainnet — major adoption milestone!
    - **The Graph backing ERC-8004 + x402** — critical indexing infrastructure
    - **MultiversX integrated x402** — cross-chain adoption expanding
    - **x402 Hackathon** in SF with Google, Coinbase, SKALE
    - Agent identity now first-class concern for DEX design
  - **🔬 New ePrint Papers (Feb 7-8)**:
    - **BABE** (verification theater follow-up): Bitcoin proof verification 1000× cheaper using witness encryption
    - **PQC Migration for Blockchain**: Comprehensive Dec 2025 analysis of post-quantum challenges
    - **Beyond LWE**: Lattice-based HE framework with LIP instantiation
    - **Collaborative Traceable SS**: Full paper on public tracing (builds on 2026/181)
  - **📦 RNBW Auction Final Confirmation**:
    - Clearing price: **$0.13** (started $0.10, +30% price discovery)
    - FDV at clearing: **~$130 million**
    - KuCoin listed with bot support (Feb 5)
    - **Validates CCA price discovery mechanism empirically**
  - **⚙️ Glamsterdam Status**:
    - **On track** despite Fusaka testing issues
    - bals-devnet-2 launched Feb 4
    - Scope freeze confirmed: end of February
    - Mainnet target: May/June 2026
  - **🆕 Vitalik "Glamsterdam Ultimatum"**:
    - Frustration with L2 "copypasta" driving L1 focus
    - Gas limit 3× increase (60M → 200M) enables L1 clearing
    - Reinforces our L1-first strategy
  - **INDEX.md updated**: Now 110+ sources catalogued
- [2026-02-07 6PM] **📊 Saturday 6PM Cron Research Update**
  - **🔄 VITALIK L2 PARADIGM SHIFT** (Feb 3, 2026) — Major strategic implications!
    - "Rollup-centric roadmap no longer makes sense"
    - L2 usage dropped **50%**: 58.4M → 30M monthly addresses
    - Ethereum L1 users **doubled**: 7M → 15M addresses
    - L1 fees now very low; gas limit increasing 3× in 2026
    - L2s must find new value: privacy, specialized VMs, non-financial apps
    - **Native rollup precompile** proposed for ZK-EVM verification
  - **🛡️ Ethereum Foundation "Trillion Dollar Security Dashboard"** (Feb 5-6, 2026)
    - Part of "1TS" initiative from May 2025
    - Six security dimensions: UX, smart contracts, infrastructure, consensus, monitoring, social governance
    - Goal: Prepare network for trillions in on-chain value
  - **📅 Glamsterdam Timeline Confirmed** (CryptoAPIs deep-dive):
    - Q1 2026: Devnet testing (bals-devnet-2, epbs-devnet-0 active)
    - Late Q1 2026: Scope freeze (end of February)
    - H1 2026: Mainnet (May/June)
    - ePBS (EIP-7732) + BALs (EIP-7928) for parallel execution
    - Gas limit: 60M → 200M (3× increase)
  - **New ePrint papers:**
    - 2026/189: Shared and leakage free MAYO (threshold signatures)
    - 2026/192: Verification Theater — critical analysis of formal verification claims
  - **Strategic insight**: L1 scaling changes our deployment calculus
    - Glamsterdam 3× gas + low fees = L1 uniform clearing now viable
    - ePBS removes relay centralization
    - BALs enable parallel batch clearing
  - **INDEX.md & IDEAS.md updated**: Now 80+ sources catalogued

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

## Strategic Decisions (Feb 7-8, 2026)
*From main session feedback on research questions:*

| Decision | Direction | Rationale |
|----------|-----------|-----------|
| **Target Chain** | ~~L2 first~~ **L1 primary** ✅ | Vitalik L2 critique + L1 scaling changes calculus |
| **Encryption** | Threshold (BEAST-MEV) primary | WE circular dependency unsolved; WE = Plan B |
| **Agent Support** | ~~Low priority~~ **V1 REQUIRED** ✅ | 24k agents week 1 = real demand (Feb 8 update) |
| **Timeline** | Glamsterdam compatibility | ePBS (EIP-7732) changes MEV landscape |
| **Chainlink Outreach** | **YES** ✅ | Manuel Vidigueira (ePrint 2026/182) — angle: accountability layer for EIP-8105 clearing |

**🆕 New Data Reshaping Strategy (Feb 7 6PM):**
- L2 usage dropped 50% (58.4M → 30M addresses)
- Ethereum L1 users doubled (7M → 15M addresses)
- Glamsterdam: 3× gas limit (60M → 200M)
- EIP-8105 provides native L1 encrypted mempool

**Revised Priority Stack:**
1. ~~L2 deployment~~ → **Ethereum L1 deployment (EIP-8105 + Glamsterdam)**
2. Threshold encryption integration path
3. Parallel execution design (BALs/EIP-7928)
4. Specialized L2s as secondary (privacy, high-frequency)
5. Agent/WE exploration → v2

**User Confirmed (Feb 7, 6PM):**
- [x] ✅ L1 primary deployment strategy confirmed
- [x] ✅ Glamsterdam (H1 2026) timeline alignment confirmed
- [x] ✅ Verification strategy: formal verification core + multi-audit + bug bounty

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

### Insight 21: Witness Encryption May Eliminate Committee Trust (NEW 2026-02-07 4PM)
ePrint 2026/175 shows practical witness encryption for SNARK verification:
- **Concept**: Encrypt order to statement "this order is in a batch with valid proof π"
- **Decryption**: Anyone with proof π can decrypt — no committee needed!
- **Trustless**: No threshold assumption, no key holders, no coordinator
- **Challenge**: Circular dependency (need orders to prove, need proof to decrypt)
- **Potential solution**: Homomorphic operations on encrypted orders?
- **Status**: Research direction; may work for small batches or specific use cases
- **Implication**: Threshold (BEAST-MEV) remains primary for high-throughput, but WE is interesting backup

### Insight 22: SNARKs Going Mainstream — Cost Trajectory (NEW 2026-02-07 4PM)
a16z's "17 Things for 2026" notes SNARK overhead is dropping dramatically:
- Previously: 1,000,000× overhead vs native computation
- Now: Becoming practical outside blockchain
- Drivers: Hardware acceleration, proving markets (Brevis ProverNet), optimized circuits
- **Implication for us**: ZK-verified clearing will become more practical over time
- **Strategy**: Design for ZK now (even if expensive), costs will drop
- **Backup**: Fraud-proof approach for near-term deployment

### Insight 23: Agent Economy Requires New Order Formats (NEW 2026-02-07 4PM)
a16z highlights "Know Your Agent" (KYA) as critical missing primitive:
- Non-human identities 96:1 vs humans in financial services
- Agents need cryptographic credentials linking to principals
- x402 protocol enables agent-to-agent payments
- **Design consideration**: Our order format should support agent-signed orders
- **Components**: principal address, agent identity, constraints, approval chain
- **Alignment**: EIP-8141 Frame Transactions (signature-scheme agnostic)

### Insight 24: Encryption Technology Diversifying Rapidly (NEW 2026-02-07 5PM)
The encrypted computation landscape is no longer threshold-only:
- **Threshold** (BEAST-MEV, Shutter): Ethereum-focused, production-ready
- **MPC** (Arcium): Solana mainnet alpha, compute on encrypted data
- **FHE** (Fhenix DBFV): EVM research, breakthrough in noise management
- **Garbled Circuits** (gcVM): ~500 cTPS for private EVM
- **Witness Encryption** (ePrint 2026/175): Trustless, no committee
- **TEE** (SUAVE): Hardware trust, in development
- **Implication**: Design clearing layer to be **encryption-agnostic**
- **Near-term**: Build on threshold (BEAST-MEV/EIP-8105)
- **Future**: FHE integration when mature (compute-on-encrypted clearing)

### Insight 25: MPC Enables Richer Private DeFi (Arcium lesson, NEW 2026-02-07 5PM)
Arcium's MPC approach enables more than threshold:
- Threshold: Encrypt → Decrypt → Execute (reveal at batch time)
- MPC: Compute on encrypted data → Never reveal intermediate state
- **Umbra Private** (first Arcium app) shows feasibility:
  - Anonymous transfers and swaps
  - Encrypted balances
  - SDK for developers
- **Trade-off**: MPC has higher coordination cost than threshold
- **Strategic implication**: Arcium covers Solana; we focus on EVM/Ethereum

### Insight 26: Production Code Availability Accelerates Research (NEW 2026-02-07 5PM)
Uniswap CCA v1.1.0 being MIT-licensed and audited is a gift:
- Can study production-grade clearing algorithm in Solidity
- Can benchmark actual gas costs from test suite
- Can extend/adapt rather than build from scratch
- Three independent audits provide security confidence
- **Action**: Clone repo, analyze clearing price computation
- **Risk**: If CCA covers our use case, contribution space narrows

### Insight 27: L1 Scaling Shifts Deployment Strategy (NEW 2026-02-07 6PM)
Vitalik's "rollup-centric roadmap no longer makes sense" has major implications:
- **L2 usage dropped 50%** (58.4M → 30M addresses) while L1 doubled (7M → 15M)
- **L1 fees are now very low** — the scaling justification for L2s is weakening
- **Glamsterdam 3× gas limit** (60M → 200M) makes L1 even more attractive
- **Implication for us**: L1 deployment of clearing layer may be more viable than expected
- **Strategy shift**: Don't assume "L2 first" — L1 uniform clearing could work with:
  - EIP-8105 encrypted mempool (native)
  - ePBS removing relay centralization
  - BALs enabling parallel batch clearing
- **L2 role redefined**: Privacy, specialized apps, not just "cheaper Ethereum"
- **Our opportunity**: Clearing layer that works on L1 (primary) + L2s (for specialized use cases)

### Insight 28: Defense in Depth Requires Formal Verification Awareness (NEW 2026-02-07 6PM)
ePrint 2026/192 "Verification Theater" warns about false assurance:
- Formally verified crypto libraries can still have vulnerabilities
- Marketing claims often exceed actual verification scope
- **Implication**: Our clearing layer shouldn't rely on single verification approach
- **Strategy**: Multiple independent audits + formal verification + economic incentives
- **Defense layers**:
  1. Cryptographic (encryption, proofs)
  2. Economic (slashing, bonds)
  3. Social (reputation, transparency)
  4. Operational (monitoring, incident response)

### Insight 29: Public Tracing Eliminates Tracer Trust Assumption (NEW 2026-02-07 7PM)
ePrint 2026/181 Collaborative Traceable Secret Sharing (CTSS) is a breakthrough:
- Prior traceable SS (Goyal-Song-Srinivasan, Boneh-Partap-Rotem) needed designated tracer
- CTSS eliminates private trace keys AND private verification keys
- Tracing requires collaboration from threshold parties (aligns with decentralization)
- **Verification is FULLY PUBLIC** — anyone can verify misbehavior proofs
- Polynomial-time tracing with minimal share overhead
- **Application to encrypted mempools**:
  - Keyper shares become traceable without central authority
  - Collusion to decrypt early produces public proof
  - Integrates with existing Shamir/Blakley infrastructure
- **Critical implication**: Closes the "who watches the watchers" gap in threshold encryption

### Insight 30: Universal Accountability Compiler Enables Formal Guarantees (NEW 2026-02-07 7PM)
ePrint 2026/182 presents τ_{zk-scr} — a universal compiler for accountability:
- Transforms ANY semi-honest crash-failure protocol into Byzantine-tolerant accountable version
- Uses Accountable Universal Composability (AUC) framework (S&P 2023)
- **Guarantees**:
  - For f ≤ t_ε: preserves privacy, correctness, output delivery
  - For f > t_ε: either safety preserved OR all correct processes get verifiable misbehavior proofs
- **Relevance for clearing layer**:
  - Could apply compiler to our batch clearing protocol
  - Get formal accountability guarantees "for free"
  - Proofs involve "significant subset" of faulty parties — deterrent effect
- **Collaboration potential**: Chainlink Labs co-author (Manuel Vidigueira)
  - Already have Chainlink relationship through FSS
  - Could explore joint work on accountable clearing

### Insight 31: Flow's Alternative Approach to MEV Resistance (NEW 2026-02-07 7PM)
Flow Network claims native MEV resistance via different architecture:
- Native VRF for unpredictable ordering
- Scheduled Transactions for time-locked execution
- "Actions" for automated trigger-based execution
- 40M users, 950M transactions — proven at scale
- **Trade-offs vs our approach**:
  - Flow: Proprietary chain, not EVM-compatible
  - Ours: Works on existing Ethereum ecosystem
  - Flow: VRF-based (probabilistic ordering fairness)
  - Ours: Uniform clearing (ordering irrelevant)
- **Key difference**: Flow still has ordering; we eliminate ordering importance entirely
- **Worth studying**: Their VRF + scheduling mechanism for hybrid approaches

### Insight 32: Agent Economy Infrastructure Is Production-Ready (NEW 2026-02-07 8PM)
ERC-8004 deployment marks a paradigm shift:
- **The standard**: On-chain identity, reputation, and discovery for AI agents
- **Adoption velocity**: Base, BNB Chain, Polygon deployed within days of mainnet
- **Key collaborators**: EF dAI Team, MetaMask, Google, Coinbase
- **Companion protocol**: x402 for HTTP-based agent-to-agent payments
- **Implication for DEX**: Agent-signed orders are now a first-class concern
- **Design requirement**: Our clearing layer must support agent-native order formats
- **Strategic opportunity**: First MEV-resistant DEX with agent compatibility = competitive moat
- **Data point**: 96:1 ratio of non-human to human identities in finserv (a16z)

### Insight 33: Hegota Headliner Competition Favors Layered Approach (NEW 2026-02-07 8PM)
Three proposals competing, but not mutually exclusive:
- **FOCIL**: Censorship resistance (consensus building, likely #1)
- **EIP-8105**: Encrypted mempool (Shutter champion, MEV protection)
- **EIP-8141**: Frame Transactions (Vitalik endorsed, post-quantum + AA)
- **Key dynamic**: FOCIL + EIP-8105 positioned as "complementary"
- **Implication**: Encrypted mempool likely to ship in Hegota, even if not headliner
- **Our strategy**: Design for EIP-8105 integration, support out-of-protocol fallback
- **Bonus**: EIP-8141's signature-agnostic design aligns with agent-signed orders

### Insight 34: Agent Economy Infrastructure Reaching Critical Mass (NEW 2026-02-08)
ERC-8004 adoption is accelerating faster than expected:
- **24,000+ agents registered** on mainnet in first week
- **Cross-chain adoption**: Base, BNB Chain, Polygon, now MultiversX
- **Infrastructure support**: The Graph providing indexing for agent registries
- **Payment rails**: x402 protocol enables HTTP-native agent-to-agent payments
- **Implications for our DEX design**:
  1. Agent-signed orders are now a production requirement, not future consideration
  2. Integration with ERC-8004 identity verification adds value
  3. x402 could enable pay-per-trade agent authorization
  4. Clearing layer should validate agent constraints (spending limits, allowed pairs)
- **Competitive advantage**: First MEV-resistant DEX with native agent support = market positioning

### Insight 35: Witness Encryption for Bitcoin Validates WE Research Direction (NEW 2026-02-08)
BABE paper (ePrint 2026) shows WE becoming practical for blockchain:
- **Bitcoin proof verification 1000× cheaper** using witness encryption
- **Mechanism**: WE + 2PC for pairing-based Groth16 verification
- **Off-chain**: 42 GiB garbled circuits (vs prior BitVM3)
- **On-chain**: Minimal verification costs
- **Relevance to us**:
  1. WE is maturing beyond theoretical — production-adjacent research now
  2. Could eventually enable trustless order encryption (no committee)
  3. WE + ZK clearing could be ultimate trustless design
  4. Keep WE as research track, threshold (BEAST-MEV) for production
- **Timeline**: WE for DEX likely 2027+; focus on threshold for 2026

## Literature Search Queries for Next Update
- "Uniswap CCA clearing price algorithm" — study Solidity implementation ✅ Found repo!
- "EIP-8141 frame transaction" — track competing proposals
- "NIST MPTS 2026 recordings proceedings" — find workshop materials (already happened Jan 26-29!)
- "Brevis ProverNet ZK marketplace" — decentralized proof generation
- "witness encryption SNARK blockchain" — track WE developments
- "ePrint 2026/175 witness encryption" — follow-up on [[alloc] init] paper
- "Rainbow RNBW Base transaction" — empirical CCA data analysis
- "Chainlink Atlas SVR integration" — OEV capture mechanisms
- "ePrint 2026 batch threshold" — track new threshold crypto papers
- "Glamsterdam scope freeze February" — monitor final feature list ✅ Confirmed end of Feb
- "EIP-7928 Block-Level Access Lists parallel" — parallel execution MEV impact
- "Know Your Agent KYA crypto" — agent identity standardization ✅ ERC-8004 found!
- "x402 protocol payments" — agent-to-agent payment infrastructure ✅ Pairs with ERC-8004
- "Hegota headliner decision" — track which EIPs are selected
- "Arcium Umbra SDK" — study private DEX reference implementation
- "Fhenix DBFV paper" — get technical details on noise management
- "gcVM MPC garbled circuits EVM" — alternative to threshold/FHE
- "Vitalik L2 rollup roadmap February 2026" — track L1/L2 strategy evolution
- "Ethereum Trillion Dollar Security Dashboard" — study 1TS initiative
- "native rollup precompile ZK-EVM" — Vitalik's proposed L2 infrastructure
- "Ethereum gas limit increase 2026" — track Glamsterdam throughput gains
- "ePrint 2026/181 traceable secret sharing" — CTSS public tracing details
- "ePrint 2026/182 accountable UC" — τ_{zk-scr} compiler implementation
- "Chainlink Labs Manuel Vidigueira" — potential collaboration contact
- "AUC framework S&P 2023" — formal accountability foundations
- "Flow blockchain VRF scheduled transactions MEV" — alternative approach analysis
- **NEW**: "ERC-8004 trustless agent registry" — study implementation details
- **NEW**: "ERC-8004 Ethereum Foundation dAI Team" — track development
- **NEW**: "x402 HTTP payment protocol agent" — agent payment mechanics
- **NEW**: "Uniswap CCA GitHub source code" — analyze clearing algorithm
- **NEW**: "ePrint 2026/190 threshold ECDSA" — O(1) communication threshold

## Next Research Cycle (Feb 8-14)
### Priority 1: Empirical Analysis
- [ ] Fetch RNBW auction transactions from Base explorer
- [ ] Reverse-engineer CCA clearing price computation
- [ ] Document gas costs for production clearing
- [x] Study mempool auditing limitations (arXiv 2601.14996) ✅
- [ ] Clone Uniswap CCA repo, analyze Solidity implementation
- [ ] Benchmark CCA gas costs from test suite

### Priority 2: Technical Deep-Dives
- [ ] Deep-read ePrint 2026/175 (witness encryption for SNARKs)
- [ ] Study ePrint 2026/031 ThFHE attack implications
- [ ] Review ePrint 2026/021 for post-quantum threshold applicability
- [ ] Analyze EIP-7928 BALs impact on MEV (parallel execution)
- [ ] Find NIST MPTS 2026 recordings/proceedings (workshop completed Jan 26-29)
- [ ] Study ePrint 2026/170 gcVM for private EVM applications
- [ ] Review arXiv 2302.01177 FBA welfare model
- [x] Analyze ePrint 2026/192 "Verification Theater" implications ✅ (multi-layer strategy)
- [ ] Deep-read ePrint 2026/181 (CTSS) — public tracing mechanisms
- [ ] Deep-read ePrint 2026/182 (τ_{zk-scr} compiler) — accountability guarantees
- [ ] Study AUC framework (S&P 2023) — formal foundations for accountability
- [ ] Analyze Flow's VRF + scheduled tx approach (alternative MEV resistance)
- [ ] **🆕 NEW**: Study ERC-8004 implementation and registry interfaces
- [ ] **🆕 NEW**: Analyze x402 protocol for agent payment flows
- [ ] **🆕 NEW**: Review ePrint 2026/190 three-round threshold ECDSA

### Priority 3: Design Work
- [ ] Draft multi-provider clearing interface spec
- [ ] Sketch ZK clearing circuit requirements
- [ ] Outline formal security model for clearing layer
- [ ] Evaluate WE as alternative to threshold for order encryption
- [x] Design "agent-compatible" order format (KYA considerations) ✅ (draft in IDEAS.md)
- [ ] Address 30-second ordering limitation in our spec (from arXiv 2601.14996)
- [ ] Design encryption-agnostic clearing interface (threshold/MPC/FHE)
- [ ] Study Arcium/Umbra for private DEX UX patterns
- [ ] Design for L1 parallel execution (BALs/EIP-7928 integration)
- [x] Draft multi-layer verification strategy (per ePrint 2026/192) ✅ (outlined in IDEAS.md)
- [ ] Integrate CTSS (ePrint 2026/181) into Keyper accountability spec
- [ ] Apply τ_{zk-scr} compiler (ePrint 2026/182) to clearing protocol design
- [ ] **🔥 PRIORITY**: Reach out to Chainlink Labs (Manuel Vidigueira) — angle: accountability layer for EIP-8105 clearing
- [ ] Compare VRF-based vs uniform-clearing MEV approaches (Flow vs our design)
- [ ] **🔥 PRIORITY (v1)**: Integrate ERC-8004 identity verification into order validation
- [ ] **🔥 PRIORITY (v1)**: Design agent constraint system (allowedPairs, maxOrderSize, etc.)
- [ ] **🆕 NEW**: Spec Hegota compatibility (EIP-8105 + EIP-8141 alignment)

### Priority 4: Confirmed Actions (Feb 7 11PM)
1. ✅ **Hegotá EIP proposal**: Prepare "ZK-Verified Uniform Clearing Layer" non-headliner proposal
   - Target: Submit within 30 days of Feb 26 headliner decision
   - Compatibility: Works with EIP-8105 OR FOCIL+Shutter
2. ✅ **Chainlink outreach**: Contact Manuel Vidigueira (ePrint 2026/182) this week
   - Angle: Accountability layer for clearing
   - Platform: Email/DM
3. ✅ **Agent support v1**: ERC-8004 compatible order format is v1 requirement
   - 24k+ agents registered proves demand

### Priority 5: Strategic Questions for User Input
1. **Target chain**: ~~L2 first~~ Given Vitalik's L2 critique, prioritize Ethereum L1?
   - **New data**: L2 usage -50%, L1 users +114%, L1 fees now low
   - **Recommendation**: L1 primary, specialized L2 secondary
   - **Status**: ✅ Confirmed by user (Feb 7, 6PM)
2. **Witness encryption**: Deep exploration track or keep focus on threshold?
   - **Recommendation**: Threshold primary, WE as research track
3. **Agent support**: Priority level for KYA/agent-signing in v1?
   - **🆕 NEW DATA**: ERC-8004 deployed to mainnet Jan 29, 2026!
   - Already adopted by Base, BNB Chain, Polygon
   - **Recommendation**: Integrate agent support in v1 (competitive advantage)
4. **Timeline alignment**: Aim for Glamsterdam compatibility (H1 2026) first?
   - **New data**: Scope freeze end of Feb, mainnet May/June
   - **Status**: ✅ Confirmed by user (Feb 7, 6PM)
5. **FHE path**: Monitor Fhenix DBFV or active research track?
6. **Verification strategy**: How much formal verification vs other methods?
   - **Status**: ✅ Confirmed by user (Feb 7, 6PM) — multi-layer approach
7. **🆕 Chainlink collaboration**: Reach out to Manuel Vidigueira (ePrint 2026/182)?
   - **Status**: ✅ Confirmed YES — reach out this week (Feb 8-14)
   - **Angle**: Accountability layer for EIP-8105 clearing
8. **🆕 Agent priority**: Given ERC-8004 is now live, prioritize agent compatibility?
   - **Status**: ✅ Confirmed — v1 REQUIREMENT (24k+ agents = proven demand)
9. **🆕 Hegotá EIP proposal**: Should we prepare a non-headliner proposal?
   - **Status**: ✅ Confirmed YES — prepare "ZK-Verified Uniform Clearing Layer"
   - **Deadline**: ~30 days after Feb 26 headliner decision
