# Novel Ideas — On-Chain Trustless FBA

**Last Updated**: 2026-02-04

## Synthesized Insights from Literature

### The Core Problem
Every current solution requires trusting *someone*:
- Flashbots: Trust builders/relays
- CoW: Trust solvers
- FSS: Trust oracle network
- L2s: Trust sequencer

The blockchain's original promise was: **trust no one, verify everything**.

### Why This Is Hard
1. **Information Asymmetry**: Someone must see orders before execution
2. **Temporal Ordering**: Blockchain is sequential; someone decides order
3. **Coordination**: Batch boundaries require agreement
4. **Liveness vs Safety**: Can't have both perfect privacy AND guaranteed execution

---

## Candidate Approaches (Refined)

### Approach 1: Pure Commit-Reveal Batch Auction
**Mechanism**:
1. Users commit `hash(order || salt)` with deposit
2. After block N, reveal window opens
3. At block N+k, batch executes with all revealed orders
4. Non-revealers forfeit deposit

**Analysis**:
- ✅ Fully on-chain
- ✅ No trusted third party
- ❌ Griefing: attacker can commit many orders, not reveal, disrupt batch
- ❌ Capital inefficiency: requires deposits
- ❌ Latency: commit → reveal → execute is 3+ blocks
- ❌ Order book leakage: can infer from commitment patterns

**Improvement Ideas**:
- Batch continues with revealed orders only (graceful degradation)
- Slash deposit proportional to batch disruption
- Minimum batch size threshold

### Approach 2: Time-Lock Encrypted Batch Auction
**Mechanism**:
1. Users encrypt orders with time-lock puzzle (e.g., VDF)
2. Puzzle becomes solvable at batch execution time
3. Anyone can solve and submit the batch
4. On-chain verification that solution is correct

**Analysis**:
- ✅ No trusted party for decryption
- ✅ No griefing (encryption is forced "reveal")
- ❌ Computational cost to solve puzzles
- ❌ Who pays for solving? Miners? Users? Contract?
- ❌ VDF verification gas cost on EVM

**Improvement Ideas**:
- Batch puzzles into single aggregate puzzle
- Incentivize third parties to solve (MEV they can capture = fair)
- Use efficient VDF constructions (Wesolowski, Pietrzak)

### Approach 3: Threshold-Encrypted Batch with Rotating Committee
**Mechanism**:
1. Orders encrypted to threshold key (t-of-n decryption)
2. Committee is randomly selected each batch (VRF)
3. Committee members are staked and slashable
4. Decryption key shares released at batch time

**Analysis**:
- ✅ Distributed trust (better than single party)
- ✅ Slashing deters malicious behavior
- ⚠️ Still requires trusting t honest committee members
- ❌ Key management complexity
- ❌ Who runs committee nodes?

**Improvement Ideas**:
- Use existing validator set as committee
- Incentivize with MEV share (align incentives)
- Combine with commit-reveal as fallback

### Approach 4: On-Chain Uniform Price Clearing (Order-Irrelevant)
**Mechanism**:
1. All orders in batch execute at same clearing price
2. Price determined by supply/demand intersection
3. Order within batch doesn't matter → front-running useless

**Analysis**:
- ✅ Eliminates ordering-based MEV
- ✅ Well-understood economics (call markets)
- ❌ Doesn't hide order *contents* (still sandwich-able pre-batch)
- ❌ Price discovery on-chain is complex
- ❌ Need to combine with privacy mechanism

**Key Insight**: Uniform price is *necessary but not sufficient*. Need privacy too.

### Approach 5: Hybrid — Time-Lock + Uniform Price
**Mechanism**:
1. Orders encrypted with time-lock puzzle
2. At batch time, puzzles solved, orders revealed
3. Clearing price computed on-chain
4. All orders execute at uniform price

**Analysis**:
- ✅ Privacy until execution (time-lock)
- ✅ Order-irrelevant execution (uniform price)
- ✅ No trusted third party
- ⚠️ Gas cost of on-chain price computation
- ⚠️ Puzzle solving coordination

**This is our leading candidate.**

---

## Novel Contributions to Explore

