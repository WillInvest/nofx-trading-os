# ETH Engine — Platform Redesign Blueprint

## Goal
Replace NOFX Go platform (10K+ lines) with ~800 lines of Python + simple dashboard.
ETH-only trading on Hyperliquid. Account ~$26.

## Architecture
```
collect-eth.sh → eth-brief.json → Opus cron reads → decision.json → executor.py → Hyperliquid
                                                                          ↓
                                                          dashboard (React SPA) ← position/balance API
```

## Dashboard (1 page)
```
┌─────────────────────────────────────┐
│  ETH Engine    $1,977.80  ▲         │
├─────────────────────────────────────┤
│  Balance: $26.22    PnL: -$0.12    │
│                                     │
│  ┌─ Position ────────────────────┐  │
│  │ LONG 0.013 ETH @ $1,987.60   │  │
│  │ PnL: -$0.12 (-0.46%)         │  │
│  │ SL: $1,948  TP: $2,030       │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌─ Opus Decision (4:00 PM) ─────┐  │
│  │ Strategy: Grid Trading        │  │
│  │ Confidence: 75%               │  │
│  │ Range: $1,895 - $2,055        │  │
│  │ "CVD +21k, buyers absorbing"  │  │
│  │ Next decision: 5:00 PM        │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌─ Recent Trades ───────────────┐  │
│  │ 3:42 PM  BUY  0.013 @ 1987.6 │  │
│  │ 3:15 PM  SELL 0.013 @ 1990.2 │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Phases
| Phase | What | Effort | Who |
|-------|------|--------|-----|
| 1. Executor | Python Hyperliquid executor (orders, grid, trailing stop) | 2-3 hours | MiniMax |
| 2. Data | Adapt collect-eth.sh + add Hyperliquid position/balance | 30 min | Opus |
| 3. Brain | Already done (cron + Opus) | ✅ Done | — |
| 4. Dashboard | Single-page React or static HTML | 1-2 hours | MiniMax |
| 5. Wire | Connect cron → data → Opus → executor → dashboard | 1 hour | Opus |
| 6. Kill NOFX | Stop NOFX containers, archive code | 10 min | Opus |

## Key Files
- Existing data collectors: workspace/projects/nofx-project/arena/
- Existing Go backend: workspace/projects/nofx-project/nofx/
- Hyperliquid API patterns: extracted from Go code
- New project home: workspace/projects/eth-engine/
