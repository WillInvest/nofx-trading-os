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
