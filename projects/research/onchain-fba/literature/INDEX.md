# Literature Index — On-Chain Trustless FBA

**Last Updated**: 2026-02-04 (comprehensive initial sweep)

## Categories
- [Foundational MEV Research](#foundational-mev-research)
- [Batch Auctions & Mechanism Design](#batch-auctions--mechanism-design)
- [Threshold Encryption](#threshold-encryption)
- [Encrypted Mempools & Sequencing](#encrypted-mempools--sequencing)
- [Privacy-Focused DEXs](#privacy-focused-dexs)
- [Current Solutions (Trust Analysis)](#current-solutions-trust-analysis)
- [Fair Ordering Protocols](#fair-ordering-protocols)
- [Traditional Finance Literature](#traditional-finance-literature)
- [SoK & Surveys](#sok--surveys)
- [Implementation References](#implementation-references)

---

## Foundational MEV Research

### Flash Boys 2.0 (Daian et al., 2019)
- **ArXiv**: https://arxiv.org/abs/1904.05234
- **Key contribution**: Coined "Miner Extractable Value" (MEV), documented PGAs
- **Relevance**: Foundational problem definition

### High-Frequency Trading on DEXs (Zhou et al., 2020)
- **ArXiv**: https://arxiv.org/abs/2009.14021
- **Key contribution**: Formalizes sandwich attacks with probability analysis

### Cross-Domain MEV (Obadia et al., 2021)
- **ArXiv**: https://arxiv.org/abs/2112.01472
- **Key insight**: L2s don't solve MEV, just shift it ("REV")

---

## Batch Auctions & Mechanism Design

### ⭐ Leaderless Auctions (Paradigm, Feb 2024)
- **URL**: https://www.paradigm.xyz/2024/02/leaderless-auctions
- **Key contribution**: 4-round trustless auction, no leader
- **Mechanism**: Threshold encryption + fault economics
- **Gap**: No uniform clearing, not permissionless
- **Our opportunity**: Add uniform clearing layer

### A2MM (Zhou et al., 2021)
- **ArXiv**: https://arxiv.org/abs/2106.07371
- **Key contribution**: On-chain atomic MEV collection

### Gnosis Batch Auction Research
- **GitHub**: https://github.com/gnosis/dex-research/releases
- **Papers**: 
  - "Multi-token Batch Auctions with Uniform Clearing Prices"
  - "Multi-token Batch Auctions with Uniform Clearing Prices on Plasma"
- **Relevance**: Mathematical optimization for clearing prices
- **Our use**: Reference for clearing price computation

---

## Threshold Encryption

### ⭐⭐ Batched Threshold Encryption (Garg, Piet, Policharla, 2024)
- **ePrint**: https://eprint.iacr.org/2024/669
- **Key contribution**: O(n) communication for B transactions
- **Concrete efficiency**: <6ms encrypt, 80 bytes/party/batch
- **Critical**: "Pitfalls in prior approaches" — must read
- **Relevance**: Makes mempool encryption practical at scale

### ⭐⭐ Threshold Encryption with Silent Setup (Garg et al., 2024)
- **ePrint**: https://eprint.iacr.org/2024/263
- **Key contribution**: NO interactive setup — deterministic joint pubkey
- **Properties**: Asynchronous, multiverse, DYNAMIC THRESHOLD
- **Efficiency**: <7ms encrypt, <1ms partial decrypt
- **Game-changer**: ENABLES PERMISSIONLESS threshold encryption

### vetKeys (DFINITY)
- **GitHub**: https://github.com/dfinity/vetkeys
- **Medium**: https://medium.com/dfinity/the-internet-computers-privacy-era-vetkeys-unlocked
- **Key contribution**: Production threshold key derivation on IC
- **Relevance**: Working implementation to study
- **Audit**: NCC Group cryptography review completed

### Shutter Network
- **Blog**: https://blog.shutter.network/introducing-shutter-api-threshold-encryption-service/
- **Status**: Production on Gnosis Chain
- **Architecture**: Decentralized Keyper network
- **Use cases**: Voting (Snapshot), auctions, gaming

---

## Encrypted Mempools & Sequencing

### Radius (PVDE)
- **Docs**: https://docs.theradius.xyz/testnet/portico-testnet/encrypted-mempool
- **Mirror**: https://mirror.xyz/0x957084A1F20AB33cfA0cE07ed57F50c05954999C/TvlP4n2W1qbP9tRMSO2-CfNwzw5WedtbC5yC5nFUezo
- **Mechanism**: Practical Verifiable Delay Encryption (PVDE)
- **Innovation**: Time-lock puzzle + zk-SNARK proof
- **Process**: Encrypt → Submit → Pre-confirm → Optional early reveal
- **Relevance**: Alternative to threshold (single-party solvable)

### SUAVE (Flashbots)
- **Docs**: https://writings.flashbots.net/the-future-of-mev-is-suave
- **GitHub**: https://github.com/flashbots/suave-geth
- **Mechanism**: TEE (Intel SGX) for confidential execution
- **Trust**: Initially trust Flashbots, roadmap to trustless
- **Our verdict**: TEE = hardware trust assumption

### Espresso Sequencer
- **HackMD**: https://hackmd.io/@EspressoSystems/EspressoSequencer
- **Key feature**: Decentralized Timeboost for fair ordering
- **MEV approach**: PBS with ordering policies at builder level
- **Relevance**: Shared sequencer architecture

---

## Privacy-Focused DEXs

### ⭐ Penumbra
- **Guide**: https://guide.penumbra.zone/overview/dex
- **Devcon Talk**: https://archive.devcon.org/archive/watch/6/penumbra-building-a-private-dex-with-zkps-and-threshold-cryptography/
- **Architecture**:
  - ZKPs for transaction privacy
  - "Flow encryption" — threshold crypto for shared state
  - Batch execution per block (~5 sec)
  - Concentrated liquidity positions (anonymous)
- **Key insight**: "ZKPs alone not enough — need shared state"
- **MEV protection**: Batch execution, no intra-block ordering
- **Automatic arbitrage**: Protocol burns arbitrage profits
- **Relevance**: Most complete private DEX design

---

## Current Solutions (Trust Analysis)

### Flashbots Auction
- **Docs**: https://docs.flashbots.net/flashbots-auction/overview
- **Trust**: ❌ Builders/relays see transactions
- **Verdict**: NOT TRUSTLESS

### CoW Protocol
- **Docs**: https://docs.cow.fi/cow-protocol/concepts/introduction/fair-combinatorial-auction
- **Mechanism**: Off-chain solver competition, batch execution
- **Trust**: ❌ Solvers are trusted third parties
- **Good parts**: Uniform Directed Clearing Prices (UDP)
- **Verdict**: NOT TRUSTLESS but good MEV protection via UDP

### Chainlink FSS
- **Blog**: https://blog.chain.link/chainlink-fair-sequencing-services/
- **Mechanism**: Oracle network for fair ordering (Aequitas)
- **Trust**: ⚠️ Oracle network trust (distributed)
- **Supports**: Threshold encryption of transactions
- **Verdict**: SEMI-TRUSTLESS

---

## Fair Ordering Protocols

### Aequitas (Kelkar et al., 2020)
- **ePrint**: https://eprint.iacr.org/2020/269
- **Key contribution**: First formal definition of order-fairness
- **Property**: If majority receive T1 before T2, T1 ordered first
- **Limitation**: Performance overhead in original protocols

### MEV Auctions Considered Harmful (Offchain Labs, 2020)
- **Medium**: https://medium.com/offchainlabs/mev-auctions-considered-harmful
- **Argument**: MEV auction revenue = tax on users
- **Problems**: Centralizes MEV extraction, enables censorship

---

## Traditional Finance Literature

### Call Auction Trading
- **Springer**: https://link.springer.com/rwe/10.1007/978-3-030-73443-5_36-1
- **Key topics**: Price discovery, order book building, critical mass
- **Relevance**: Traditional market design insights

### FBA vs Continuous Auctions
- **ResearchGate**: Strategic Market Choice paper (2015)
- **Relevance**: Fast vs slow trader dynamics

---

## SoK & Surveys

### ⭐ SoK: Preventing Transaction Reordering (Heimbach, 2022)
- **ArXiv**: https://arxiv.org/abs/2203.11520
- **Critical finding**: "No scheme fully meets all demands"
- **Categories**: Auctions, encryption, fair ordering
- **Verdict**: Confirms unsolved problem

### SoK: Decentralized Finance (Klages-Mundt et al., 2021)
- **ArXiv**: https://arxiv.org/abs/2101.08778
- **Contribution**: Technical vs economic security distinction

### Deciphering Encrypted Mempools
- **Medium**: https://medium.com/@chaisomsri96/deciphering-encrypted-mempools-2-project-insights-97ec257d7951
- **Coverage**: SUAVE, Shutter, Radius comparison

---

## Implementation References

### Gnosis Protocol v1/v2
- **GitHub**: https://github.com/gnosis/dex-contracts
- **Relevance**: Batch auction smart contracts

### Gnosis Auction (IDO)
- **GitHub**: https://github.com/gnosis/ido-contracts
- **Relevance**: Batch auction for token sales

### ERC-5732: Commit Interface
- **EIP**: https://eips.ethereum.org/EIPS/eip-5732
- **Relevance**: Standard for commit-reveal

### Commit-Reveal² (2025)
- **ArXiv**: https://arxiv.org/html/2504.03936v2
- **Innovation**: Randomized reveal order
- **Relevance**: Griefing resistance improvements

---

## Key Synthesis: Our Approach

**Three advances to combine:**
1. **Silent Setup** (2024/263) → Permissionless threshold encryption
2. **BTE** (2024/669) → Efficient batch decryption
3. **Uniform Clearing** (Gnosis research) → MEV-resistant execution

**"Silent Batch Auction" Protocol:**
- Phase 1: Encrypt orders to deterministic threshold key
- Phase 2: Committee generates decryption shares (O(n) cost)
- Phase 3: Compute uniform clearing price on-chain
- All orders execute at same price → sandwich impossible

---

## Papers to Deep-Read (Priority)

1. [ ] Silent Setup (ePrint 2024/263) — permissionless enabler
2. [ ] BTE (ePrint 2024/669) — efficiency breakthrough
3. [ ] Gnosis clearing price optimization paper
4. [ ] Penumbra flow encryption details
5. [ ] Paradigm Leaderless Auctions full protocol

---

## ⭐⭐⭐ MAJOR NEW DISCOVERIES (2026-02-07)

### BEAST-MEV (Choudhuri, Faust, Garg et al., Aug 2025)
- **ePrint**: https://eprint.iacr.org/2025/1419
- **Key contribution**: First scheme combining BOTH Silent Setup + Batched Decryption
- **Critical**: This is essentially our "Silent Batch Auction" concept — ALREADY EXISTS!
- **Authors**: Same team behind original BTE and Silent Setup papers
- **Security**: Generic Group Model proof
- **Status**: Implemented and benchmarked
- **Our opportunity**: They address privacy, NOT uniform clearing — we can still contribute

### Weighted Batched Threshold Encryption (Babel, Das et al., Nov 2025)
- **ePrint**: https://eprint.iacr.org/2025/2115
- **Key contribution**: Extends BEAT-MEV to weighted settings (PoS validator stakes)
- **Improvements**: 
  - Quasilinear (not quadratic) in batch size via FFT-friendly punctured PRFs
  - 6× faster for 512 batch, 50× better communication for weighted validators
- **Relevance**: Makes encrypted mempools practical for PoS chains like Solana

### Silent Threshold Cryptography from Pairings (Waters & Wu, Aug 2025)
- **ePrint**: https://eprint.iacr.org/2025/1547
- **Key contribution**: Silent setup for expressive policies (monotone Boolean formulas)
- **Breakthrough**: Standard model security (not idealized model)
- **Compact**: 3 group elements for signatures, 4 for ciphertexts
- **Relevance**: Enables fine-grained access control without trusted setup

### USENIX Security '25: Practical Mempool Privacy
- **URL**: https://www.usenix.org/conference/usenixsecurity25/presentation/choudhuri
- **Key contribution**: Formal publication of BTE with pending transaction privacy
- **Achievement**: O(1) communication per decryption server per epoch

### Accountability Primitives (Shutter Blog Roundup)
- **Secret Sharing with Snitching** (ePrint 2024/1610): Proofs of reconstruction for punishment
- **Strong SSS** (ePrint 2025/1119): Insurance contract hedging resistance
- **Self-Incriminating Proofs** (ePrint 2024/794): At least one colluder gets caught
- **Traceable TE** (ePrint 2023/1724, Boneh et al.): Identify unauthorized decryption
- **Public Tracing** (ePrint 2025/1347, Canard et al.): On-chain automatic enforcement

### HAL 2025: Fast Gas-Efficient Private Sealed-Bid Auctions
- **HAL**: https://hal.science/hal-05061427v1
- **Authors**: Ballweg (HKUST), Goharshady (Oxford), Lin (HKUST)
- **Focus**: Optimizing on-chain auction gas costs
- **Relevance**: May have solutions for our clearing price computation

### GitHub Implementation: Tangle Network Silent TE Gadget
- **URL**: https://github.com/tangle-network/silent-threshold-encryption-gadget
- **Implementation**: Arkworks-based Silent Setup threshold encryption
- **Status**: Production-ready Rust code
- **Value**: Reference implementation for our work

---

## KEY SYNTHESIS: Our Updated Position

**State of the Art (as of Feb 2026):**
- BEAST-MEV solves: Privacy + Batching + No Trusted Setup ✅
- BEAST-MEV does NOT address: Uniform price clearing, on-chain execution

**Our Remaining Contribution Space:**
1. **Uniform Price Clearing Layer** — Design execution mechanism for BEAST-MEV outputs
2. **In-Protocol Arbitrage** — Adopt Penumbra's approach to internalize MEV
3. **Gas-Optimized On-Chain Clearing** — Make price computation practical on EVM
4. **Accountability Integration** — Combine with SSS/traceable TE for stronger guarantees

---

---

## ⭐⭐⭐⭐ CRITICAL NEW DISCOVERIES (2026-02-07 PM Update)

### EIP-8105: Universal Enshrined Encrypted Mempool (Shutter, Dec 2025)
- **Blog**: https://blog.shutter.network/introducing-the-universal-enshrined-encrypted-mempool-eip/
- **EthResearch**: https://ethresear.ch/t/universal-enshrined-encrypted-mempool-eip/23685
- **EIP PR**: https://github.com/ethereum/EIPs/pull/10943
- **Key contribution**: Native encrypted mempool for Ethereum mainnet!
- **Components**:
  1. New encrypted transaction type (envelope + encrypted payload)
  2. Technology-agnostic key provider registry (threshold, MPC, TEE, FHE, delay)
  3. Sub-slot key inclusion mechanism (inspired by ePBS)
- **Target**: Hegotá fork
- **Critical for us**: Layer 0/1 is being built — our Layer 2 contribution is needed!

### TrX: Encrypted Mempools in High Performance BFT (ePrint 2025/2032, Nov 2025)
- **ePrint**: https://eprint.iacr.org/2025/2032
- **Authors**: Fernando, Policharla (BEAST-MEV author!), Tonkikh, Xiang (Aptos Labs + Berkeley)
- **Key contribution**: First production-ready encrypted mempool in BFT consensus
- **Performance**: Only 27ms overhead (14%) vs baseline!
- **Insight**: "Closes gap between cryptographic defenses and production-ready consensus"
- **Relevance**: Proves encrypted mempools are production-viable

### Uniswap Continuous Clearing Auctions (CCA) (Nov 2025)
- **Blog**: https://blog.uniswap.org/continuous-clearing-auctions
- **Docs**: https://docs.uniswap.org/contracts/liquidity-launchpad/Overview
- **Key contribution**: Production uniform clearing price auctions on Uniswap v4
- **Features**:
  - Single market-clearing price per block
  - ZK Passport for private participation (with Aztec)
  - Automatic liquidity seeding on v4
  - Continuous price discovery with gradual supply release
- **First launch**: Aztec token ($59M auction)
- **CRITICAL**: This is exactly our Layer 2 concept in production! Must study.

### Jump Crypto Dual Flow Batch Auction (DFBA)
- **URL**: https://jumpcrypto.com/resources/dual-flow-batch-auction
- **Key contribution**: Separates orders into maker/taker flows
- **Mechanism**:
  - Two independent auctions per ~100ms
  - Each auction clears at uniform price
  - Makers and takers don't compete on latency
- **Innovation**: "Natural flow" focus — designed for real traders, not bots
- **Addresses**: Toxic flow problem, LVR for market makers
- **Potential integration**: Combine DFBA flow separation with BEAST-MEV encryption

### a16z "On the Limits of Encrypted Mempools" (July 2025)
- **URL**: https://a16zcrypto.com/posts/article/limits-encrypted-mempools/
- **Key contribution**: Critical analysis of encrypted mempool limitations
- **Key insights**:
  1. **Speculative MEV** still possible (guess and try)
  2. **Strong vs weak trust**: Consensus failures visible, early decryption undetectable
  3. Threshold encryption has STRONGER trust assumption than consensus
  4. Survey of approaches: TEEs, threshold, time-locks, witness encryption
- **Important**: We must address these concerns in our design
- **Shutter response**: https://blog.shutter.network/on-the-limits-of-encrypted-mempools-a-response-to-a16z-cryptos-analysts/

### Shutter + Primev: Threshold Encrypted Mempools with mev-commit (Dec 2025)
- **EthResearch**: https://ethresear.ch/t/threshold-encrypted-mempools-with-mev-commit-preconfirmations/23588
- **Blog**: https://blog.shutter.network/the-first-encrypted-mempool-is-coming-to-pbs-on-ethereum/
- **Key contribution**: First encrypted mempool in Ethereum PBS (out-of-protocol)
- **Architecture**: Combines Shutter threshold encryption + Primev preconfirmations
- **Status**: Proof of concept underway
- **Relevance**: Real-world path to encrypted txs on Ethereum L1

---

## KEY SYNTHESIS: Ecosystem Landscape (Feb 2026)

**What's Happening Now:**
1. **EIP-8105** → Native encrypted mempool coming to Ethereum (target: Hegotá)
2. **BEAST-MEV** → Academic foundation is solid, production-proven
3. **Shutter+Primev** → PBS integration in progress (out-of-protocol first)
4. **Uniswap CCA** → Uniform clearing in production (for token launches)
5. **Jump DFBA** → Flow separation concept gaining traction

**Where We Fit:**
| Layer | Component | Status | Our Role |
|-------|-----------|--------|----------|
| 3 | MEV Internalization | Penumbra only | Future work |
| 2 | **Uniform Clearing** | Uniswap CCA (limited), CoW (trusted) | **OUR FOCUS** |
| 1 | Encrypted Mempool | BEAST-MEV, EIP-8105, Shutter | Use as foundation |
| 0 | Settlement | Ethereum, L2s | Inherit |

**Remaining Contribution Space:**
1. **Trustless uniform clearing** that works with any encrypted mempool
2. **Gas-efficient clearing** (ZK or fraud-proof)
3. **Multi-pair batch clearing** (beyond single-asset auctions)
4. **Integration spec** for BEAST-MEV + clearing layer

---

## ⭐⭐⭐⭐⭐ ALLCOREDEVS & DEPLOYMENT UPDATES (2026-02-07 Evening)

### EIP-8105: Universal Enshrined Encrypted Mempool — Hegotá Headliner Candidate
- **Eth Magicians**: https://ethereum-magicians.org/t/hegota-headliner-proposal-eip-8105-universal-enshrined-encrypted-mempool-eem/27448
- **Presenter**: Jannik Luhn (Shutter Network)
- **Jan 29 ACD**: Formal presentation as Hegotá headliner
- **Quote**: "it relies on trusted parties, which is bad for decentralisation and censorship resistance"
- **Status**: Positioned as complementary to FOCIL

### EIP-8141: Frame Transactions (Post-Quantum AA)
- **Eth Magicians**: https://ethereum-magicians.org/t/eip-8141-frame-transaction/27617
- **Presenter**: Felix Lange (EF)
- **Vitalik endorsement**: "From a use cases perspective, this does basically satisfy everything... the entire list of goals of account abstraction"
- **Key innovation**: Unlinks transactions from fixed signature schemes (ECDSA)
- **Relevance**: Post-quantum signatures for encrypted mempool transactions

### Uniswap CCA: Multi-Chain Deployment
- **Base deployment**: Jan 22, 2026 (permissionless, no approvals needed)
- **Web app UI**: Feb 2, 2026 (auction discovery + bidding)
- **Arbitrum**: Also deploying (Jan 2026 reports)
- **Key docs**: https://support.uniswap.org/hc/en-us/articles/43107626487437-What-are-Continuous-Clearing-Auctions

### Consensys Acquires MEV Blocker
- **Date**: Jan 26, 2026
- **Source**: https://www.cryptotimes.io/2026/01/27/consensys-expands-mev-stack-with-mev-blocker-acquisition/
- **Stats**: 4.5M+ unique wallets, ~6,177 ETH rebates distributed
- **Significance**: Consolidation in MEV protection space

### NIST MPTS 2026 Workshop
- **URL**: https://csrc.nist.gov/events/2026/mpts2026
- **Date**: March 10-11, 2026
- **Topics**: Threshold schemes, MPC, ZKP, FHE, threshold-friendly primitives
- **Relevance**: Standards-track discussion for threshold encryption

### Anoma Intent Architecture
- **URL**: https://www.chaincatcher.com/en/article/2241000
- **Key innovation**: Users sign "intents" not transactions
- **Encryption**: Intents encrypted until execution conditions met
- **MEV mitigation**: Conditions-based execution, not ordering-based

### Brevis ProverNet
- **URL**: https://www.weex.com/news/detail/brevis-is-releasing-the-provernet-whitepaper...
- **Contribution**: Decentralized ZK proof generation marketplace
- **Relevance**: Could provide proving infrastructure for our ZK clearing layer

---

## Update Log
- [2026-02-04] Initial collection (7 papers)
- [2026-02-04] Found Paradigm Leaderless Auctions
- [2026-02-04] **Comprehensive sweep**: Added threshold encryption (3), encrypted mempools (3), Penumbra, traditional finance, implementation refs
- [2026-02-04] Total: 25+ sources catalogued
- [2026-02-07] **MAJOR UPDATE**: Found BEAST-MEV (ePrint 2025/1419) — our "Silent Batch Auction" concept already implemented!
- [2026-02-07] Added Weighted BTE, Silent Threshold Crypto (Waters & Wu), accountability primitives
- [2026-02-07] Identified remaining contribution space: Uniform clearing + execution
- [2026-02-07] Total: 35+ sources catalogued
- [2026-02-07] **PM UPDATE**: Major ecosystem developments!
  - EIP-8105: Native encrypted mempool proposed for Hegotá
  - TrX: Production-ready encrypted mempool in BFT (27ms overhead)
  - Uniswap CCA: Uniform clearing in production!
  - Jump DFBA: Maker/taker flow separation
  - a16z limits paper: Must-address counterarguments
  - Total: 45+ sources catalogued
- [2026-02-07] **EVENING UPDATE**: AllCoreDevs & deployment tracking
  - EIP-8105 formally presented as Hegotá headliner (Jan 29 ACD)
  - EIP-8141 Frame Transactions (post-quantum AA) — Vitalik endorsed
  - Uniswap CCA deployed to Base (permissionless, Jan 22)
  - Uniswap web app auction UI live (Feb 2)
  - Consensys acquired MEV Blocker from CoW (Jan 26)
  - NIST MPTS 2026 workshop on threshold crypto (March 10-11)
  - Total: 50+ sources catalogued
- [2026-02-07] **CRON PM UPDATE**: Daily automated research
  - RNBW CCA auction completed ($0.10→$0.13 clearing)
  - Chainlink acquired Atlas, Consensys/SMG acquired MEV Blocker
  - New ePrint papers on post-quantum threshold crypto
  - Total: 58+ sources catalogued

---

## ⭐⭐⭐⭐⭐⭐⭐⭐ SATURDAY 5PM CRON UPDATE (2026-02-07)

### NEW: Arcium Mainnet Alpha on Solana (Feb 2, 2026)
- **Substack**: https://arcium.substack.com/p/arcium-mainnet-alpha-is-live
- **Messari**: https://messari.io/report/arcium-mainnet-alpha-release
- **Key contribution**: First production MPC-based encrypted computation on Solana mainnet
- **Features**:
  - Trustless computation over fully encrypted data
  - 3,000+ distributed nodes on testnet
  - Developing C-SPL (Confidential SPL) token standard
  - First app: **Umbra Private Mainnet** (anonymous transfers, swaps)
- **Architecture**: MPC-based (not threshold encryption)
- **Status**: Mainnet Alpha (permissioned), moving toward decentralization
- **Relevance**: Alternative encrypted execution layer for Solana; validates market demand

### NEW: Fhenix Decomposable BFV (DBFV) (Feb 6, 2026)
- **Source**: Business Insider, TheStreet (press release)
- **Key contribution**: Major FHE breakthrough — solves scaling problem for large integers
- **Innovation**:
  - Decomposes large plaintexts into smaller "limbs" during encryption
  - Dramatically improves noise management
  - Enables sustained encrypted workloads without excessive bootstrapping
  - Makes FHE viable for DeFi and financial logic
- **Status**: Research completed; integration planned for later 2026
- **Relevance**: FHE could eventually replace threshold encryption; watch for EVM integration

### NEW: Uniswap CCA v1.1.0 Audits (Jan 2026)
- **GitHub**: https://github.com/Uniswap/continuous-clearing-auction
- **Audits**:
  - OpenZeppelin (Jan 23, 2026)
  - Spearbit (Jan 22, 2026)
- **Key facts**:
  - MIT licensed (can study/extend)
  - Canonical addresses across EVM chains
  - Bug bounty via Cantina
  - Factory: 0xCCccCcCAE7503Cac057829BF2811De42E16e0bD5
- **Relevance**: Production-ready uniform clearing; must study implementation

### NEW: ePrint 2026/170 — gcVM: MPC via Garbled Circuits
- **URL**: https://eprint.iacr.org/2026/170
- **Key contribution**: Publicly auditable MPC for EVM-compatible computation
- **Performance**: 83 cTPS current, ~500 cTPS projected
- **Mechanism**: Garbled circuits for confidential transaction execution
- **Relevance**: Alternative to threshold encryption for private computation

### NEW: arXiv 2302.01177 — "The Case of FBA as a DEX Processing Model"
- **URL**: https://arxiv.org/abs/2302.01177
- **Key contribution**: Formal welfare analysis of FBA vs continuous matching
- **Finding**: FBA reduces welfare loss from MEV in DEX order books
- **Mechanism**: Discrete batch auctions with uniform price
- **Relevance**: Academic validation of our core thesis

### NEW: arXiv 2408.12225 — "Fair Combinatorial Auction for Blockchain Trade Intents"
- **URL**: https://arxiv.org/abs/2408.12225
- **Key contribution**: Novel fairness definition for combinatorial batch auctions
- **Context**: Analyzes CoW Protocol-style intent-based trading
- **Finding**: Compares batch auctions vs simultaneous individual auctions
- **Relevance**: Fairness definitions applicable to our clearing layer

---

## ⭐⭐⭐⭐⭐⭐⭐ SATURDAY EVENING CRON UPDATE (2026-02-07 4:00 PM)

### NEW: Implementable Witness Encryption (ePrint 2026/175, Feb 2026)
- **URL**: https://eprint.iacr.org/2026/175
- **Authors**: Soukhanov, Rebenko, El Gebali, Komarov ([[alloc] init])
- **Key contribution**: Practical witness encryption for SNARK verification
- **Mechanism**: Modified Affine Determinant Program framework for arithmetic circuits
- **Relevance**: Alternative to threshold encryption — encrypt to proof of inclusion!
- **Potential**: "Encrypt order until it's included in a valid batch proof"
- **Gap for us**: Explore WE as alternative to threshold for encrypted orders

### NEW: Bitcoin PIPEs v2 (ePrint 2026/186, Feb 2026)
- **URL**: https://eprint.iacr.org/2026/186
- **Key contribution**: Programmable covenants on Bitcoin via witness encryption
- **Properties**: No soft forks, no trusted parties, no interactive fraud proofs
- **Mechanism**: WE + digital signatures → SNARK-verifiable conditions
- **Relevance**: Shows WE is becoming practical for blockchain applications
- **Gap for us**: Cross-pollination of WE ideas to encrypted mempools

### NEW: NIST MPTS 2026 Workshop (Jan 26-29, 2026 — COMPLETED)
- **URL**: https://csrc.nist.gov/events/2026/mpts2026
- **Status**: Already happened! (Not March as previously noted)
- **Content**: 45 talks on threshold cryptography, 25 preview talks
- **Format**: Virtual, free attendance via ZoomGov
- **Action needed**: Find recordings/proceedings for standardization insights

### NEW: a16z "17 Things for 2026" (Feb 6, 2026)
- **URL**: https://a16zcrypto.com/posts/article/big-ideas-things-excited-about-crypto-2026/
- **Key insights**:
  - **SNARKs going mainstream**: "1,000,000× overhead" dropping rapidly, becoming practical outside blockchain
  - **KYA (Know Your Agent)**: Critical primitive for agent economy; non-human identities 96:1 vs humans in finserv
  - **Stablecoins**: $46T transaction volume (20× PayPal, 3× Visa)
  - **x402 protocol**: Agent-to-agent payments, programmable settlement
  - **Wealth management democratization**: On-chain portfolio management for all
- **Relevance**: Framing of SNARK efficiency aligns with our ZK clearing direction

### NEW: CryptoAPIs Glamsterdam Deep-Dive (Feb 5, 2026)
- **URL**: https://cryptoapis.io/blog/553-ethereum-glamsterdam-upgrade
- **Key timeline**:
  - Q1 2026: Devnet testing (bals-devnet-2, epbs-devnet-0)
  - Late Q1 2026: Scope freeze (end of February)
  - H1 2026: Mainnet activation (May/June 2026)
- **Key features**:
  - **ePBS (EIP-7732)**: Enshrined proposer-builder separation, removes relay trust
  - **BALs (EIP-7928)**: Block-level access lists for parallel execution
  - **FOCIL**: Fork-choice enforced inclusion lists (may slip to Hegotá)
- **Implications for us**:
  - ePBS removes relay centralization bottleneck
  - BALs enable parallel clearing (non-conflicting batches)
  - Parallel execution = potential 3× throughput

### Updated Competitive Analysis (Feb 2026)

| Project | Focus | Status | Our Integration |
|---------|-------|--------|-----------------|
| EIP-8105 | L1 encrypted mempool | Hegotá headliner | Build on top |
| BEAST-MEV | Threshold + batch | Academic | Reference impl |
| Uniswap CCA | Token launch clearing | Production (Base) | Study & extend |
| Jump DFBA | Flow separation | Design | Incorporate |
| Shutter | Keyper network | Production (Gnosis) | Out-of-protocol |
| Witness Encryption | Alt to threshold | Emerging (2026/175) | Explore |

---

## ⭐⭐⭐⭐⭐⭐⭐ SATURDAY CRON UPDATE (2026-02-07 3:00 PM)

### NEW: Mempool Auditing Limitations (arXiv 2601.14996, Jan 2026)
- **URL**: https://arxiv.org/html/2601.14996v1
- **Authors**: Jannik Albrecht, Ghassan Karame (Runtime Verification)
- **Key contribution**: First rigorous analysis of mempool-based transaction auditing
- **Critical findings**:
  - 25%+ false positive rate for censorship detection
  - 30-second threshold for reliable transaction ordering
  - Batch-fair ordering schemes can only guarantee fairness for limited subset
- **Quote**: "mempool auditing can mislabel honest miners as 'malicious' with probability > 25%"
- **Relevance**: Validates need for batch auctions over ordering-based fairness
- **Our insight**: Ordering-based fairness is fundamentally limited → uniform clearing is essential

### NEW: Glamsterdam Deep Dive (CryptoAPIs, Feb 2026)
- **URL**: https://cryptoapis.io/blog/553-ethereum-glamsterdam-upgrade
- **Key details confirmed**:
  - **EIP-7732**: Enshrined Proposer-Builder Separation (ePBS)
  - **EIP-7928**: Block-Level Access Lists (BALs) for parallel execution
  - **Gas limit**: 60M → 200M (3× increase)
  - **Timeline**: May/June 2026 mainnet
  - **Devnets**: bals-devnet-2, epbs-devnet-0 active in Q1 2026
  - **Scope freeze**: End of February 2026
- **Relevance**: ePBS removes relay trust, BALs enable higher L1 throughput

### NEW: Hegota Headliner Competition Intensifies
- **Source**: DL News, Phemex News (Feb 2-3, 2026)
- **Leading candidates**:
  1. **FOCIL** (Fork-Choice Inclusion Lists) — gaining consensus as #1 headliner
  2. **EIP-8105** (Encrypted Mempool) — Jannik Luhn (Shutter) championing
  3. **EIP-8141** (Frame Transactions) — Vitalik personally endorsed
- **Key dynamics**:
  - FOCIL + EIP-8105 positioned as "complementary" (censorship + MEV)
  - EIP-8141 competes for headliner slot but focused on post-quantum
  - Vitalik quote on EIP-8141: "entire list of goals of account abstraction"
- **Our strategic position**: Layer 2 clearing works with any winning combination

### NEW: VibeSwap Proposal (Nervos, Feb 2026)
- **URL**: https://talk.nervos.org/t/vibe-swap-a-new-decentralized-exchange-giving-fair-price-discovery-as-a-human-right/9897
- **Chain**: Nervos Network (CKB)
- **Tagline**: "Fair price discovery as a human right"
- **Mechanism**: MEV-resistant batch auction on UTXO-based chain
- **Relevance**: Shows MEV-resistant DEX interest beyond EVM; validates problem space

---

## ⭐⭐⭐⭐⭐⭐ DAILY UPDATE (2026-02-07 Evening, Cron Run)

### New ePrint Papers (2026)

#### IND-CCA Lattice Threshold KEM under 30 KiB (ePrint 2026/021)
- **URL**: https://eprint.iacr.org/2026/021
- **Authors**: Boudgoust, Lapiha, del Pino, Prest (Royal Holloway, PQShield)
- **Key contribution**: Post-quantum threshold KEM with 18× smaller ciphertexts
- **Stats**: 30 KiB ciphertext (vs 540 KiB prior), T=32 threshold, 128-bit security
- **Relevance**: Post-quantum threshold encryption for future-proof encrypted mempools
- **Gap**: Applied to KEM, not mempool; could inspire post-quantum BEAST-MEV

#### Threshold FHE with Synchronized Decryptors (ePrint 2026/031)
- **URL**: https://eprint.iacr.org/2026/031
- **Authors**: Colin de Verdière, Passelègue, Stehlé (CryptoLab)
- **Key contribution**: First proper security model for synchronized ThFHE
- **CRITICAL**: **Finds key-recovery attacks against Mouchet et al. (2023, 2024)**!
- **Proposed fix**: Masking partial decryption shares with PRFs
- **Relevance**: Security of threshold FHE schemes — applicable to encrypted computation

#### Three-Round Robust Threshold ECDSA (ePrint 2026/190)
- **URL**: https://eprint.iacr.org/2026/190
- **Authors**: Jiang, Tang, Xue
- **Key contribution**: Robust threshold ECDSA from CL encryption
- **Relevance**: Threshold signatures for validator committee coordination

#### Hardware-Friendly Robust Threshold ECDSA (ePrint 2026/094)
- **URL**: https://eprint.iacr.org/2026/094
- **Key contribution**: ART-ECDSA for asymmetric settings (hardware wallets)
- **Relevance**: Could enable hardware-secured Keyper nodes

### Production Developments

#### Rainbow RNBW CCA Auction Completed (Feb 3-5, 2026)
- **Source**: Multiple (Phemex, Bitrue, Longbridge)
- **Mechanism**: First major token launch using CCA post-web-app-launch
- **Timeline**: Pre-bid Feb 2 → Auction Feb 3 → Clearing Feb 5
- **Clearing Price**: **$0.13** (started at $0.10) — 30% price discovery
- **FDV at clearing**: ~$130 million
- **Significance**: Live production validation of uniform clearing price mechanism
- **Platform**: Base chain via Uniswap v4

#### Chainlink Acquires Atlas (Jan 22, 2026)
- **Source**: PRNewswire, The Block, multiple crypto news
- **Acquired from**: FastLane Labs
- **Product**: Transaction-ordering and order-flow auction protocol
- **Integration**: Now exclusively supports Chainlink SVR (Smart Value Recapture)
- **Live on**: Arbitrum, Base, BNB Chain, Ethereum, HyperEVM
- **Strategy**: OEV (Oracle Extractable Value) capture and redistribution
- **Relevance**: Chainlink positioning as MEV infrastructure layer

#### Consensys/SMG Acquires MEV Blocker (Jan 26, 2026)
- **Source**: CoW DAO announcement, Consensys
- **Acquirer**: Special Mechanisms Group (SMG), Consensys subsidiary
- **Stats**: 4.5M+ unique users, 6,177 ETH in rebates returned
- **Model**: Backrunning auction infrastructure
- **Significance**: Consolidation in MEV protection space; CoW focusing on protocol
- **Relevance**: Shift from DAO-operated to corporate-operated MEV protection

### Ethereum Upgrade Timeline Updates

#### Glamsterdam Status
- **bals-devnet-2**: Launched Feb 4, 2026
- **Target**: H1 2026 mainnet
- **Key features**: enshrined Proposer-Builder Separation (ePBS)
- **Status**: On track despite earlier Fusaka issues

#### Hegotá Status
- **Headliner deadline**: Feb 4, 2026 (passed)
- **Leading candidates**:
  1. FOCIL (Fork-Choice Inclusion Lists) — consensus building
  2. EIP-8105 (Encrypted Mempool) — Shutter Network's proposal
  3. EIP-8141 (Frame Transactions) — Vitalik-endorsed post-quantum AA
- **Expected timeline**: Following Glamsterdam (likely late 2026 or 2027)

### Emerging Competitors

#### Shade Network Testnet (Jan 19, 2026)
- **Source**: Airdrops.io
- **Features**: Private transactions, encrypted mempool, private contracts
- **Status**: Testnet live
- **Relevance**: New entrant in encrypted execution space

---

## Updated Source Count: 80+ sources catalogued

### Sources Added This Cycle (Feb 7 PM)
1. arXiv 2601.14996 — Mempool auditing effectiveness (Albrecht, Karame)
2. CryptoAPIs Glamsterdam deep-dive
3. DL News Hegota headliner coverage
4. Phemex Hegota features summary
5. VibeSwap Nervos proposal

### Sources Added This Cycle (Feb 7 Evening — 4PM Cron)
1. ePrint 2026/175 — Implementable Witness Encryption (Soukhanov et al.)
2. ePrint 2026/186 — Bitcoin PIPEs v2 (WE for covenants)
3. NIST MPTS 2026 Workshop — Proceedings (Jan 26-29, completed)
4. a16z "17 Things for 2026" — SNARKs, KYA, stablecoins
5. CryptoAPIs Glamsterdam timeline update (scope freeze, mainnet target)
6. Multiple Hegota headliner news updates (Feb 3-5)

### Sources Added This Cycle (Feb 7 — 5PM Cron)
1. **Arcium Mainnet Alpha** (Feb 2, 2026) — MPC-based encrypted computation on Solana
2. **Fhenix Decomposable BFV** (Feb 6, 2026) — FHE breakthrough for blockchain
3. **Uniswap CCA v1.1.0** — Audited by OpenZeppelin (Jan 23) & Spearbit (Jan 22)
4. **ePrint 2026/170** — gcVM: MPC via garbled circuits (~500 cTPS)
5. **arXiv 2302.01177** — "The Case of FBA as a DEX Processing Model" (formal welfare analysis)
6. **arXiv 2408.12225** — "Fair Combinatorial Auction for Blockchain Trade Intents"
7. Uniswap CCA whitepaper fetched (docs.uniswap.org/whitepaper_cca.pdf)
8. Uniswap CCA GitHub repo (open source, MIT licensed)

### Sources Added This Cycle (Feb 7 — 6PM Cron)
1. **Vitalik L2 Paradigm Shift** (Feb 3, 2026) — "Rollup-centric roadmap no longer makes sense"
   - L2 usage dropped 50%: 58.4M → 30M addresses
   - Ethereum L1 users doubled: 7M → 15M
   - Proposed native rollup precompile for ZK-EVM verification
   - Sources: CoinDesk, DL News, Decrypt, BeInCrypto
2. **Ethereum Foundation Trillion Dollar Security Dashboard** (Feb 5-6, 2026)
   - Six security dimensions: UX, smart contracts, infrastructure, consensus, monitoring, social governance
   - Part of "1TS" (Trillion Dollar Security) initiative from May 2025
   - URL: https://security.ethereum.org (implied from coverage)
3. **ePrint 2026/189** — Shared and leakage free MAYO (threshold signatures)
   - Post-quantum threshold signature scheme
   - t-of-n threshold MAYO signatures
4. **ePrint 2026/192** — Verification Theater (Feb 2026)
   - Critical analysis of formal verification claims in crypto libraries
   - Case study: Cryspen's libcrux and hpke-rs
   - Warning: Marketing claims may exceed actual verification scope
5. **Glamsterdam Timeline Confirmed** (CryptoAPIs Feb 5, 2026)
   - Scope freeze: End of February 2026
   - Mainnet: May/June 2026
   - Key EIPs: 7732 (ePBS), 7928 (BALs)
   - Gas limit: 60M → 200M (3× increase)
