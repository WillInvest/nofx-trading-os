# AMM Long-Term Fee Revenue Research

## Overview

Research project investigating the long-term fee revenue dynamics for Liquidity Providers (LPs) in Automated Market Makers (AMMs). Understanding how LP fee revenue accumulates, compounds, and behaves over extended time horizons.

## Research Questions

### Primary Question
What are the key factors that determine long-term fee revenue sustainability and growth for AMM liquidity providers?

### Sub-Questions
1. How does fee revenue compound over time for passive LPs?
2. What is the relationship between trading volume volatility and long-term LP returns?
3. How do fee revenue patterns differ across different AMM designs (Uniswap v2/v3, Curve, Balancer)?
4. What is the impact of impermanent loss on net long-term returns?
5. How does concentrated liquidity (v3-style) affect long-term fee capture?
6. What strategies optimize long-term LP fee revenue?
7. How do gas costs and rebalancing frequency affect net returns?

## Hypothesis

Long-term LP profitability depends on:
- **Volume consistency**: Sustained trading volume over time
- **Fee tier selection**: Matching fee tier to asset volatility
- **IL management**: Strategies to minimize impermanent loss drag
- **Compounding effects**: Reinvestment of fees back into positions
- **Market regime**: Bull/bear/sideways markets have different LP dynamics

## Status

🟡 **Phase 1: Literature Review** — Initial setup

## Related Projects
- [AMM LVR Research](../amm-lvr/) — Understanding LP losses from arbitrage
- [Output-Fee AMM](../output-fee-amm/) — Alternative fee structures
- [On-Chain FBA](../onchain-fba/) — MEV protection mechanisms
