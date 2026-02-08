# Literature Index — On-Chain Trustless FBA

**Last Updated**: 2026-02-08 (125+ sources catalogued)

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

### ⭐ FairTraDEX: DEX Preventing Value Extraction (McMenamin et al., 2022)
- **ArXiv**: https://arxiv.org/abs/2202.06384
- **Key contribution**: First FBA-based DEX with formal game-theoretic guarantees
- **Mechanism**:
  - ZK set-membership proofs for bid privacy
  - Escrow-enforced commit-reveal protocol
  - Handles monopolistic/malicious liquidity providers
- **Key result**: Fixed-fee model independent of order size (first guarantee of its kind)
- **Implementation**: Detailed Solidity code provided
- **Relevance**: Foundational academic work validating our approach

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

### ⭐⭐ The High-Frequency Trading Arms Race: Frequent Batch Auctions (Budish, Cramton, Shim, 2015)
- **SSRN**: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2388265
- **Published**: The Quarterly Journal of Economics, Vol. 130, Issue 4 (Nov 2015)
- **PDF**: https://conference.nber.org/confer/2013/MDf13/Budish_Cramton_Shim.pdf
- **Key contribution**: **FOUNDATIONAL PAPER** for uniform-price batch auctions as MEV mitigation
- **Core argument**: Financial exchanges should use frequent batch auctions (uniform price double auctions, e.g., every 100ms) instead of continuous limit order books
- **Key insight**: Converts competition on speed → competition on price
- **Benefits proven**: Eliminates latency arbitrage, enhances liquidity, simplifies market computationally
- **Authors**: Eric Budish (Chicago Booth), Peter Cramton (Maryland), John Shim
- **Citations**: 1000+ — highly influential in market design literature
- **Relevance**: Theoretical foundation for all blockchain batch auction research including Uniswap CCA

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
- [2026-02-08] **SATURDAY NIGHT CRON UPDATE**:
  - Added Budish-Cramton-Shim (2015) — foundational batch auction paper
  - Uniswap CCA technical documentation added
  - ePrint 2026 index scanned — no major new papers today
  - Total: 100+ sources catalogued

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

### NEW: Uniswap CCA v1.1.0 (Production, Jan 2026)
- **GitHub**: https://github.com/Uniswap/continuous-clearing-auction
- **Docs**: https://docs.uniswap.org/contracts/liquidity-launchpad/CCA
- **Whitepaper**: https://docs.uniswap.org/whitepaper_cca.pdf (Hayden Adams, Nov 2025)
- **Audits**:
  - OpenZeppelin (Jan 23, 2026)
  - Spearbit (Jan 22, 2026) + additional
  - ABDK Consulting
- **Key facts**:
  - MIT licensed (can study/extend)
  - Canonical addresses across EVM chains
  - Factory: 0xCCccCcCAE7503Cac057829BF2811De42E16e0bD5
  - Bug bounty via Cantina
- **Technical**:
  - Uses Foundry for build/test
  - BTT unit tests + fuzz + invariant tests
  - Pairs with Uniswap Liquidity Launcher
- **Mechanism**: Uniform-price auction generalized to continuous time
  - Tokens released per block (configurable schedule)
  - Clearing price = price where all supply sells to active bids
  - Bids have max price → removed when clearing exceeds max
  - Early bidders get better exposure to lower prices
- **Relevance**: **CRITICAL** — Production uniform clearing implementation to study

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

## Updated Source Count: 110+ sources catalogued

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

---

## ⭐⭐⭐⭐⭐⭐⭐⭐ SATURDAY 7PM CRON UPDATE (2026-02-07)

### NEW: Collaborative Traceable Secret Sharing (ePrint 2026/181, Feb 2026)
- **URL**: https://eprint.iacr.org/2026/181
- **Authors**: Pousali Dey, Rittwik Hajra, Subha Kar, Soumit Pal (Indian Statistical Institute)
- **Key contribution**: Public tracing for secret sharing WITHOUT designated tracer
- **Mechanism**:
  - Eliminates private trace keys and private verification keys
  - Tracing requires collaboration from threshold parties
  - Verification is FULLY PUBLIC
  - Based on Shamir and Blakley schemes
