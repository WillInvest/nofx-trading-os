# AMM Loss-Versus-Rebalancing (LVR) Mitigation Research

## Project Goal

Design improved AMM mechanisms that mitigate **impermanent loss** (IL) and **loss-versus-rebalancing** (LVR) risk for liquidity providers, while maintaining capital efficiency and decentralization.

## Problem Statement

**Impermanent Loss (IL)**: When LP token value < holding the underlying assets due to price divergence.

**Loss-Versus-Rebalancing (LVR)**: Formalized by Milionis et al. (2022) — LPs systematically lose to arbitrageurs who have fresher price information. This is the continuous-time "cost of providing liquidity" that IL approximates discretely.

**Core issue**: CFMMs leak value to informed traders (arbitrageurs) who correct stale prices. LPs are always trading at "yesterday's prices" against counterparties with "today's prices."

## Research Questions

1. **Oracle Integration**: Can external price oracles reduce LVR by keeping AMM prices fresh?
2. **Dynamic Fees**: Can adaptive fee structures capture arbitrage value for LPs?
3. **Auction Mechanisms**: Can batch auctions or other order flow auctions reduce toxic flow?
4. **Hedging Instruments**: Can options/perpetuals provide LP hedging?
5. **Novel Curve Designs**: Are there bonding curve innovations that reduce LVR?
6. **Hybrid Models**: Can combining AMM with orderbook/RFQ reduce adverse selection?

## Key Metrics

- **LVR reduction** (% vs baseline Uniswap v2/v3)
- **Capital efficiency** (liquidity depth per $ TVL)
- **Decentralization** (trust assumptions, permissionlessness)
- **Complexity** (implementation difficulty, gas costs)
- **LP returns** (net APY after fees minus losses)

## Related Project

See `../onchain-fba/` for complementary research on protecting traders from MEV via trustless batch auctions.

## Status

**Phase**: Initial Literature Review
**Created**: 2026-02-04
