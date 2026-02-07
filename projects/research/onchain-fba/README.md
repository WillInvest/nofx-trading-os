# On-Chain Trustless FBA for AMM Front-Running Protection

## Problem Statement

AMM (Automated Market Maker) traders face front-running and MEV (Maximal Extractable Value) extraction risks. Current solutions have trust issues:

1. **Flashbots / Private RPCs** — Requires trusting the relay/builder not to leak orders
2. **Off-chain FBA (CoW Protocol)** — Requires trusting the solver network
3. **Both violate blockchain's trustless ethos** — If you must trust a third party, why use blockchain?

## Research Goal

Design a **fully on-chain, trustless Frequent Batch Auction (FBA)** mechanism that:
- Eliminates front-running without requiring trust in any centralized party
- Maintains reasonable gas efficiency
- Provides provable fairness guarantees
- Can be practically implemented on existing EVM chains

## Key Research Questions

1. **Commitment Schemes**: Can commit-reveal or threshold encryption enable trustless order hiding?
2. **Batch Timing**: How to coordinate batch boundaries without a trusted sequencer?
3. **Price Discovery**: How to determine uniform clearing price on-chain efficiently?
4. **MEV Resistance**: Can the mechanism be MEV-proof even with public mempool?
5. **Liveness**: How to ensure batches always clear even under adversarial conditions?
6. **Composability**: Can this integrate with existing DeFi protocols?

## Approach

Following the research skill framework:
1. Literature review of existing academic and industry solutions
2. Theoretical synthesis and novel mechanism design
3. Smart contract implementation and testing

## Current Status

**Phase**: Initial literature collection

## Timeline

- Week 1: Comprehensive literature review
- Week 2-3: Theoretical framework development
- Week 4+: Prototype implementation

## Related Work Categories

- Batch auctions (traditional finance + crypto)
- Commit-reveal schemes
- Threshold cryptography
- MEV mitigation strategies
- Order flow auctions
- Encrypted mempools
- Fair ordering protocols