- **Properties**: Secrecy, traceability, non-imputability
- **Minimal share size overhead, polynomial-time tracing**
- **Builds on**: Goyal-Song-Srinivasan (CRYPTO'21), Boneh-Partap-Rotem (CRYPTO'24)
- **Relevance**: **CRITICAL for accountability in encrypted mempools!**
  - Could enable public verification of Keyper misbehavior
  - No designated authority needed for tracing
  - Aligns with decentralization goals

### NEW: Accountable UC Asynchronous Secure Distributed Computing (ePrint 2026/182, Feb 2026)
- **URL**: https://eprint.iacr.org/2026/182
- **Authors**: Civit, Collins (NYU), Gramoli (Sydney/Redbelly), Guerraoui (EPFL), Komatovic (Category Labs), Vidigueira (Chainlink Labs), Zarbafian (Amaroo)
- **Key contribution**: Universal compiler for accountability in distributed protocols
- **Mechanism**: τ_{zk-scr} compiler transforms any semi-honest crash-failure protocol into Byzantine-tolerant accountable counterpart
- **Guarantees**:
  - Preserves privacy, input-independence, correctness, output delivery for f ≤ t_ε
  - If f > t_ε: either (1) hypersafety preserved, or (2) all correct processes get verifiable proofs of misbehavior
  - Externally verifiable proofs involving significant subset of faulty parties
- **Formalized**: Using Accountable Universal Composability (AUC) framework (S&P 2023)
- **Relevance**: **EXTREMELY relevant for our clearing layer!**
  - Could apply τ_{zk-scr} to batch clearing protocols
  - Provides formal accountability guarantees we need
  - Authors include Chainlink Labs (potential collaboration)

### NEW: MPC Benchmarking Framework (ePrint 2026/183, Feb 2026)
- **URL**: https://eprint.iacr.org/2026/183
- **Authors**: Harth-Kitzerow, Schiller, Schwanke, Prantl, Carle (Würzburg, TUM)
- **Key contribution**: First systematic cross-framework MPC evaluation
- **Frameworks tested**: HPMPC, MPyC, MP-SPDZ, MOTION
- **Evaluation**: Varying bandwidth, latency, packet loss, input sizes
- **Value**: Evidence-based framework selection guidance
- **Relevance**: Useful for evaluating MPC alternatives to threshold encryption

### NEW: Flow Network MEV Resistance Milestone (Feb 5, 2026)
- **Source**: GlobeNewswire press release
- **Stats**: 40 million unique users, 950 million transactions
- **MEV Features Claimed**:
  - Native MEV Resistance
  - Native VRF (verifiable randomness)
  - Scheduled Transactions
  - "Actions" for automated execution
- **Context**: Dapper Labs chain (NBA Top Shot, NFL ALL DAY, Disney Pinnacle)
- **Architecture**: Not threshold-based; appears to use VRF + scheduling
- **Relevance**: Alternative approach to MEV resistance; worth studying mechanism
- **Gap**: Not EVM-compatible, proprietary approach

### UPDATE: Vitalik's L2 Critique Continues to Reverberate (Feb 3-6, 2026)
- **Sources**: CoinDesk, Yahoo Finance, Bankless, Unchained Crypto
- **Key quote**: "make yet another EVM chain and add an optimistic bridge... is to infra what forking Compound is to governance"
- **L2 response**:
  - Base (Jesse Pollak): "L2s can't just be 'Ethereum but cheaper'"
  - Polygon (Marc Boiron): "Scaling alone is insufficient"
  - Unchained: Framing shift from "branded shards" to "sovereign systems"
- **Strategic implication**: Reinforces our L1-first deployment strategy
- **Our opportunity**: Uniform clearing layer provides differentiation L2s now need

### UPDATE: Glamsterdam Scope Freeze Imminent
- **Deadline**: End of February 2026
- **Source**: Multiple (CryptoAPIs, Motley Fool, ad-hoc-news.de)
- **Final feature list** being determined NOW
- **Our window**: ~3 weeks to influence or contribute to discussion

---

## Updated Source Count: 95+ sources catalogued