### Idea A: "Lazy VDF" — Externalize Puzzle Solving
- Users submit encrypted orders
- Don't solve puzzles until batch is "full" or timer expires
- Let MEV searchers solve puzzles (they're incentivized)
- The MEV they can extract = payment for solving
- Creates market-based decryption timing

### Idea B: "Progressive Reveal" — Partial Information Leak
- Reveal order *type* (buy/sell) immediately
- Reveal *size* at t+1
- Reveal *price* at t+2
- Execution at t+3
- Progressively reduces information asymmetry
- May enable better price discovery

### Idea C: "Batch Futures" — Commit to Participate
- Users commit to participate in batch N
- Batch N parameters (time, minimum size) are known
- Commitment locks funds, ensures participation
- Non-participation = slashing
- Creates predictable batches without coordinator

### Idea D: "AMM as Auctioneer"
- AMM itself runs the batch auction
- Liquidity providers are implicitly the "committee"
- LP shares = voting power on batch execution
- Aligns incentives: LPs want fair execution to attract traders

---

## Open Questions

1. **What's the minimum latency achievable with full trustlessness?**
   - Conjecture: At least 1 block for commit, 1 for reveal/execute
   - Can we do better with probabilistic guarantees?
   - **Update**: Paradigm's Leaderless Auctions uses 4 rounds off-chain, then settles on Ethereum

2. **Can VDF verification be made gas-efficient on EVM?**
   - Current: ~200k gas for RSA-based VDF verification
   - Precompiles could help (EIP needed?)
   - Alternative: optimistic verification with fraud proofs

3. **How to handle partial fills in batch auctions?**
   - Pro-rata allocation?
   - Priority by submission time?
   - Random selection?

4. **What if no orders arrive in a batch?**
   - Empty batches waste gas
   - Need minimum participation threshold?
   - Dynamic batch sizing?

5. **Cross-asset batches?**
   - Single-pair batch is simple
   - Multi-pair introduces routing complexity
   - CoW (coincidence of wants) requires solver-like logic

---

## New Insights from Paradigm "Leaderless Auctions" (Feb 2024)

### Critical Discovery
Paradigm has published a concrete protocol for trustless auctions that solves the "last look" problem!

### Key Mechanism Elements
1. **Threshold Encryption**: Bids encrypted so any f+1 of 3f+1 participants can decrypt
   - Uses [vetKeys](https://eprint.iacr.org/2023/616) or similar
   - No single party can see bids before submission deadline
   
2. **4-Round Protocol**:
   - Round 1: Submit signed, encrypted bids
   - Round 2: Gossip bid sets (who received what)
   - Round 3: Gossip bid views + threshold decryption shares
   - Round 4: Aggregate signatures for on-chain verification

3. **Fault Economics**: 
   - **Equivocation fault**: Conflicting bids → severe slashing
   - **Absence fault**: Missing from f+1 bid sets → penalty > option value
   - Key insight: "No free option" — if you want to cancel, you pay upfront

4. **Bandwidth**: O(n³) worst case, but O(1) in practice when honest + good network

### How This Relates to Our Approaches

| Our Approach | Paradigm's Solution | Comparison |
|-------------|---------------------|------------|
| Commit-Reveal | Threshold encryption | Their approach eliminates griefing via forced decryption |
| Time-Lock (VDF) | Threshold key | Threshold requires committee; VDF is trustless but expensive |
| Rotating Committee | Fixed participant set | They assume known participant set, we wanted permissionless |
| Uniform Price | Not addressed | We could combine their privacy with our clearing mechanism |

### What Paradigm Doesn't Solve
1. **Permissionless participation**: Requires known participant set (3f+1)
2. **On-chain execution**: Most logic is off-chain; Ethereum just settles
3. **Uniform clearing**: Doesn't address price fairness, just bid fairness
4. **MEV from execution**: Winning bid still goes to Ethereum → proposer sees it

### Our Potential Contribution: Leaderless + Uniform Clearing
Combine Paradigm's bid privacy mechanism with uniform price clearing:
1. Use Leaderless Auctions protocol for bid submission/revelation
2. All revealed bids form a batch
3. Compute clearing price on-chain (or via fraud-proof)
4. Execute all trades at uniform price

This would add:
- ✅ Order-irrelevant execution (eliminates sandwich even after reveal)
- ✅ Better capital efficiency (no overpayment vs. limit price)
- ⚠️ Complexity of on-chain clearing computation

---

## Revised Priority Order

1. **Study Paradigm protocol in depth** — their threshold encryption approach is mature
2. **Design uniform clearing layer** — what happens after bids are revealed?
3. **Consider permissionless variant** — can we adapt Leaderless Auctions for open participation?
4. **Gas optimization** — on-chain clearing price computation

---

---

## 🔥 NEW: Paradigm + Silent Setup Synthesis

### The Breakthrough Combination

**Problem**: All prior approaches had one of these flaws:
1. Required trusted setup (Flashbots, CoW)
2. Required known participant set (Paradigm's Leaderless)
3. Required interactive coordination (vanilla threshold)

**Solution**: Combine THREE recent advances:

| Component | Paper | Contribution |
|-----------|-------|--------------|
| Bid Privacy | Paradigm Leaderless | 4-round no-leader protocol |
| Efficient Batching | BTE (ePrint 2024/669) | O(n) communication |
| Permissionless Setup | Silent Setup (ePrint 2024/263) | No interactive setup |
| **+ Our Addition** | Uniform Clearing | MEV-resistant execution |

### Proposed Protocol: "Silent Batch Auction" (SBA)

**Phase 1: Commitment (Block N)**
- Anyone encrypts order using Silent Setup threshold key
- Submit encrypted order + deposit to smart contract
- No coordinator needed — pubkey is deterministic

**Phase 2: Batch Close (Block N+k)**
- Smart contract closes batch
- Committee (could be validators) generates decryption shares
- BTE ensures O(n) communication regardless of batch size

**Phase 3: Reveal & Clear (Block N+k+1)**
- Orders decrypted on-chain
- Smart contract computes uniform clearing price
- All orders execute at same price → no sandwich possible

### Why This Works

1. **Trustless**: Silent Setup = no trusted dealer
2. **Permissionless**: Anyone can join/leave
3. **MEV-Resistant**: Uniform price = order irrelevant
4. **Practical**: BTE makes batching efficient

### Open Questions
1. Who serves as the threshold committee? Validators? Stakers?
2. How to handle non-participation in decryption?
3. Gas costs for on-chain clearing price computation?
4. Can we use Shutter's existing Keyper network?

---

---

## 🔥🔥🔥 MAJOR UPDATE: BEAST-MEV EXISTS (2026-02-07)

### Discovery
**Our "Silent Batch Auction" concept has been implemented!**

Paper: [BEAST-MEV](https://eprint.iacr.org/2025/1419) (Aug 2025)
- Authors: Choudhuri, Faust, Garg, Policharla et al.
- Combines: Silent Setup + Batched Decryption
- Status: Implemented, benchmarked, Generic Group Model security proof

### What BEAST-MEV Solves
| Problem | BEAST-MEV Solution |
|---------|-------------------|
| Trusted Setup | Silent Setup — deterministic joint pubkey from individual keys |
| Per-tx Decryption Cost | Batched — O(1) communication per decryption server |
| Privacy Before Inclusion | Threshold encryption until block confirmation |
| Pending Tx Privacy | Unselected txs remain encrypted |

### What BEAST-MEV Does NOT Solve ← OUR OPPORTUNITY

1. **Execution Mechanism**
   - BEAST-MEV decrypts transactions, but doesn't specify execution order
   - After decryption, transactions are visible — back-running still possible
   - **We can add**: Uniform price clearing (all trades at same price)

2. **MEV Internalization**
   - Penumbra approach: Protocol captures arbitrage, burns or redistributes
   - BEAST-MEV is infrastructure, not a complete DEX
   - **We can add**: In-protocol arbitrage to capture value for LPs/stakers

3. **On-Chain Clearing Computation**
   - Computing clearing price on EVM is gas-intensive
   - No existing efficient implementation
   - **We can add**: ZK-verified off-chain clearing, fraud-proof clearing

4. **Accountability / Collusion Deterrence**
   - Threshold trust still required (f+1 honest of 3f+1)
   - New primitives exist: SSS, self-incriminating proofs, traceable TE
   - **We can add**: Integration with accountability mechanisms

---

## Revised Research Direction: "BEAST-MEV + Uniform Clearing"

### New Contribution: Trustless Uniform-Price DEX Layer

**Layer Architecture:**
```
┌─────────────────────────────────────────┐
│     Layer 3: Penumbra-Style Arb         │ ← Internalize MEV
├─────────────────────────────────────────┤
│     Layer 2: Uniform Price Clearing     │ ← OUR CONTRIBUTION
├─────────────────────────────────────────┤
│     Layer 1: BEAST-MEV Encryption       │ ← Already exists
├─────────────────────────────────────────┤
│     Layer 0: Ethereum / L2              │ ← Settlement
└─────────────────────────────────────────┘
```

### Design Goals for Layer 2

1. **Trustless Clearing**
   - Input: Set of decrypted orders (from BEAST-MEV)
   - Output: Uniform clearing price + fills
   - No additional trust assumptions beyond BEAST-MEV

2. **Gas Efficiency**
   - Problem: Computing market-clearing price on-chain is expensive
   - Solutions to explore:
     a) ZK proof of clearing price correctness
     b) Optimistic clearing with fraud proofs
     c) Batch-friendly clearing algorithms

3. **Capital Efficiency**
   - Execute at uniform price (no overpayment vs limit)
   - Pro-rata allocation for partial fills
   - Unused orders return funds

4. **Composability**
   - Integrate with existing DeFi
   - Support multiple trading pairs
   - Enable CoW (coincidence of wants)

---

## New Idea: ZK-Verified Clearing Price

### Concept
Instead of computing clearing price on-chain (expensive), prove it off-chain:

1. **Off-chain**: Solver computes clearing price P* from revealed orders
2. **ZK Proof**: Generate proof that P* satisfies market-clearing conditions
3. **On-chain**: Verify proof (cheap) + execute all orders at P*

### Why This Works
- Verification << Computation (ZK property)
- Market-clearing conditions are simple to verify:
  - Sum of buys at P* ≥ Sum of sells at P* (or opposite, with price adjustment)
  - No single order can improve outcome

### Challenges
- ZK circuit for variable-size order sets
- Proof generation latency (must be fast)
- Handling partial fills in ZK

---

## New Idea: Fraud-Proof Clearing

### Concept
Optimistic approach — assume solver is honest, slash if wrong:

1. **Solver posts**: Claimed clearing price P* + bonds collateral
2. **Challenge period**: Anyone can prove P* is wrong
3. **Settlement**: If no challenge, execute at P*; else slash solver

### Challenge Types
1. **Better price exists**: Challenger proves P' > P* (for sellers) or P' < P* (for buyers) would increase volume
2. **Order not filled**: Prove an order that should fill at P* was excluded
3. **Wrong fill amount**: Prove pro-rata allocation is incorrect

### Why This Could Work
- Most batches are small → gas acceptable
- Large batches justify challenge overhead
- Creates market for honest solvers

---

## Updated Priority List (Feb 2026)

### Immediate (This Week)
- [x] ~~Find BEAST-MEV paper~~ ✅ Found!
- [ ] Deep-read BEAST-MEV implementation details
- [ ] Study Weighted BTE for PoS integration
- [ ] Review HAL gas-optimization paper
- [x] ~~Search for production implementations~~ ✅ Found Uniswap CCA!
- [ ] **NEW**: Study Uniswap CCA implementation (open source!)
- [ ] **NEW**: Review Jump DFBA for maker/taker separation insights

### Short-term (This Month)
- [ ] Design uniform clearing algorithm for EVM
- [ ] Prototype ZK circuit for clearing price
- [ ] Estimate gas costs for fraud-proof approach
- [ ] Compare with CoW Protocol's UDP implementation
- [ ] **NEW**: Address a16z "limits" concerns in our design
- [ ] **NEW**: Spec integration with EIP-8105 (when available)

### Medium-term
- [ ] Implement clearing layer on testnet
- [ ] Integrate with Shutter Keyper network (or simulate)
- [ ] Benchmark end-to-end latency and gas
- [ ] Write specification document
- [ ] **NEW**: Combine DFBA flow separation with uniform clearing

---

## 🆕 Major Ecosystem Update (2026-02-07 PM)

### The Landscape Has Changed!

**Production implementations now exist:**
1. **Uniswap CCA** (Nov 2025) — Continuous Clearing Auctions on v4
   - Single clearing price per block ✅
   - ZK Passport for privacy ✅
   - Automatic liquidity bootstrapping ✅
   - BUT: Limited to token launches, not general DEX trading

2. **Jump DFBA** — Dual Flow Batch Auction design
   - Maker/taker separation ✅
   - Uniform clearing ✅
   - Sub-100ms batches ✅
   - BUT: No encryption layer mentioned

3. **EIP-8105** — Native encrypted mempool coming to Ethereum
   - Technology-agnostic (threshold, TEE, FHE, etc.) ✅
   - Sub-slot key revelation ✅
   - Proposed for Hegotá fork
   - BUT: No execution mechanism specified

### What This Means For Us

**Good News**: Our thesis is validated! Multiple teams are building toward the same vision.

**Shift in Focus**: We're no longer inventing from scratch. We're:
1. **Synthesizing** existing approaches into optimal architecture
2. **Filling gaps** between encryption layer and execution layer
3. **Optimizing** gas costs for on-chain clearing

### New Research Questions

1. **How does Uniswap CCA compute clearing prices?**
   - Is it gas-efficient?
   - Can we extend to multi-pair batches?
   - What are the ZK Passport circuits?

2. **Can DFBA's flow separation improve clearing efficiency?**
   - Separate auctions for makers vs takers
   - Reduces matching complexity?
   - Could integrate with BEAST-MEV

3. **How to integrate with EIP-8105?**
   - Our clearing layer should work with any key provider
   - Design for future-proof composability

4. **Addressing a16z Concerns**
   - Speculative MEV: Can uniform clearing mitigate?
   - Trust assumptions: Can we layer accountability on top?
   - Thesis: Encryption + uniform clearing = defense in depth

---

## New Idea: BEAST-MEV + CCA + DFBA Synthesis

### Concept: "Triple-Layer Fair Exchange"

```
┌──────────────────────────────────────────────┐
│  Layer 3: MEV Internalization (Penumbra)     │
├──────────────────────────────────────────────┤
│  Layer 2.5: Flow Separation (DFBA concept)   │ ← Maker/taker auctions
├──────────────────────────────────────────────┤
│  Layer 2: Continuous Clearing (CCA concept)  │ ← Uniform price per batch
├──────────────────────────────────────────────┤
│  Layer 1: Encrypted Mempool (BEAST-MEV)      │ ← Privacy until ordering
├──────────────────────────────────────────────┤
│  Layer 0: Ethereum via EIP-8105              │ ← Settlement
└──────────────────────────────────────────────┘
```

### How It Works

1. **Submit**: Users encrypt orders via EIP-8105 encrypted tx type
2. **Collect**: Orders accumulate in encrypted mempool
3. **Decrypt**: At batch boundary, BEAST-MEV decrypts batch
4. **Separate**: Orders split into maker/taker flows (DFBA)
5. **Clear**: Each flow clears at uniform price (CCA)
6. **Internalize**: Protocol arbitrage captured (Penumbra)
7. **Settle**: Trades execute on Ethereum

### Why This Could Be Optimal

- **Privacy**: BEAST-MEV encrypts until after ordering
- **Fairness**: Uniform clearing eliminates ordering MEV
- **Efficiency**: Flow separation reduces matching complexity
- **Value Capture**: Internalized arb benefits LPs/stakers
- **Composability**: Works with EIP-8105 future upgrades

---

## Addressing a16z "Limits" Paper

Their concerns and our responses:

| a16z Concern | Our Response |
|--------------|--------------|
| Speculative MEV (guess attacks) | Uniform clearing makes position in batch irrelevant |
| Threshold trust is strong | Layer accountability primitives (SSS, traceable TE) |
| Who decrypts? | EIP-8105's registry allows competition among providers |
| Plaintext after decrypt vulnerable | Immediate clearing — no time for back-running |
| TEE trust | Tech-agnostic design (don't require TEE) |

**Key insight**: Encrypted mempool alone doesn't solve MEV. Encrypted mempool + uniform clearing + flow separation = robust defense.

---

## 🆕 AllCoreDevs Validation (2026-02-07 Evening)

### EIP-8105 is Now Official
- Jannik Luhn (Shutter) presented at Jan 29 ACD meeting
- Positioned as **complementary to FOCIL** (censorship resistance + MEV protection)
- Direct quote: "it relies on trusted parties, which is bad for decentralisation"
- **Implication**: Our Layer 2 clearing work will have a native L1 foundation

### Frame Transactions (EIP-8141) Adds Post-Quantum Dimension
- Vitalik's endorsement signals priority
- Post-quantum signatures = longer ciphertexts
- **Design consideration**: Our clearing layer should be signature-agnostic

### Production Validation: CCA on Base
- Uniswap CCA is now **permissionless on Base** (Jan 22, 2026)
- Web app has auction UI (Feb 2, 2026)
- We can study live deployments, not just theory

### New Research Direction: ZK-Proven Clearing

Given discoveries today:
1. **Brevis ProverNet**: Decentralized ZK proof marketplace exists
2. **NIST MPTS 2026**: Threshold crypto standardization underway
3. **EIP-8141**: Post-quantum considerations needed

**Proposed Architecture for ZK Clearing:**
```
┌─────────────────────────────────────────────────┐
│  Uniswap CCA-style UI (bidding interface)       │
├─────────────────────────────────────────────────┤
│  Our ZK Clearing Circuit                        │
│  ┌─────────────────────────────────────────┐   │
│  │ Inputs: Decrypted orders (from EIP-8105) │   │
│  │ Prove: Clearing price P* is optimal      │   │
│  │ Prove: Fill allocations are pro-rata     │   │
│  │ Output: Proof π + settlements            │   │
│  └─────────────────────────────────────────┘   │
├─────────────────────────────────────────────────┤
│  Brevis ProverNet (decentralized proving)       │
├─────────────────────────────────────────────────┤
│  EIP-8105 Encrypted Mempool                     │
├─────────────────────────────────────────────────┤
│  Ethereum L1 (Hegotá+)                          │
└─────────────────────────────────────────────────┘
```

### Competitive Landscape Update

| Project | Layer | Status | Gap We Fill |
|---------|-------|--------|-------------|
| Shutter/EIP-8105 | Encryption | In development | Execution mechanism |
| Uniswap CCA | Clearing | Production | Multi-pair + general DEX |
| Jump DFBA | Flow sep | Design | Encryption layer |
| CoW Protocol | Intent | Production | Trustless solvers |
| Penumbra | Full stack | Production | EVM compatibility |

**Our unique position**: EVM-native, ZK-verified, trustless clearing on top of EIP-8105.

---

## Update Log
- [2026-02-04] Initial synthesis from literature review
- [2026-02-04] Identified Approach 5 (Time-Lock + Uniform Price) as leading candidate
- [2026-02-04] Proposed 4 novel ideas (A-D) for exploration
- [2026-02-04] **MAJOR UPDATE**: Found Paradigm Leaderless + Silent Setup papers
- [2026-02-04] New leading approach: "Silent Batch Auction" combining 3 advances
- [2026-02-04] **Major update**: Discovered Paradigm "Leaderless Auctions" paper
  - Solves last-look problem with threshold encryption + fault economics
  - Shifts our focus: can we combine their privacy with uniform clearing?
  - New potential contribution: Leaderless + Uniform Clearing hybrid
- [2026-02-07] **CRITICAL UPDATE**: BEAST-MEV paper found — our core concept already exists!
  - Pivoting focus to Layer 2 (Uniform Clearing) contribution
  - New ideas: ZK-verified clearing, fraud-proof clearing
  - Research direction: Build execution layer on top of BEAST-MEV infrastructure
- [2026-02-07 PM] **ECOSYSTEM MATURATION**:
  - Found Uniswap CCA (production uniform clearing!)
  - Found Jump DFBA (maker/taker flow separation)
  - Found EIP-8105 (native encrypted mempool for Ethereum)
  - Found TrX paper (production-ready encrypted BFT, 27ms overhead)
  - New synthesis: BEAST-MEV + CCA + DFBA "Triple-Layer" architecture
  - Addressed a16z concerns in our framework
- [2026-02-07 PM] **ALLCOREDEVS VALIDATION**:
  - EIP-8105 formally presented as Hegotá headliner (Jan 29 ACD)
  - EIP-8141 Frame Transactions (post-quantum AA) endorsed by Vitalik
  - CCA deployed to Base (permissionless) and web app live
  - Consensys acquired MEV Blocker — consolidation in MEV protection
  - NIST MPTS 2026 workshop (March) — threshold crypto standardization
  - New direction: ZK-proven clearing with Brevis ProverNet integration
- [2026-02-07 Eve] **DAILY CRON RESEARCH UPDATE**:
  - **RNBW auction validation**: First major CCA post-launch → $0.10→$0.13 (30% discovery)
  - **Infrastructure consolidation**: Chainlink→Atlas, Consensys/SMG→MEV Blocker
  - **New ePrint papers**: Post-quantum threshold KEM (2026/021), ThFHE attacks (2026/031)
  - **Glamsterdam progress**: bals-devnet-2 live, H1 2026 target
  - **Hegotá**: Headliner deadline passed, EIP-8105/FOCIL/Frame Tx leading
  - **New competitor**: Shade Network encrypted mempool testnet

---

## 🆕 New Idea: Empirical Study of CCA Price Discovery (2026-02-07 Eve)

### Opportunity from RNBW Data

The Rainbow token auction provides first empirical data on CCA price discovery:

| Metric | Value |
|--------|-------|
| Starting price | $0.10 |
| Clearing price | $0.13 |
| Price discovery | +30% |
| Auction window | ~3 days |
| Pre-bid period | 24 hours |

### Research Questions

1. **How did the clearing algorithm determine $0.13?**
   - Need to study on-chain transaction data
   - What was the order book shape?
   - How many bids at different price levels?

2. **What was the gas cost of clearing?**
   - Critical for our gas-efficiency research
   - Can we extract from Base explorer?

3. **Did MEV occur during the auction?**
   - Sandwich attacks on auction participants?
   - Front-running of bid transactions?
   - Or did CCA successfully prevent?

4. **How does token launch clearing differ from continuous DEX?**
   - Token launch: One-way flow (buyers only initially)
   - DEX: Two-way flow (buyers + sellers)
   - Different optimization problems

### Proposed Analysis

1. **Data collection**: Fetch all RNBW CCA transactions from Base
2. **Reconstruct order book**: Map bids to prices and quantities
3. **Verify clearing**: Confirm $0.13 is optimal given order book
4. **Gas analysis**: Total gas used for clearing computation
5. **MEV scan**: Check for suspicious transaction patterns

---

## 🆕 New Idea: Multi-Provider Clearing Layer (2026-02-07 Eve)

### Observation

MEV infrastructure is consolidating:
- **Chainlink**: Now has Atlas (ordering) + SVR (OEV) + FSS (fair sequencing)
- **Consensys/SMG**: Now has MEV Blocker + builder infrastructure
- **Flashbots**: Protect, SUAVE, block building
- **Shutter**: EIP-8105, Keyper network

### Opportunity: Provider-Agnostic Clearing

Our clearing layer could work with **any** encrypted mempool provider:

```
┌─────────────────────────────────────────────────┐
│      Trustless Uniform Clearing Layer (Ours)    │
├───────────┬───────────┬───────────┬─────────────┤
│ EIP-8105  │  Shutter  │  SUAVE    │  Radius     │
│ (native)  │ (Keypers) │ (TEE)     │ (PVDE)      │
└───────────┴───────────┴───────────┴─────────────┘
```

### Design Requirements

1. **Input abstraction**: Accept decrypted orders from any source
2. **Output format**: Standard settlement instructions
3. **Provider-specific adapters**: Handle timing/format differences
4. **Fallback mechanisms**: If one provider fails, degrade gracefully

### Competitive Advantage

- Not locked into single encryption provider
- Can use best-in-class for each chain (EIP-8105 for Ethereum, Shutter for Gnosis, etc.)
- Future-proof as new providers emerge

---

## 🆕 New Idea: Security Audit Consideration (2026-02-07 Eve)

### Critical Finding from ePrint 2026/031

The CryptoLab paper found **key-recovery attacks** in prior ThFHE schemes:
- Mouchet et al. (Journal of Cryptology 2023) — VULNERABLE
- Mouchet et al. (ACM CCS 2024) — VULNERABLE

### Implications for Our Work

1. **Threshold crypto is tricky**: Even published, peer-reviewed schemes can have flaws
2. **Defense in depth**: Don't rely solely on cryptographic guarantees
3. **Our uniform clearing adds value**: Even if encryption breaks, ordering doesn't matter
4. **Audit requirement**: Any production clearing layer needs formal verification

### Our Security Thesis (Refined)

```
Security = Encryption + Uniform Clearing + Accountability
           └─ If fails ──┘└─ Backup ────────┘└─ Deterrent ─┘
```

Even if threshold encryption has a vulnerability:
1. Uniform clearing means order doesn't matter → reduced MEV even without encryption
2. Accountability primitives deter collusion → economic disincentive
3. Defense in depth > single point of failure

---

## Updated Research Priorities (Post-Cron Update)

### This Week
1. ~~Daily literature search~~ ✅ Completed (Feb 7)
2. [ ] Fetch RNBW auction on-chain data from Base
3. [ ] Analyze CCA clearing algorithm gas costs
4. [ ] Study ePrint 2026/031 attack implications

### This Month
1. [ ] Design multi-provider clearing interface
2. [ ] Prototype ZK clearing circuit
3. [ ] Compare fraud-proof vs ZK approaches (gas analysis)
4. [ ] Write draft specification for "Trustless Uniform Clearing Layer"

### Blocking on User Input
- [ ] Should we prioritize integration with specific provider (EIP-8105 likely)?
- [ ] Is formal verification required before prototyping?
- [ ] Target chain: Ethereum L1, Base, or generic EVM?

---

## 🆕 Critical Validation: Ordering Fairness Is Fundamentally Limited (2026-02-07 3PM)

### Academic Proof of Our Thesis

**Paper**: "On the Effectiveness of Mempool-based Transaction Auditing" (arXiv 2601.14996)
**Authors**: Jannik Albrecht, Ghassan Karame (Runtime Verification)
**Published**: January 2026

### Key Findings

| Finding | Implication |
|---------|-------------|
| **30-second threshold** for reliable ordering | Transactions sent <30s apart have probabilistic, not deterministic, order |
| **25%+ false positive rate** for censorship detection | Mempool auditing frequently mislabels honest miners |
| **"Limited subset" guarantee** for batch-fair ordering | Only some transactions can be fairly ordered |

### Direct Quote
> "batch-fair ordering schemes can offer only strong fairness guarantees for a limited subset of transactions in real-world deployments"

### Why This Matters for Us

This paper **academically validates our core thesis**:

1. **Ordering-based fairness is insufficient**
   - Even with perfect mempool visibility, network propagation introduces irreducible uncertainty
   - Sub-30-second ordering is fundamentally non-deterministic across observers
   - No amount of better auditing can fix this — it's a physics/network problem

2. **Uniform clearing is the correct approach**
   - If ordering is probabilistic, make it irrelevant
   - Same price for all participants = ordering doesn't matter
   - This is immune to the 30-second limitation

3. **Defense in depth validated**
   - Encryption hides content (BEAST-MEV)
   - Uniform clearing eliminates ordering MEV (our contribution)
   - Even if encryption fails, clearing still protects
   - Even if both fail, accountability deters

### Refined Value Proposition

**Before this paper**: "Uniform clearing is *better* than ordering fairness"
**After this paper**: "Uniform clearing is *necessary* because ordering fairness is provably limited"

### New Research Direction

The paper suggests a **30-second batch window** is the minimum for deterministic ordering:
- If batch window < 30s: Some orders have undefined relative order
- If batch window ≥ 30s: Can reliably determine who submitted first

**Design implication**: Our batch windows should be ≥30 seconds for predictable behavior
- Matches block time on Ethereum (~12s per slot, but 30s = ~2-3 slots)
- Longer batches = more liquidity aggregation
- Trade-off: Latency vs ordering certainty

### Integration with Our Architecture

```
┌─────────────────────────────────────────────────┐
│  Order Submission (encrypted via BEAST-MEV)     │
├─────────────────────────────────────────────────┤
│  Batch Window (≥30s for deterministic order)    │ ← From arXiv 2601.14996
├─────────────────────────────────────────────────┤
│  Decryption (threshold, end of batch)           │
├─────────────────────────────────────────────────┤
│  Uniform Clearing (ordering irrelevant)         │ ← Our key contribution
├─────────────────────────────────────────────────┤
│  Settlement (on-chain)                          │
└─────────────────────────────────────────────────┘
```

The 30-second finding actually **reinforces** why we need uniform clearing:
- Short batches (< 30s): Ordering is probabilistic anyway, uniform clearing removes ambiguity
- Long batches (≥ 30s): Uniform clearing still provides capital efficiency and MEV resistance

---

## 🆕 Parallel Execution Considerations (Glamsterdam, 2026-02-07 3PM)

### EIP-7928: Block-Level Access Lists

Glamsterdam introduces parallel transaction execution:
- Transactions declare which accounts/storage slots they access
- Non-conflicting transactions execute simultaneously
- Gas limit increases 3× (60M → 200M)

### Impact on Our Design

**Potential Benefits:**
1. Higher throughput → more transactions per batch
2. Cheaper gas → more complex clearing computation feasible
3. Predictable state access → cleaner integration

**Potential Challenges:**
1. Parallel execution changes MEV dynamics (unclear how)
2. Access list requirements may conflict with encrypted transactions
3. Need to study interaction with EIP-8105 encrypted tx type

### Open Questions

1. Can encrypted transactions have access lists?
   - Access lists reveal which contracts are touched → partial information leak
   - Or: Decrypt first, then compute access list, then execute

2. Does parallel execution help or hurt batch auctions?
   - Pro: Multiple batch settlements can run in parallel
   - Con: Proposer has more flexibility in ordering parallel groups

3. Integration with EIP-8105:
   - EIP-8105 encrypted txs are decrypted by key providers
   - After decryption, access lists can be computed
   - But timing matters: decrypt → access list → execute must happen in one block?

### Design Consideration

Our clearing layer should:
1. Support access list generation after decryption
2. Minimize conflicts with other transactions (isolate state)
3. Take advantage of parallelization where possible

---

## Update Log (continued)
- [2026-02-07 3PM] **Critical validation**: arXiv 2601.14996 proves ordering fairness limited to 30s threshold
- [2026-02-07 3PM] Added analysis of Glamsterdam parallel execution (EIP-7928) impact
- [2026-02-07 3PM] Refined value proposition: Uniform clearing is *necessary*, not just *better*
- [2026-02-07 4PM] **Saturday Evening Cron Update**: New cryptographic directions identified

---

## 🆕 New Idea: Witness Encryption for Order Privacy (2026-02-07 4PM)

### Discovery: ePrint 2026/175 — Implementable WE

A new paper shows **witness encryption for SNARK verification** is now practical!

**What is Witness Encryption?**
- Encrypt data to a *statement* (e.g., "X will be included in a valid batch")
- Anyone with a *witness* (proof that statement is true) can decrypt
- No trusted setup, no key holders, no committee

### Application to Encrypted Orders

**Traditional Threshold Approach:**
```
Order → Encrypt(threshold_pubkey) → Wait for committee → Decrypt
                                    ↑ Trust assumption here
```

**Witness Encryption Approach:**
```
Order → Encrypt("this order is in a batch with proof π") → Wait for batch proof → Decrypt
                                                          ↑ No trusted party!
```

### How It Would Work

1. **Encrypt**: User encrypts order to statement: "Order O is included in batch B with clearing proof π"
2. **Batch**: Orders accumulate encrypted
3. **Prove**: Solver computes clearing price P* and generates SNARK proof π
4. **Decrypt**: π is the witness — anyone can decrypt orders using it
5. **Execute**: All orders execute at P*

### Why This Is Elegant

- **Trustless**: No committee, no key holders, no threshold
- **Self-enforcing**: Decryption tied to valid clearing proof
- **Atomic**: Can't decrypt without proving correct clearing

### Challenges

1. **Circular dependency?**
   - Need orders to compute clearing
   - Need clearing to decrypt orders
   - **Solution**: Homomorphic operations on encrypted orders?
   
2. **Proof size**
   - WE typically has large ciphertexts
   - Gas costs may be prohibitive
   
3. **Efficiency**
   - 2026/175 claims "practical" but needs benchmarking
   - May only work for small batches

### Research Direction

Explore WE as **alternative** to threshold for specific use cases:
- Small, high-value batches (NFT auctions)
- Cross-chain bridges (where committee trust is expensive)
- Privacy pools (similar to Zcash shielded pools)

For high-throughput DEX, threshold (BEAST-MEV) likely still preferred.

---

## 🆕 SNARK Efficiency Revolution (a16z 2026 Predictions)

### Key Insight from a16z

> "Proving a computation could take 1,000,000× more work than just running it. Worth it when you're amortizing across many thousands of validators, but impractical anywhere else. **That's about to change.**"

### What This Means for ZK Clearing

1. **ZK proofs becoming mainstream** outside blockchain
   - Patent searches, art generation, research assistance
   - Prover efficiency improving dramatically
   
2. **Off-chain proving markets emerging**
   - Brevis ProverNet: Decentralized proof marketplace
   - Competition drives costs down
   
3. **Hardware acceleration coming**
   - ePrint 2026/160: ASIC chips for homomorphic encryption
   - Similar trajectory expected for SNARK proving

### Implications for Our Design

**Short-term (2026):**
- ZK clearing proof still expensive but feasible
- Target: 1 proof per batch (amortize across all orders)
- Use fraud-proof as fallback for small batches

**Medium-term (2027+):**
- Per-order ZK proofs may become practical
- Real-time clearing verification possible
- Remove fraud-proof complexity entirely

### Updated ZK Clearing Architecture

```
┌─────────────────────────────────────────────────┐
│              ZK Clearing Circuit                │
│  ┌───────────────────────────────────────────┐ │
│  │ Inputs: Encrypted orders (public commits) │ │
│  │ Private: Decrypted orders (from BEAST-MEV)│ │
│  │ Prove:                                    │ │
│  │  1. Decryption was correct               │ │
│  │  2. Clearing price P* is optimal         │ │
│  │  3. Fill allocations are pro-rata        │ │
│  │ Output: (P*, fills[], proof π)           │ │
│  └───────────────────────────────────────────┘ │
├─────────────────────────────────────────────────┤
│  Proving Infrastructure                         │
│  ┌──────────────┬──────────────┬─────────────┐ │
│  │ Brevis       │ Custom       │ Local       │ │
│  │ ProverNet    │ Prover Pool  │ Hardware    │ │
│  └──────────────┴──────────────┴─────────────┘ │
├─────────────────────────────────────────────────┤
│  On-Chain Verifier (cheap, constant-size proof) │
└─────────────────────────────────────────────────┘
```

---

## 🆕 Parallel Execution Deep Dive (Glamsterdam)

### EIP-7928: Block-Level Access Lists (BALs)

**Current state**: Transactions execute sequentially because EVM doesn't know what state they'll touch until runtime.

**After Glamsterdam**: Blocks include pre-declared access lists → nodes can parallelize non-conflicting transactions.

### Impact on Batch Auction Design

**Optimization Opportunity:**
If our batch clearing is isolated (only touches its own state), it can run in parallel with other block activity.

**Design Principle:**
```
┌─────────────────────────────────────────────────┐
│  Batch Auction State (Isolated)                 │
│  ┌───────────────────────────────────────────┐ │
│  │ orders[] — encrypted then decrypted       │ │
│  │ clearingPrice — computed per batch        │ │
│  │ fills[] — settlement amounts              │ │
│  │ batchNonce — increments each batch        │ │
│  └───────────────────────────────────────────┘ │
│  ↕ Parallel with rest of block                 │
└─────────────────────────────────────────────────┘
```

**Access List for Clearing:**
```solidity
accessList: [
    BatchAuction.orders[batchId],
    BatchAuction.clearingPrice[batchId],
    BatchAuction.fills[batchId],
    Token.balances[...] // All participants
]
```

### Multi-Batch Parallelization

Could run multiple independent batches in parallel:
- ETH/USDC batch
- BTC/USDC batch  
- ETH/BTC batch

As long as participant overlaps are declared, no conflicts.

---

## 🆕 "Know Your Agent" (KYA) Implications

### The Problem

From a16z article:
> "Non-human identities now outnumber human employees 96-to-1 in financial services — yet these identities remain unbanked ghosts."

### Why This Matters for DEX

**Current DEX model**: Human signs transaction
**Agent economy model**: Agent signs on behalf of human

### Design Consideration

Our clearing layer should support:
1. **Agent-signed orders**: Cryptographic link to principal
2. **Spending limits**: Constraint on agent's trading authority
3. **Audit trails**: Which agent placed which order

### Potential Integration

```
Order {
    principal: 0x...     // Human's address
    agent: 0x...         // Agent's identity (could be contract)
    signature: ...       // Agent's signature
    constraints: {       // Limits on agent
        maxOrderSize: 1000 USDC
        allowedPairs: [ETH/USDC, BTC/USDC]
    }
    principalApproval: ... // One-time or per-trade?
}
```

This aligns with EIP-8141 Frame Transactions (signature-scheme agnostic).

---

## 🆕 Revised Architecture (Feb 2026)

### Full Stack Vision

```
┌─────────────────────────────────────────────────────────┐
│  Layer 4: Agent Economy Interface                       │
│  ┌─────────────────────────────────────────────────────┐│
│  │ x402 payments │ KYA credentials │ Agent wallets     ││
│  └─────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────┤
│  Layer 3: MEV Internalization (Future)                  │
│  ┌─────────────────────────────────────────────────────┐│
│  │ Protocol arbitrage │ LP value capture │ Burn/rebate ││
│  └─────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────┤
│  Layer 2: TRUSTLESS UNIFORM CLEARING (OUR FOCUS)        │
│  ┌─────────────────────────────────────────────────────┐│
│  │ ZK clearing │ Fraud proofs │ Multi-pair batching    ││
│  │ Flow separation (DFBA) │ Pro-rata fills             ││
│  └─────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────┤
│  Layer 1: Encrypted Order Pool                          │
│  ┌────────────┬────────────┬────────────┬─────────────┐ │
│  │ EIP-8105   │ BEAST-MEV  │ Shutter    │ WE (future) │ │
│  │ (L1 native)│ (academic) │ (Keypers)  │ (research)  │ │
│  └────────────┴────────────┴────────────┴─────────────┘ │
├─────────────────────────────────────────────────────────┤
│  Layer 0: Settlement                                    │
│  ┌────────────┬────────────┬────────────┬─────────────┐ │
│  │ Ethereum   │ Base       │ Arbitrum   │ Gnosis      │ │
│  │ (Hegotá+)  │ (OP Stack) │ (Orbit)    │ (Shutter)   │ │
│  └────────────┴────────────┴────────────┴─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Priority for Next Phase

1. **Layer 2 spec**: Define clearing interface that works with any Layer 1 provider
2. **ZK circuit prototype**: Prove clearing price correctness
3. **Gas benchmarking**: Compare ZK vs fraud-proof costs
4. **Integration test**: Hook into Uniswap CCA for empirical data

---

## Updated Research Priorities (Feb 7 Evening)

### Immediate (This Week)
- [x] Daily literature search ✅
- [x] Update INDEX.md with new sources ✅
- [ ] Deep-read ePrint 2026/175 (witness encryption)
- [ ] Fetch RNBW auction data from Base explorer
- [ ] Find NIST MPTS 2026 recordings/proceedings

### Short-term (Feb 8-14)
- [ ] Prototype ZK clearing circuit (simplified: 10 orders)
- [ ] Benchmark WE ciphertext sizes for feasibility
- [ ] Study parallel execution implications (EIP-7928)
- [ ] Draft "agent-compatible" order format

### Medium-term (Feb 2026)
- [ ] Full clearing layer spec document
- [ ] Compare with CoW Protocol's UDP implementation
- [ ] Design multi-provider abstraction layer
- [ ] Contribute to EIP-8105 discussion

---

## 🆕 L1/L2 Paradigm Shift — Strategic Reframe (2026-02-07 6PM)

### Vitalik's Bombshell (Feb 3, 2026)

> "The rollup-centric roadmap no longer makes sense."

### The Data

| Metric | Mid-2025 | Feb 2026 | Change |
|--------|----------|----------|--------|
| L2 monthly addresses | 58.4M | ~30M | **-48%** |
| L1 active addresses | 7M | 15M | **+114%** |
| L1 tx fees | High | Very low | Dramatic drop |
| L1 gas limit | 60M | 200M (planned) | **+233%** |

### Why L2 Usage Is Dropping

1. **L1 fees collapsed**: Proto-danksharding, execution optimizations
2. **L2 security lagged**: Most L2s never reached Stage 2 rollup status
3. **UX friction**: Bridging, multiple gas tokens, fragmented liquidity
4. **User preference**: When L1 is cheap, users prefer its security

### Implications for Our Research

**Original Assumption**: Deploy on L2 first (faster iteration, lower costs)

**New Reality**: L1 deployment may be optimal:
- EIP-8105 provides native encrypted mempool on L1
- ePBS removes relay centralization bottleneck
- BALs enable parallel execution (batch clearing can run concurrently)
- 3× gas limit means more complex on-chain computation is viable
- Users are already migrating back to L1

### Revised Deployment Strategy

```
┌─────────────────────────────────────────────────────────┐
│  PRIMARY: Ethereum L1 (Hegotá+)                         │
│  ┌─────────────────────────────────────────────────────┐│
│  │ • EIP-8105 encrypted mempool (native)              ││
│  │ • ePBS (no relay trust)                            ││
│  │ • BALs (parallel clearing execution)              ││
│  │ • 200M gas limit (complex clearing feasible)       ││
│  └─────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────┤
│  SECONDARY: Specialized L2s                             │
│  ┌─────────────────────────────────────────────────────┐│
│  │ • Privacy-focused (Aztec, future zk-rollups)       ││
│  │ • Application-specific (gaming, social)            ││
│  │ • High-frequency (where sub-block batching needed) ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

### What Vitalik Wants from L2s

1. **Privacy**: "Privacy-focused virtual machines"
2. **Specialization**: "Efficiency specialized around a particular application"
3. **Extreme scale**: "Truly extreme levels of scaling that even a greatly expanded L1 will not do"
4. **Non-financial**: "Different design for non-financial applications, e.g. social, identity, AI"

### How This Affects Our Clearing Layer

**For L1 (primary target)**:
- Work with EIP-8105 encrypted tx type
- Leverage parallel execution via BALs
- Design for block-size batches (~12 seconds)
- Gas optimization less critical (higher limit)

**For specialized L2s (secondary)**:
- Privacy L2s: Could use our clearing with ZK Passport integration
- High-frequency L2s: Sub-block batching for latency-sensitive use cases
- Application L2s: Embedded clearing for specific DEX applications

---

## 🆕 Trillion Dollar Security Dashboard — Design Implications (2026-02-07 6PM)

### The EF's Six Security Dimensions

1. **User Experience Security**: Wallet UX, transaction signing, phishing protection
2. **Smart Contract Security**: Audits, formal verification, bug bounties
3. **Infrastructure Security**: Node software, client diversity, RPC providers
4. **Consensus Security**: Validator set, finality, reorg resistance
5. **Monitoring Security**: Anomaly detection, incident response, transparency
6. **Social/Governance Security**: Upgrade processes, community coordination

### How Our Clearing Layer Fits

| Dimension | Our Responsibility |
|-----------|-------------------|
| UX | Clear order status, price transparency, fair execution guarantees |
| Smart Contract | Audited clearing logic, formal verification of price computation |
| Infrastructure | Multi-provider support (don't rely on single encryption provider) |
| Consensus | Integrate with EIP-8105 key provider registry |
| Monitoring | Batch execution transparency, MEV detection, anomaly alerts |
| Social | Open-source, community governance of protocol parameters |

### Design Principle: Defense in Depth

The 1TS initiative reinforces our multi-layer security approach:

```
Security Stack
┌───────────────────────────────────────────┐
│  Social: Open governance, transparency    │
├───────────────────────────────────────────┤
│  Monitoring: MEV detection, alerts        │
├───────────────────────────────────────────┤
│  Consensus: EIP-8105 key provider trust   │
├───────────────────────────────────────────┤
│  Contract: Audited clearing, ZK proofs    │
├───────────────────────────────────────────┤
│  Economic: Slashing, bonds, incentives    │
├───────────────────────────────────────────┤
│  Cryptographic: Encryption, signatures    │
└───────────────────────────────────────────┘
```

---

## 🆕 Verification Theater Warning (2026-02-07 6PM)

### ePrint 2026/192 Key Findings

The paper warns that "formally verified" crypto libraries may provide false assurance:
- Marketing claims often exceed actual verification scope
- Critical code paths may not be covered by proofs
- Implementation bugs can exist outside verified core

### Implications for Our Design

1. **Multiple independent audits**: Don't rely on single auditor or verification tool
2. **Bug bounties**: Economic incentives for vulnerability discovery
3. **Defense in depth**: Assume any single layer might fail
4. **Operational security**: Monitoring and incident response as first-class concerns

### Our Verification Strategy

```
┌─────────────────────────────────────────────────────────┐
│  Verification Layers (Defense in Depth)                 │
├─────────────────────────────────────────────────────────┤
│  1. Formal Verification: Core clearing algorithm        │
│     - Coq/Lean proofs for price computation            │
│     - Bounded model checking for edge cases            │
├─────────────────────────────────────────────────────────┤
│  2. Traditional Audits: Full contract review            │
│     - Multiple independent auditors (e.g., OZ + Spearbit)│
│     - Focus on integration points, gas assumptions     │
├─────────────────────────────────────────────────────────┤
│  3. Economic Audits: Incentive analysis                 │
│     - Game-theoretic review of slashing conditions     │
│     - Simulation of attack scenarios                   │
├─────────────────────────────────────────────────────────┤
│  4. Fuzzing & Testing: Implementation coverage          │
│     - Foundry invariant testing                        │
│     - Echidna property-based fuzzing                   │
├─────────────────────────────────────────────────────────┤
│  5. Bug Bounty: Ongoing discovery                       │
│     - Cantina/Immunefi program                         │
│     - Graduated rewards based on severity              │
├─────────────────────────────────────────────────────────┤
│  6. Monitoring: Runtime detection                       │
│     - On-chain anomaly detection                       │
│     - Off-chain monitoring dashboard                   │
└─────────────────────────────────────────────────────────┘
```

---

## Questions for User (Updated)

1. **Target chain priority**: Given Vitalik's L2 critique, should we prioritize Ethereum L1 (EIP-8105 native) over L2?
   - **Recommendation**: Yes, L1 primary with specialized L2 as secondary
2. **Witness encryption**: Worth deep exploration, or keep focus on threshold?
   - **Recommendation**: Keep threshold primary (BEAST-MEV), WE as research track
3. **Verification approach**: How much to invest in formal verification vs other methods?
   - **Recommendation**: Multi-layer approach per "Verification Theater" findings

---

## Update Log (continued)
- [2026-02-07 6PM] **L1/L2 paradigm shift analysis**: Vitalik's critique + data showing L2 decline
- [2026-02-07 6PM] **EF 1TS Dashboard**: Integrated six security dimensions into our design
- [2026-02-07 6PM] **Verification Theater warning**: Multi-layer verification strategy proposed
- [2026-02-07 6PM] **Revised deployment strategy**: L1 primary, specialized L2 secondary

## 🆕 Major New Discoveries (2026-02-07 5PM Cron)

### Arcium Mainnet Alpha: MPC Alternative to Threshold

**Discovery**: Arcium launched Mainnet Alpha on Solana (Feb 2, 2026), bringing MPC-based encrypted computation to production.

**Key Differentiators from BEAST-MEV:**
| Aspect | BEAST-MEV | Arcium |
|--------|-----------|--------|
| Approach | Threshold encryption | Multi-party computation |
| Chain | Ethereum-focused | Solana-native |
| Trust model | t-of-n threshold | MPC across distributed nodes |
| Computation | Decrypt then execute | Compute on encrypted data |

**Why This Matters:**
1. **Validation**: Another team proving encrypted execution is viable at scale
2. **Alternative path**: MPC can do more than threshold (arbitrary computation)
3. **Solana presence**: If we build EVM-first, Arcium handles Solana

**First App — Umbra Private:**
- Anonymous transfers and swaps on Solana
- Encrypted balances
- SDK for developers
- **Note**: Similar to what we'd build, but Solana-native

**Implication for Our Work:**
- Focus on EVM — Arcium has Solana covered
- Study Umbra as reference implementation for private DEX UX
- Consider MPC as alternative to threshold for compute-intensive operations

---

### Fhenix DBFV: FHE Becoming Practical

**Discovery**: Fhenix announced Decomposable BFV (DBFV), a breakthrough that makes exact FHE practical for blockchain (Feb 6, 2026).

**The Problem DBFV Solves:**
- FHE operations on large integers cause "noise explosion"
- Noise management (bootstrapping) is extremely expensive
- Made FHE impractical for financial computations

**The Solution:**
- Decompose large plaintext into smaller "limbs" during encryption
- Each limb managed independently → better noise control
- Avoids frequent bootstrapping → massive cost reduction

**Why This Matters for Encrypted Mempools:**

| Current State | With FHE |
|---------------|----------|
| Threshold: Encrypt then decrypt | FHE: Compute while encrypted |
| Reveals orders at batch boundary | Can compute clearing while encrypted! |
| Requires committee for decryption | No committee needed |

**Potential Future Direction:**
```
┌─────────────────────────────────────────────────┐
│  FHE-Based Clearing (Future Vision)             │
├─────────────────────────────────────────────────┤
│  1. Encrypt order with FHE                      │
│  2. Submit to batch (encrypted)                 │
│  3. Smart contract computes clearing price      │
│     ON ENCRYPTED DATA (no decryption!)          │
│  4. Execute at clearing price                   │
│  5. Only reveal final balances                  │
└─────────────────────────────────────────────────┘
```

**Caveat**: DBFV is research; production integration planned for "later this year"

**Action**: Monitor Fhenix progress; may obsolete threshold approaches

---

### Uniswap CCA: Production Code Available

**Discovery**: Uniswap CCA v1.1.0 is:
- Fully open source (MIT license)
- Audited by OpenZeppelin & Spearbit (Jan 2026)
- Deployed to canonical addresses across chains
- Bug bounty active

**Key Technical Insights from GitHub:**

1. **Factory Pattern**: 
   - ContinuousClearingAuctionFactory deploys auction instances
   - Canonical address: 0xCCccCcCAE7503Cac057829BF2811De42E16e0bD5

2. **Integration with Liquidity Launcher**:
   - Designed to work with Uniswap's token distribution system
   - Seeds Uniswap v4 pools automatically

3. **Audit Coverage**:
   - Three independent audits (Spearbit, OpenZeppelin, ABDK)
   - Bug bounty via Cantina

**Immediate Research Actions:**
- [ ] Clone repo, read source code
- [ ] Study clearing price algorithm in Solidity
- [ ] Analyze gas costs in test suite
- [ ] Identify extension points for multi-pair

---

### gcVM: Garbled Circuits for Private EVM

**Discovery**: ePrint 2026/170 introduces gcVM — MPC via garbled circuits achieving ~500 cTPS.

**What Garbled Circuits Offer:**
- Alternative to FHE/threshold for confidential computation
- Generally faster than FHE but higher communication
- Publicly auditable execution

**Performance Claims:**
- Current: 83 confidential transactions per second
- Projected: ~500 cTPS with optimizations

**Comparison:**
| Approach | Performance | Communication | Trust Model |
|----------|-------------|---------------|-------------|
| Threshold (BEAST-MEV) | High | O(1) per server | t-of-n honest |
| Garbled Circuits (gcVM) | 500 cTPS | O(circuit_size) | Two-party |
| FHE (Fhenix) | Low (improving) | Low | Zero trust |
| MPC (Arcium) | Medium | O(n) | Honest majority |

**Relevance**: gcVM might be good for specific high-value, low-volume use cases (NFT auctions, cross-chain bridges).

---

### Academic Validation: FBA Welfare Analysis

**Discovery**: arXiv 2302.01177 provides formal economic analysis of FBA for DEX.

**Key Finding**:
> FBA (Frequent Batch Auctions) reduces welfare loss compared to continuous matching in the presence of MEV.

**Why This Matters:**
- Peer-reviewed academic support for our approach
- Formal model we can cite in our specification
- Identifies specific conditions where FBA dominates

**Paper Structure:**
1. Model DEX with order book + MEV extractors
2. Compare continuous vs discrete (batch) matching
3. Prove welfare improvement under specific conditions

**Action**: Deep-read for formal model; may adopt their welfare definitions.

---

## 🆕 New Insight: Encryption Technology Landscape Diversifying

### Observation (Feb 2026)

The encrypted computation space is rapidly diversifying:

| Technology | Project | Chain | Status |
|------------|---------|-------|--------|
| Threshold | BEAST-MEV, Shutter | Ethereum | Research → Production |
| MPC | Arcium | Solana | Mainnet Alpha |
| FHE | Fhenix | EVM | Research (DBFV) |
| Garbled | gcVM | EVM | Research |
| WE | 2026/175 | Any | Early research |
| TEE | SUAVE | Ethereum | Development |

### Implication: Technology-Agnostic Design

Our clearing layer should be **encryption-agnostic**:

```
┌─────────────────────────────────────────────────┐
│  Clearing Layer (OUR FOCUS)                     │
│  Input: Decrypted orders OR encrypted orders    │
│  Output: Clearing price + fills                 │
├─────────────┬─────────────┬─────────────────────┤
│  Threshold  │  FHE        │  MPC / GC / WE      │
│  (decrypt   │  (compute   │  (various)          │
│   first)    │   encrypted)│                     │
└─────────────┴─────────────┴─────────────────────┘
```

For near-term: Build on threshold (BEAST-MEV/EIP-8105)
For future: FHE integration when mature (enables compute-on-encrypted)

---

## Updated Research Priorities (Feb 7, 5PM)

### Immediate (Next 24 Hours)
- [x] Daily literature search ✅ (completed this cron)
- [x] Update INDEX.md ✅
- [x] Update IDEAS.md ✅
- [ ] Study Uniswap CCA source code (now that repo is found)

### Short-term (Feb 8-14)
- [ ] Clone and analyze Uniswap CCA repo
- [ ] Reverse-engineer clearing algorithm from Solidity
- [ ] Benchmark gas costs from test suite
- [ ] Study Arcium/Umbra as reference for private DEX UX
- [ ] Read DBFV paper when available (or contact Fhenix team)

### Medium-term (Feb 2026)
- [ ] Design encryption-agnostic clearing interface
- [ ] Prototype integration with CCA contracts
- [ ] Explore FHE clearing path as future direction

---

## Update Log (continued)
- [2026-02-07 5PM] **5PM Cron Update**: Major new discoveries
  - Arcium Mainnet Alpha: MPC alternative on Solana (production)
  - Fhenix DBFV: FHE breakthrough (noise management solved)
  - Uniswap CCA v1.1.0: Production code available, audited
  - gcVM: Garbled circuits for private EVM (~500 cTPS)
  - arXiv FBA welfare paper: Academic validation of batch auctions
- [2026-02-07 5PM] New insight: Encryption technology diversifying rapidly
- [2026-02-07 5PM] Design principle: Build encryption-agnostic clearing layer
3. **Agent support**: How important is KYA/agent-signing in initial design?
4. **Timeline**: Hegotá is late 2026/2027 — aim for Glamsterdam compatibility first?
