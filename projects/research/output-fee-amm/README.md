# Output-Asset AMM Fees Research

## Overview

Most AMMs (Uniswap, Curve, etc.) charge trading fees on the **input asset** — the token being sold. This project investigates an alternative: charging fees on the **output asset** — the token being bought.

## Research Questions

### Primary Question
What are the economic implications of using output assets instead of input assets as the fee source for LP revenue in AMMs?

### Sub-Questions
1. How does output-fee affect LP returns vs input-fee?
2. How does it change impermanent loss dynamics?
3. What is the impact on LVR (Loss-Versus-Rebalancing)?
4. How does it affect arbitrageur behavior?
5. Are there any existing implementations or proposals?
6. What are the trade-offs for different token pairs (stable/stable, ETH/stable, volatile/volatile)?

## Hypothesis

Output-asset fees may have different properties:
- **LP perspective**: Fees accumulate in the "desired" asset (what traders want)
- **Arbitrage**: May change when/how arbitrage is profitable
- **IL mitigation**: Could have different IL characteristics
- **LVR**: May affect information leakage differently

## Status

🟡 **Phase 1: Literature Review** — Initial comprehensive search

## Related Projects
- [AMM LVR Research](../amm-lvr/) — Understanding LP losses
- [On-Chain FBA](../onchain-fba/) — MEV protection via batch auctions