### Sources Added This Cycle (Feb 7 — 7PM Cron)
1. **ePrint 2026/181** — Collaborative Traceable Secret Sharing (public tracing!)
2. **ePrint 2026/182** — Accountable UC Async Secure Distributed Computing (Chainlink Labs co-author)
3. **ePrint 2026/183** — MPC Benchmarking Framework (HPMPC, MPyC, MP-SPDZ, MOTION)
4. **Flow Network** — 40M users milestone, native MEV resistance claims
5. **Vitalik L2 follow-up** — "copypasta L2 chains" critique (Feb 5 CoinDesk)
6. **L2 ecosystem response** — Base, Polygon reactions to Vitalik's comments

---

## ⭐⭐⭐⭐⭐⭐⭐⭐⭐ SATURDAY 8PM CRON UPDATE (2026-02-07)

### NEW: ERC-8004 — Trustless Agent Standard (Mainnet Jan 29, 2026)
- **Bitget News**: https://www.bitget.com/news/detail/12560605183395
- **Biometric Update**: https://www.biometricupdate.com/202602/no-trust-required-with-8004-a-new-ethereum-protocol-for-trustless-agents
- **Bankless Podcast**: https://www.bankless.com/podcast/ai-on-ethereum-erc-8004-x402
- **Key contribution**: On-chain registry for AI agent identity, capabilities, and reputation
- **Collaborators**: Ethereum Foundation dAI Team, MetaMask, Google, Coinbase
- **Architecture**:
  - Identity Registry: Agent names, skills, endpoints
  - Reputation Registry: On-chain performance history
  - Discovery: Agents can find and interact trustlessly
- **Adoption**: Base (first L2), BNB Chain, Polygon already deployed
- **Pairs with**: x402 protocol for agent-to-agent payments
- **Critical for us**: Native infrastructure for agent-signed orders in DEX!

### NEW: EIP-8105 vs EIP-8141 Hegota Competition
- **DL News**: https://www.dlnews.com/articles/defi/ethereum-devs-begin-debate-over-hegota-upgrade/
- **BitcoinEthereumNews**: https://bitcoinethereumnews.com/ethereum/ethereum-eyes-frame-transactions-as-hegota-headliner/
- **Key dynamics**:
  - EIP-8105 (Shutter/Luhn): Encrypted mempool for MEV protection
  - EIP-8141 (Frame Tx): Post-quantum + account abstraction
  - FOCIL: Censorship resistance (consensus building)
  - All competing for headliner slot
- **Jannik Luhn quote**: "relies on trusted parties, which is bad for decentralisation"
- **Vitalik on EIP-8141**: "satisfies entire list of goals of account abstraction"
- **Implication**: L1 encrypted mempool increasingly likely, but encryption-agnostic design needed

### NEW: Glamsterdam Scope Freeze Confirmed
- **CryptoAPIs**: https://cryptoapis.io/blog/553-ethereum-glamsterdam-upgrade
- **Timeline Confirmed**:
  - Scope freeze: End of February 2026 (~3 weeks)
  - Mainnet target: H1 2026 (May/June)
  - bals-devnet-2 launched Feb 4
- **Key EIPs**:
  - EIP-7732 (ePBS): Enshrined Proposer-Builder Separation
  - EIP-7928 (BALs): Block-Level Access Lists for parallel execution
- **Gas limit**: 60M → 200M (3× increase!)
- **Implication**: L1 clearing more viable with higher gas limit + ePBS

### NEW: Uniswap CCA Web App Live
- **CryptoAdventure**: https://cryptoadventure.com/uniswap-web-adds-continuous-clearing-auctions-what-cca-changes-for-routing-and-liquidity/
- **Phemex**: https://phemex.com/news/article/uniswap-launches-auction-feature-on-web-app-57600
- **Launched**: February 2, 2026
- **Features**:
  - Discover, bid, and claim tokens in web interface
  - Powered by CCA contracts on Base
  - Continuous price discovery with gradual supply release
- **First use case**: Token launches (RNBW auction completed)

### NEW: arXiv 2602.01392 — Electricity Market Clearing Mechanisms
- **URL**: https://arxiv.org/html/2602.01392
- **Key contribution**: Reinforcement learning evaluation of uniform vs pay-as-bid clearing
- **Finding**: Uniform price mechanism values all accepted offers at System Marginal Price
- **Relevance**: Methodological insights for evaluating clearing mechanism efficiency

