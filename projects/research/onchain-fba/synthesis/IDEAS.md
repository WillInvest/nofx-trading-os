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
