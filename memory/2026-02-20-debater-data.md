# Debater Data Enrichment Plan — Feb 20, 2026

## Context
User (Hao) and I agreed debaters need more than just price + technical indicators.
This was discussed before a context compaction, reconstructed from ARCHITECTURE.md + this conversation.

## Agreed Data Sources to Add (beyond current klines/indicators/OI/fundflow)
1. Liquidation heatmaps — where clusters are, magnetic price targets
2. Orderbook depth / bid-ask imbalance
3. Funding rates — crowded trade detection
4. Whale wallet movements — on-chain, large transfers to/from exchanges
5. Macro context — Fed/CPI/FOMC, tariffs, regulatory events
6. Cross-coin correlation — BTC vs alts divergence
7. Volume profile — POC, value area
8. Social sentiment — Fear & Greed, CT buzz
9. Options data — max pain, put/call ratio, large OI strikes
10. Delta (CVD) — cumulative volume delta

## Available Resources
- **Brave API** — ready, NOT free, use sparingly
- **ETH node** — fully synced, on another server, Hao will give access
- **Hyperliquid API** — already integrated (free)
- **Binance API** — already integrated (free)

## ETH-Edge Coin List (confirmed)
Focus on coins where our ETH node gives alpha:
1. ETH — $1B OI, direct on-chain
2. AAVE — $27M OI, lending/liquidations
3. LINK — $21M OI, ERC-20 whale tracking
4. ZRO — $36M OI, LayerZero bridge flows
5. ENA — $14M OI, Ethena mint/burn
6. UNI — $14M OI, have uni-v3-data tool
7. PEPE — $12M OI, whale wallet tracking
8. CRV — $5.4M OI, Curve DEX on-chain
9. PENDLE — $4.6M OI, yield market
10. ARB — $3.7M OI, L2 bridge flows

Dropped: BTC (no ETH edge), SOL, HYPE, small random coins

## Key Architecture Decision: Shared On-Chain Intelligence Layer
On-chain data is NOT per-coin — it's a shared context for ALL debaters because protocols are interconnected:
- Aave liquidations → forced selling of ETH, LINK, CRV, UNI collateral
- Curve 3pool imbalance → stablecoin stress → risk-off for ALL coins
- USDe mint/burn → leverage demand → ALL coins
- Stablecoin exchange flows → buying/selling pressure → ALL coins
- Uniswap liquidity repositioning → ETH price direction → ALL coins
- ARB bridge flows → capital rotation → ecosystem health

Every debater sees the FULL on-chain picture. A bull arguing for PENDLE needs to know Aave utilization is spiking.

## VPN / Binance
- Mullvad account: 0618229008768044
- Not set up yet — Binance geo-blocked from our servers
- Deprioritized — on-chain data is the focus
- Revisit when we need Binance liquidation data

## Principles
- Cost-effective, reliable, sustainable, continuous
- Hourly data collection feeding into debates
- Opus (me) decides dynamically what data each debate gets
- Do it myself, only ask Hao if truly stuck

## Deployment Status (Feb 20, 2026 ~9pm)
All integration work COMPLETE:
- Backend: v17 (rebuilt from compose, includes on-chain data injection)
- Frontend: v12 (has On-Chain data tab)
- Docker compose rebuilds from source, not tagged images
- debate-context.json must be copied to nofx/data/arena/ for container access
- Path inside container: /app/data/arena/debate-context.json
- API: GET /api/arena/context (requires JWT auth)
- JWT secret is used as raw bytes, NOT base64 decoded
- Port mapping: 8080 internal → 8090 external

## Memory Management (new routine)
- Short-term memory: daily files (memory/YYYY-MM-DD.md) — replace after 1-3 days
- Long-term memory: MEMORY.md — curated, important decisions/context
- Back up key conversations so compaction doesn't lose important decisions
- Remind Hao to clean up if memory files get too large