### UPDATE: ePrint 2026/192 — Verification Theater
- **URL**: https://eprint.iacr.org/2026/192
- **Authors**: Nadim Kobeissi
- **Key finding**: Five vulnerabilities in "formally verified" libcrux and hpke-rs
- **Vulnerabilities found**:
  1. Platform-dependent SHA-3 failure
  2. Missing X25519 DH output validation
  3. Nonce reuse via integer overflow
  4. ECDSA signature malleability
  5. Ed25519 entropy reduction
- **Critical insight**: "Verification boundary problem" — formal methods cover limited scope
- **Implication**: Multi-layer security essential, formal verification insufficient alone

### UPDATE: ePrint 2026/190 — Three-Round Threshold ECDSA
- **URL**: https://eprint.iacr.org/2026/190
- **Authors**: Jiang, Tang, Xue
- **Key contribution**: First 3-round threshold ECDSA with O(1) outgoing communication
- **Comparison**: Wong et al. (NDSS24) required 4 rounds
- **Relevance**: Efficient committee coordination for encrypted mempool key management

### Sources Added This Cycle (Feb 7 — 8PM Cron)
1. **ERC-8004** — Trustless Agent Standard (mainnet Jan 29, 2026)
2. **Bankless podcast** — ERC-8004 + x402 deep dive (Feb 4)
3. **DL News Hegota coverage** — EIP competition dynamics
4. **arXiv 2602.01392** — Electricity market clearing via RL
5. **Glamsterdam scope freeze confirmation** — End of February
6. **Uniswap CCA web app launch** — February 2, 2026
7. **Multiple L2 response articles** — Base, Polygon on Vitalik's critique

### Sources Added This Cycle (Feb 8 — 9PM Cron)
1. **Budish-Cramton-Shim (2015)** — "Frequent Batch Auctions" QJE paper (FOUNDATIONAL)
2. **Uniswap CCA whitepaper** — Hayden Adams, Nov 2025
3. **Uniswap CCA technical docs** — Full mechanism specification
4. **ePrint 2026 index scan** — Confirmed no major new threshold/MEV papers today
5. **Hegota competition updates** — Frame Tx vs EIP-8105 positioning

### Sources Added This Cycle (Feb 7 — 11PM Cron)
1. **EF Checkpoint #8 Blog Post** (Jan 20, 2026) — Official Glamsterdam/Hegotá timeline
   - FOCIL moved to Hegotá, competing with EIP-8105 for headliner
   - Headliner decision: Feb 26; scope freeze: end of Feb
   - URL: https://blog.ethereum.org/en/2026/01/20/checkpoint-8

### Sources Added This Cycle (Feb 8 — 3AM Cron)
1. **GraphTally** — The Graph's micropayment batching (live since late 2024)
   - Cryptographically signed vouchers, settled in batches
   - Enables sub-cent payments without per-tx gas
   - Critical for x402/ERC-8004 agent economy viability
2. **The Graph ERC-8004 Subgraphs** — 8 blockchain coverage (with Agent0)
   - Cross-chain agent reputation queries via single lookup
   - Base, Arbitrum, Polygon, etc.

### Sources Added This Cycle (Feb 8 — 10PM Cron)
1. **ERC-8004 adoption news** — 24k+ agents registered (CryptoRank, Bitget)
2. **The Graph + ERC-8004/x402** — Major indexing infrastructure support (BitcoinEthereumNews)
3. **MultiversX x402 integration** — Cross-chain adoption (The Block)
4. **x402 Protocol explainer** — HTTP 402 for agent payments (JoinedCrypto)
5. **BABE (ePrint 2026)** — Bitcoin proof verification 1000× cheaper via WE
6. **PQC Migration for Blockchain** — Comprehensive blockchain quantum readiness (ePrint, Dec 2025)
7. **Beyond LWE** — Lattice-based HE framework, LIP instantiation (ePrint 2026)
8. **RNBW auction final data** — $0.13 clearing confirmed, $130M FDV (HokaNews, BingX)
9. **Vitalik "Glamsterdam Ultimatum"** — L2 criticism driving L1 focus (BitcoinEthereumNews)
10. **Glamsterdam on track** — bals-devnet-2 live, scope freeze end of Feb (TronWeekly, CryptoAPIs)

