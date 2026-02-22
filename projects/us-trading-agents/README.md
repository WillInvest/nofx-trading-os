# US Stock Trading Agents

**Multi-Agent LLM Financial Trading System for US Markets**

Based on [TradingAgents](https://github.com/TauricResearch/TradingAgents) framework by Tauric Research.

## Project Goal

Implement a production-ready multi-agent LLM trading system for US stock market that:
1. Mirrors real-world trading firm dynamics with specialized agents
2. Supports multiple LLM providers (OpenAI, Anthropic, local Ollama)
3. Integrates with free/low-cost US market data sources
4. Provides backtesting and paper trading capabilities
5. Enables live signal generation (not automated execution initially)

## Quick Start

```bash
cd projects/us-trading-agents
conda activate d2l  # or create new env
pip install -r requirements.txt
python -m src.main --ticker AAPL --date 2026-02-15
```

## Project Status

- [ ] Phase 1: Foundation (Week 1-2)
- [ ] Phase 2: Core Agents (Week 3-4)
- [ ] Phase 3: Integration (Week 5-6)
- [ ] Phase 4: Testing & Optimization (Week 7-8)

See [PLAN.md](docs/PLAN.md) for detailed roadmap.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Data Sources Layer                          │
│  yfinance | Finnhub | Alpha Vantage | Reddit | News APIs        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Analyst Team                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │Fundamental│ │Sentiment │ │Technical │ │  News    │           │
│  │ Analyst  │ │ Analyst  │ │ Analyst  │ │ Analyst  │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Research Team (Debate)                        │
│           ┌──────────┐         ┌──────────┐                     │
│           │  BULL    │◄───────►│  BEAR    │                     │
│           │Researcher│  Debate │Researcher│                     │
│           └──────────┘         └──────────┘                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Trader Agent                               │
│              Synthesizes reports → Trading Decision              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Risk Management Team                           │
│        ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│        │  Risky   │ │ Neutral  │ │  Safe    │                   │
│        │ Manager  │ │ Manager  │ │ Manager  │                   │
│        └──────────┘ └──────────┘ └──────────┘                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Portfolio Manager                            │
│              Final Approval → Execute/Reject                     │
└─────────────────────────────────────────────────────────────────┘
```

## Related Projects

- [TradingAgents](https://github.com/TauricResearch/TradingAgents) - Original framework
- [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) - AI Agent for Finance
- [FinGPT](https://github.com/AI4Finance-Foundation/FinGPT) - Financial LLMs
- [FinMem](https://github.com/pipiku915/FinMem-LLM-StockTrading) - Memory-enhanced trading

## License

MIT (for our additions) | Original TradingAgents license applies to forked code
