# Ideas — AMM LVR Mitigation

## Solution Landscape Overview

After comprehensive literature review, LVR mitigation approaches fall into **six main categories**:

```
                    LVR MITIGATION APPROACHES
                    ========================
                    
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. ELIMINATE SOURCE          2. CAPTURE VALUE                  │
│  ├─ Oracle pricing            ├─ Batch auctions (FM-AMM)        │
│  └─ Real-time feeds           ├─ MEV auctions (McAMM)           │
│                               └─ Harberger leases (am-AMM)      │
│                                                                 │
│  3. ADAPTIVE DEFENSE          4. EXTERNAL HEDGE                 │
│  ├─ Dynamic fees              ├─ Options/power perps            │
│  ├─ Threshold triggers        └─ Structured products            │
│  └─ Volatility-reactive                                        │
│                                                                 │
│  5. STRUCTURAL DESIGN         6. INSURANCE                      │
│  ├─ Directional LP            └─ BNT-style compensation         │
│  ├─ Concentrated ranges           (unsustainable!)              │
│  └─ Knockout positions                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Key Insight: The LVR Equation

From Milionis et al.:
```
LVR ≈ (σ²/8) × L × dt
```
Where:
- σ = volatility
- L = liquidity
- dt = time interval between price updates

**Implication**: To reduce LVR, you must either:
1. **Reduce σ exposure** (hedge, use stablecoin pairs)
2. **Update prices faster** (oracles, batching)
3. **Charge fees ≥ LVR** (dynamic fees)
4. **Capture arb value** (auctions)

---

## Promising Novel Combinations

### Idea 1: Oracle-Gated Batch Auctions
**Combine**: UAMM + FM-AMM

**Concept**: 
- Use oracle for continuous "indicative price"
- Run micro-batches (every ~12 seconds / 1 block)
- Only allow trades within oracle ± spread
- Surplus from batch → LPs

**Advantage**: Gets benefits of both — oracle prevents stale prices, batch captures remaining arbitrage

**Challenge**: Oracle latency still creates brief windows; complexity

### Idea 2: Volatility-Triggered Fee Regime
**From**: Campbell et al. (2025) optimal fees paper

**Concept**:
- Normal volatility: Low competitive fee (match CEX)
- High volatility: Spike fee dramatically (protect LPs)
- Threshold-based, not continuous (simpler to implement)

**Implementation**: Uniswap v4 hook with Chainlink volatility oracle or on-chain vol estimation

**Advantage**: Near-optimal with simple logic
**Challenge**: Defining thresholds; vol estimation lag

### Idea 3: JIT Liquidity Defense via am-AMM
**From**: Adams et al. (2024)

**Concept**: 
- Auction pool management rights
- Manager pays rent but captures arb
- Rent → LPs (replaces fee income)
- Manager has incentive to price accurately

**Novel twist**: Could combine with Angstrom-style ordering

### Idea 4: LP-Owned MEV Protection (Angstrom Model)
**From**: Sorella Labs

**Concept**:
- All trades in a block get same price
- Ordering doesn't matter → no sandwich possible
- LVR captured by LP collective
- Implemented as Uniswap v4 hook

**Key question**: Can this work for very high-volume pairs? Scaling limits?

### Idea 5: Perpetual-Hedged LP Vaults
**Combine**: Standard AMM LP + automatic perp hedging

**Concept**:
- Vault takes LP position
- Continuously delta-hedges with perps
- Gamma hedge with power perps / options
- User gets fee yield minus hedging cost

**Advantage**: Works with any AMM; doesn't require protocol changes
**Challenge**: Hedging costs may exceed fee income for high-vol pairs

---

## Unexplored Territory

### Threshold Encryption for Fair Ordering
**Connection to FBA research**: What if trades are encrypted until batch close?

- Traders submit encrypted orders
- Threshold decryption at batch boundary
- No one knows order content during batch → no frontrunning
- Combined with FM-AMM batch clearing

**Potential synergy**: Our FBA research could apply here!

### Prediction Market for LP Protection
**Concept**: Let market predict volatility; if high vol predicted, auto-raise fees

### Retroactive LVR Compensation
**Concept**: Measure actual LVR extracted per block; redistribute from protocol revenue

---

## Evaluation Framework

For any proposed solution, evaluate on:

| Criterion | Weight | Notes |
|-----------|--------|-------|
| LVR Reduction | 30% | Theoretical and empirical |
| Trust Assumptions | 25% | Oracles, sequencers, auctions |
| Capital Efficiency | 15% | Liquidity depth per TVL |
| Implementation Complexity | 15% | Smart contract, gas, UX |
| Composability | 10% | Works with existing DeFi |
| Production Readiness | 5% | Audits, mainnet testing |

---

## Most Promising Directions (Ranked)

1. **FM-AMM / CoW AMM Model**
   - Proven to eliminate LVR
   - Production-ready
   - Trust trade-off: solver network
   
2. **Angstrom/Hook-Based Protection**
   - Native to Uniswap ecosystem
   - Growing adoption
   - Needs scale testing
   
3. **Dynamic Fees + Oracle Hybrid**
   - Near-optimal theoretically
   - Uniswap v4 enables this
   - Sweet spot of simplicity vs effectiveness

4. **Threshold Encryption Batch**
   - Most trustless option
   - Not yet production-ready
   - Synergy with FBA research!

---

## Research Questions for This Project

1. **Can we design a fully trustless LVR mitigation mechanism?**
   - No oracle trust, no solver trust, no sequencer trust
   
2. **What is the minimum latency/batch size that still eliminates most LVR?**
   - Trade-off: shorter batches = better UX, but more LVR leakage
   
3. **Can dynamic fees alone achieve >90% LVR reduction?**
   - Without any external price information
   
4. **How do different approaches compose?**
   - Can you layer FM-AMM + dynamic fees + oracle backstop?

---

---

## New Insights (2026-02-07)

### From Herlihy (2026) — Defensive Rebalancing ⭐ MAJOR

This paper introduces a fundamentally new approach to LVR mitigation:

**Core concept**: Instead of individual CFMMs defending themselves, **coordinate across pools**.

**Key theorems**:
1. For any arbitrage-prone state, ∃ a rebalancing that improves some pools without hurting others
2. Arbitrage-free ⟺ Pareto efficient (under rebalancing moves)
3. Optimal rebalancing is convex optimization → unique, tractable solution

**Why this matters**:
- Current solutions (FM-AMM, Angstrom) focus on single-pool protection
- This suggests **multi-pool coordination** could be strictly better
- Mixed rebalancing can even "attack back" against CEXs and non-participants

**Idea 9: Coordinated CFMM Defense Coalition**
- Multiple pools form a "defense pact"
- Share liquidity via direct transfers to neutralize arbitrage
- Capture arbitrage from non-member pools and CEXs
- Implementation: Could work as a Uniswap v4 "meta-hook" or L2-native

**Idea 10: On-Chain Rebalancing DAO**
- Decentralized coordination mechanism
- Pools opt-in to rebalancing coalition
- Smart contract computes optimal rebalancing (convex solver on-chain?)
- Challenge: Gas costs, latency

**Connection to existing work**:
- FM-AMM: Single-pool batching → Multi-pool coordination
- Angstrom: Per-block same price → Per-block optimal rebalancing
- am-AMM: Auction manager → Rebalancing coordinator

### From L2 Sandwich Paper (2026) — Good News for Rollups

Private mempools make sandwiching unprofitable! Key findings:
- Without builder markets, attackers rely on probabilistic inclusion
- Median L2 sandwich return is **negative**
- Most "detected" sandwiches are false positives

**Implication for LVR research**:
- L2 deployment may inherently reduce LP costs
- Sequencer design matters more than AMM design for some MEV types
- Could combine L2 private mempool + FM-AMM batching for double protection

**Idea 11: L2-Native LVR-Resistant AMM**
- Deploy on rollup with private mempool (sandwich protection)
- Add FM-AMM-style batching (LVR protection)
- Dynamic fees as backup (volatility protection)
- Could achieve near-zero MEV/LVR without trust assumptions

### From Bartoletti et al. (2026) — Formal Verification

**Key finding**: With trading fees, **single large swap > split trades**

This has implications:
- Arbitrageurs should consolidate trades (already known empirically, now proven)
- LP fee revenue is sub-additive: many small trades ≠ one large trade in fee capture
- For dynamic fee design: fee calculation should account for expected trade size distribution

**Idea 6: Size-Dependent Dynamic Fees**
- Lower fees for small trades (retail, uninformed)
- Higher fees for large trades (likely informed/arb)
- Rationale: Large trades carry more information; should pay more
- Implementation: Fee tier based on trade size relative to pool depth

### From Volatility Buffering Paper (2026)

**Key finding**: V-S pools have natural "volatility buffering"

Implications for LPs:
1. **Pool selection matters**: V-S pools (e.g., ETH-USDC) are safer than V-V pools (e.g., ETH-BTC)
2. **IL has memory**: Autoregressive structure means recent IL predicts near-term IL
3. **Cross-market contagion**: Traditional finance volatility (VIX) affects crypto IL

**Idea 7: Volatility-Aware LP Vault**
- Monitor both CVI (crypto vol) and VIX/OVX (traditional vol)
- Auto-rebalance between V-S and V-V pools based on regime
- Withdraw from high-IL pools during volatility spikes
- Could use prediction markets for vol forecasting

**Idea 8: AR-Based Fee Adjustment**
- Since IL is autoregressive, high recent IL → expect more IL
- Auto-raise fees when pool has experienced elevated IL recently
- Self-adaptive without external oracle

### From Wu et al. (2025) & Sandmark Analysis — MEV Concentration ⭐ NEW

**Key finding**: ~90% of DEX arbitrage value extracted by just 3 entities (Wintermute, SCP, Kayle) in Q1 2025

**Implications**:
1. **MEV extraction is oligopolistic** — not a competitive market
2. Searcher-builder vertical integration concentrates power further
3. High barriers to entry for new MEV extractors

**Idea 12: Oligopoly-Aware LVR Estimation**
- Current LVR models assume competitive arbitrage
- With oligopolistic extractors, actual LVR may be lower than theoretical max
- But extractors may also collude or extract more efficiently
- Could empirically measure "realized LVR" vs theoretical LVR

**Idea 13: Direct LP ↔ Searcher Negotiation**
- If only 3 entities extract 90% of MEV, why not negotiate directly?
- LPs could auction exclusive pool access to searchers
- Similar to OFA (Order Flow Auctions) but pool-level
- Reduces intermediation; LPs capture more value

---

## Next Steps

1. Deep-read FM-AMM paper (Canidio & Fritsch 2023)
2. Study CoW AMM implementation on GitHub
3. Analyze Angstrom hook architecture
4. Model threshold-dynamic fee strategy
5. Explore encryption-based approaches (connect to FBA project)
6. **NEW**: Model size-dependent fee schedules
7. **NEW**: Backtest AR-based fee adjustment on historical data
8. **NEW**: Empirically compare realized vs theoretical LVR
9. **NEW**: Study CCA mechanism for lessons applicable to continuous trading

---

## New Insights (2026-02-07, Update #4)

### Uniswap CCA Validates Batch Auction Approach

Uniswap's Continuous Clearing Auctions (CCA) on Base provide real-world validation of FM-AMM principles, but for token launches rather than continuous trading:

**Mechanism comparison:**
| Aspect | FM-AMM (Trading) | CCA (Token Launch) |
|--------|------------------|-------------------|
| Use case | Ongoing swaps | Initial distribution |
| Batch duration | Per-block or custom | Multi-day (e.g., 5 days) |
| Price discovery | Arbitrageur competition | Bidder competition |
| Post-auction | Continuous trading | v4 pool auto-seeded |

**Key insight**: The Aztec case ($557M FDV, 16,700 participants) demonstrates that:
1. Users accept batch-based systems when fairness is clear
2. Automatic liquidity provisioning reduces friction
3. Block-by-block clearing creates smooth price discovery

**Idea 14: CCA-to-FM-AMM Pipeline**
- Launch tokens via CCA
- Transition to FM-AMM-style continuous trading post-launch
- Unified batch auction framework across token lifecycle
- Could reduce LVR from day 1 of a token's life

### Systemic Risk as LP Signal (from ASRI paper)

The ASRI paper's regime detection (Low/Moderate/Elevated risk) could inform LP strategies:

**Idea 15: Regime-Aware LP Positioning**
- Monitor ASRI or similar risk index
- In "Elevated" regime: raise fees, reduce liquidity depth, or exit positions
- In "Low" regime: normal operations
- Could automate via oracle + dynamic fee hook

### Attack Surface Awareness (from TxRay)

The TxRay paper's "Anyone-Can-Take" (ACT) taxonomy is relevant:
- LVR itself is a form of ACT opportunity — public state, deterministic pricing
- 92% of DeFi exploits are reconstructible from public data
- Implication: AMMs need proactive defense, not just reactive

**Connection**: Both LVR and exploits arise from deterministic, permissionless execution. FM-AMM/batching address LVR; could similar approaches help with exploit defense?