---

## ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ SUNDAY 12AM CRON UPDATE (2026-02-08)

### 🚀 ERC-8004 Adoption Explosion (Past 24 Hours!)

#### NEW: Virtuals Protocol ACP Integration
- **Source**: Bitget News (Feb 7, 5 PM)
- **URL**: https://www.bitget.com/news/detail/12560605187604
- **Key**: All graduated AI agents on ACP (Agency Commerce Protocol) will be **automatically registered on ERC-8004**
- **Significance**: Major agent platform integrating → network effects accelerating
- **Implication**: Agent economy infrastructure reaching critical mass

#### NEW: Avalanche C-Chain Support
- **Source**: Bitget News (Feb 7, 5 PM)
- **URL**: https://www.bitget.com/news/detail/12560605187590
- **Key**: Avalanche now supports ERC-8004 natively
- **Features**: On-chain identity, discovery, portable reputation for AI agents
- **Chain count**: Now 5+ chains (Base, BNB, Polygon, MultiversX, Avalanche)
- **Velocity**: New chain every 2-3 days → exponential adoption

#### NEW: Davide Crapis Interview (EF dAI Team Lead)
- **Source**: CryptoBriefing / Unchained (Feb 8, 2 AM)
- **URL**: https://cryptobriefing.com/davide-crapis-erc-8004-enables-decentralized-ai-agent-interactions-establishes-trustless-commerce-and-enhances-reputation-systems-on-ethereum-unchained/
- **Key quotes**:
  - "ERC 8004 aims to build trust between agents in decentralized environments"
  - "I think that's where really the magic of 8,004 that you cannot have in a smaller like centralized service can like be realized."
- **Focus**: Trust, reputation, specialized agents providing services
- **Implication**: Vision extends beyond trading to full agent economy

### NEW ePrint Papers (Feb 6-7, 2026)

#### ePrint 2026/194 — Unified Hardware for Hash-Based Signatures
- **URL**: https://eprint.iacr.org/2026/194
- **Authors**: Zhang, Chu, Wei, Dai, Shen, Tian
- **Key contribution**: Single FPGA architecture for LMS, XMSS, and SPHINCS+
- **Efficiency**: 4.12×/10.92× lower Area-Time Product for signing
- **Relevance**: Hardware acceleration for post-quantum signatures (future Keyper nodes?)

#### ePrint 2026/193 — Atkin/Weber Modular Polynomials for Isogeny Proofs
- **URL**: https://eprint.iacr.org/2026/193
- **Authors**: den Hollander, Mula, Slamanig, Spindler
- **Key contribution**: Up to 39% sparser R1CS constraint systems using Weber polynomials
- **Relevance**: More efficient ZK proofs for cryptographic primitives

#### ePrint 2026/191 — PEARL-SCALLOP Active Attack
- **URL**: https://eprint.iacr.org/2026/191
- **Authors**: Fouotsa, Houben, Lorenzon, Rueger, Tasbihgou
- **Key contribution**: Active attack requires only 4 oracle calls to recover secret
- **Warning**: Demonstrates cryptographic schemes can have subtle vulnerabilities
- **Relevance**: Reinforces need for multi-layer security (not just cryptographic)

#### ePrint 2026/189 — Shared and Leakage-Free MAYO
- **URL**: https://eprint.iacr.org/2026/189
- **Authors**: Azevedo-Oliveira, Beraud, Varjabedian
- **Key contribution**: Threshold instantiation of UOV/MAYO post-quantum signatures
- **Methods**: Newton polynomials + Samuelson-Berkowitz for shared determinant computation
- **Relevance**: Post-quantum threshold signatures for future Keyper committees

### NIST MPTS 2026 Workshop Details (Completed Jan 26-29)
- **URL**: https://csrc.nist.gov/events/2026/mpts2026
- **Key talks identified**:
  - TECLA/THE CLASH: Two-party and threshold ECDSA from class groups
  - (Red)ETA: Refreshable extensible DLOG enhanced threshold algorithms
  - SplitForge: Two-party signing with extra features
- **Status**: Virtual via ZoomGov, recordings likely available
- **Action**: Find and review proceedings for standardization insights

