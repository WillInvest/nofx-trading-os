# MEMORY.md — Long-Term Memory

## Who I Am
- **Role**: Hedge Fund Portfolio Manager / Opus Decider for NOFX trading system
- **User**: Hao Fu, EST timezone, Telegram

## NOFX System Overview (v2 — Feb 21 evening)
- Crypto AI trading on Hyperliquid, account ~$26
- **ETH ONLY** — all other coins dropped to concentrate capital and analysis
- Architecture v2: Raw data → Opus reads directly → Opus decides → Fao executes
- NO more V3 debates — Opus sees all raw data (~3.4K tokens) and decides solo
- Evolving data collection: Opus can add new data sources each hour via data-requests.json
- Backend: Go, Docker (compose rebuilds from source)
- Cron: "ETH Opus Hourly" (0 9-23 * * *), daily/weekly/monthly reviews
- Port mapping: container 8080 → host 8090
- JWT secret used as raw bytes (NOT base64 decoded)

## Key Decisions
- **ETH only** — $26 is too small to spread across 10 coins
- **Opus direct** — no intermediate V3 debates, Opus reads raw data and decides
- **NO plain waiting** — always pick an active strategy
- **Available strategies**: grid_trading, funding_harvest, mean_reversion, breakout, open_long, open_short
- **Evolving data** — Opus can request new data sources each hour to improve confidence
- **Lite mode** for trader — tiny prompts, I do all analysis
- **Trader executes ONCE** per hour, not every 5 min

## Data Pipeline (v2)
- `collect-eth.sh` — runs on-chain + protocol + market collectors in ~30s
- Output: `eth-brief.json` (~13KB, ~3.4K tokens)
- Opus reads raw data directly, no V3 preprocessing
- `data-requests.json` — Opus-editable list of extra data to collect each hour

## Available Infrastructure
- i9-14900, RTX 4000 SFF Ada (20GB VRAM), 32GB RAM
- Brave API (not free, use sparingly)
- **ETH Erigon archive node** — fully synced, at hfu11@10.246.103.160 (SSH key configured), RPC localhost:8545, 13TB free
- Hyperliquid + Binance APIs (free, integrated — Binance geo-blocked, need VPN)
- Mullvad VPN account: 0618229008768044 (not set up yet, deprioritized)

## On-Chain Data System (Built Feb 20, 2026)
Three data collectors feeding into debate engine:

### 1. On-chain basics (ETH node, ~43s)
- Script: `/srv/ethnode/bin/onchain-collector.py`
- Output: `/srv/ethnode/output/onchain-hourly.json`
- Data: whale stablecoin flows to exchanges, ERC-20 whale transfers (>$100K), gas trends, exchange ETH reserves, USDT/USDC supply changes

### 2. Market data (free APIs, ~4.5s)
- Script: `/projects/nofx-project/arena/market-collector.py`
- Output: `/projects/nofx-project/arena/market-data-hourly.json`
- Data: funding rates, orderbook depth/imbalance, OI + velocity, CVD, Fear & Greed, Deribit ETH options (put/call ratio)

### 3. Protocol-specific (ETH node, ~10s)
- Script: `/srv/ethnode/bin/protocol-collector.py`
- Output: `/srv/ethnode/output/protocol-hourly.json`
- Data: Aave v3 utilization/rates (WETH/LINK/CRV/UNI), Curve 3pool balances, Uniswap V3 liquidity, Ethena USDe/sUSDe supply, Pendle token supply, ARB bridge ETH locked, LINK staking

### Pipeline
- `collect-all.sh` → SSHs to ETH node, runs both remote collectors, SCPs back, runs market collector, merges all
- `merge-data.py` → combines 3 JSONs + coin-profiles.json → `debate-context.json`
- Must copy to `nofx/data/arena/` for Docker container access
- API: `GET /api/arena/context` (JWT auth required)
- Total collection time: ~20 seconds, all free

### Coin Profiles
- File: `/projects/nofx-project/arena/coin-profiles.json`
- Per-coin: what_it_is, on_chain_relevance (how shared data relates to THIS coin), key_debate_angles
- Key insight: same data means different things per coin (Aave 93.8% utilization = bullish revenue for AAVE token, but liquidation risk for ETH)

## Go Backend Changes (Feb 20)
- `RunParallelScan` → fixed 10 ETH-edge coins (was dynamic OI top 10)
- `loadDebateContext()` → reads `/app/data/arena/debate-context.json`
- `BuildUserPromptForDebate()` → injects shared on-chain intelligence + per-coin context + coin profile
- `buildDebateSystemPrompt()` → tells debaters to reference on-chain metrics
- Frontend: "🔗 On-Chain" tab in ScanView showing shared + per-coin data
- PEPE → kPEPE mapping for Hyperliquid

## Agent Fleet (Feb 21)
- **MiniMax M2.5** (API): base=https://api.minimax.io/anthropic, model=MiniMax-M2.5, wrapper=bin/claude-minimax
- **Qwen3-30B-A3B** (local): ollama, free, ~30 tok/s, wrapper=bin/claude-local
- Dispatch: 🟢 Simple→Qwen3 🟡 Medium→MiniMax 🔴 Complex→ask Hao
- NEVER code as Opus without permission. NEVER fix bugs myself — dispatch to sub-agents.
- Agent Dashboard: /agents route in NOFX frontend, events at /api/agents/events

## First Test Debate (Feb 21 12:20am)
- 9/10 coins debated, PEPE failed (needs kPEPE mapping for CoinAnk)
- Debaters successfully reference on-chain data (Aave utilization, Curve stress, whale flows)
- Decision: WAIT — Extreme Fear + Aave liquidation risk

## Agent Fleet (Feb 21)
- **MiniMax M2.5** (API): base=https://api.minimax.io/anthropic, model=MiniMax-M2.5, wrapper=bin/claude-minimax
- **Qwen3-30B-A3B** (local): ollama, free, ~30 tok/s, wrapper=bin/claude-local
- Dispatch: 🟢 Simple→Qwen3 🟡 Medium→MiniMax 🔴 Complex→ask Hao
- NEVER code as Opus without permission. NEVER fix bugs myself — dispatch to sub-agents.
- Agent Dashboard: /agents route in NOFX frontend, events at /api/agents/events

## First Test Debate (Feb 21 12:20am)
- 9/10 coins debated, PEPE failed (needs kPEPE mapping for CoinAnk)
- Debaters successfully reference on-chain data (Aave utilization, Curve stress, whale flows)
- Decision: WAIT — Extreme Fear + Aave liquidation risk

## TODO / Next Steps
- Docker rebuild to deploy engine changes (V3×3 + R1 synthesis)
- Add mempool monitoring, Uniswap LP tracking, Aave health factors
- Set up Mullvad VPN for Binance liquidation data (when needed)

## Memory Routine
- Daily: save key conversations to memory/YYYY-MM-DD.md
- Every 1-3 days: prune old short-term memory
- Periodically: update this file with curated learnings
- Alert Hao if memory files grow too large
- Key reference: memory/2026-02-20-debater-data.md (detailed session notes)