### Ecosystem Status Confirmations

#### Glamsterdam Timeline (Locked)
- **Scope freeze**: End of February 2026 (~3 weeks)
- **Mainnet target**: May/June 2026 (H1)
- **EIPs confirmed**: ePBS (7732), BALs (7928)
- **Gas limit**: 60M → 200M (3× increase)

#### Hegotá Headliner Competition (Active)
- **Decision date**: February 26, 2026
- **Leading candidates**:
  1. FOCIL — gaining consensus as #1 (censorship resistance)
  2. EIP-8105 — encrypted mempool (MEV protection)
  3. EIP-8141 — Frame Transactions (post-quantum + AA)
- **Non-headliner deadline**: ~30 days after Feb 26 decision
- **Our window**: ~3 weeks to contribute/influence

---

## Updated Source Count: 120+ sources catalogued

### Sources Added This Cycle (Feb 8 — 12AM Cron)
1. **Virtuals Protocol ACP + ERC-8004** — Auto-registration for graduated agents
2. **Avalanche C-Chain ERC-8004** — New chain support, 5+ total
3. **Davide Crapis interview** — EF dAI Team lead on ERC-8004 vision
4. **ePrint 2026/194** — Unified hardware for hash-based signatures
5. **ePrint 2026/193** — Atkin/Weber modular polynomials (39% improvement)
6. **ePrint 2026/191** — PEARL-SCALLOP active attack (4 oracle calls!)
7. **ePrint 2026/189** — Shared/leakage-free MAYO (post-quantum threshold)
8. **NIST MPTS 2026** — Workshop talk details (TECLA, RED-ETA, SplitForge)
9. **UW Fair Ordering Thesis** — Foundational PhD thesis (2023)

### Sources Added This Cycle (Feb 8 — 1AM Cron)
1. **FairTraDEX** (arXiv 2202.06384, Aug 2022) — DEX based on FBA with formal game-theoretic guarantees
   - Uses ZK set-membership + commit-reveal
   - Fixed-fee guarantee independent of order size
   - Foundational academic work for our approach
2. **Odaily ERC-8004 Deep-Dive** (Feb 7, 2026) — Comprehensive analysis of the three registries
   - Identity Registry: ERC-721 based agent NFTs
   - Reputation Registry: Payment-linked reviews ("Yelp for AI")
   - Verification Registry: ZK/TEE endorsements for high-risk tasks
   - Goal is "universal standard for AI Agent discovery and trust"
3. **Davide Crapis interview (Unchained)** — "ERC 8004 enables decentralized AI agent interactions"
4. **ePrint 2026 scan** — No major new threshold/MEV papers today (Sunday quiet period)

### Key Synthesis Update

**ERC-8004 Adoption Velocity:**
| Date | Chains | Agents |
|------|--------|--------|
| Jan 29 | 1 (mainnet) | Launch |
| Feb 1 | 3 (Base, BNB, Polygon) | 24k+ |
| Feb 7 | 5+ (+ MultiversX, Avalanche) | Growing |

**Implication**: Agent economy infrastructure is real and accelerating. Our DEX design MUST support agent-signed orders in v1.

### Sources Added This Cycle (Feb 8 — 4AM Cron)
1. **BNB Chain ERC-8004 Deployment** (Feb 4, 2026) — Official deployment to BSC Mainnet + Testnet
   - Sources: Chainwire, Business Insider, Cryptopolitan, BanklessTimes
   - BNB Chain now supports "Trustless Agents" standard
   - Verifiable identity and on-chain reputation for autonomous agents
   - Joins Base, Polygon, MultiversX, Avalanche in ERC-8004 support
2. **ePrint 2026 scan** — No new major threshold/MEV papers (Sunday quiet period continues)
3. **Hegota competition stable** — FOCIL, EIP-8105, EIP-8141 dynamics unchanged

### Research Saturation Note (Feb 8 4AM)
All major search queries now returning known sources. Literature collection reaching maturity.
Shifting focus to:
- Implementation analysis (Uniswap CCA, BEAST-MEV code)
- Empirical data collection (RNBW auction, Base transactions)
- Design work (ZK clearing, multi-provider interface)
- Hegotá proposal preparation
