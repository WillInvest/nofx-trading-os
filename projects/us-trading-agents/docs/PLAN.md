# US Trading Agents - Comprehensive Implementation Plan

## Executive Summary

This project implements a multi-agent LLM trading system for US stock markets, inspired by TradingAgents (Xiao et al., 2024). The system deploys specialized AI agents that collaborate like a real trading firm to analyze markets and generate trading signals.

**Target Outcome:** A working system that can:
1. Analyze any US stock ticker using multiple data sources
2. Generate buy/sell/hold recommendations with confidence scores
3. Backtest strategies on historical data
4. Run paper trading simulations
5. Provide explainable, auditable decision trails

---

## Phase 1: Foundation (Week 1-2)

### 1.1 Environment Setup

```bash
# Create dedicated environment
conda create -n trading-agents python=3.11
conda activate trading-agents

# Core dependencies
pip install langchain langgraph langchain-openai langchain-anthropic
pip install yfinance finnhub-python alpha_vantage
pip install pandas numpy scipy ta-lib
pip install pydantic python-dotenv rich typer
pip install pytest pytest-asyncio httpx
```

### 1.2 Data Sources Integration

| Source | Data Type | Cost | Rate Limit | Priority |
|--------|-----------|------|------------|----------|
| **yfinance** | Price, Fundamentals | Free | Unofficial | P0 |
| **Finnhub** | News, Sentiment, Insider | Free tier: 60/min | 60/min | P0 |
| **Alpha Vantage** | Technical Indicators | Free: 25/day | 5/min | P1 |
| **Reddit API** | Social Sentiment | Free | 100/min | P1 |
| **Polygon.io** | Real-time quotes | $29/mo | Generous | P2 |
| **SEC EDGAR** | Filings | Free | 10/sec | P2 |

**Week 1 Deliverables:**
- [ ] `src/data/yfinance_client.py` - Price & fundamentals
- [ ] `src/data/finnhub_client.py` - News & sentiment
- [ ] `src/data/technical_indicators.py` - 60 standard indicators
- [ ] `src/data/data_aggregator.py` - Unified data interface

### 1.3 Configuration System

```python
# config/default_config.py
DEFAULT_CONFIG = {
    # LLM Settings
    "llm_provider": "ollama",  # ollama, openai, anthropic
    "deep_think_llm": "llama3.3:70b",  # Complex reasoning
    "quick_think_llm": "llama3.2:8b",  # Fast tasks
    
    # Agent Settings
    "max_debate_rounds": 3,
    "risk_tolerance": "moderate",  # conservative, moderate, aggressive
    
    # Data Settings
    "lookback_days": 30,
    "news_lookback_hours": 72,
    
    # Trading Settings
    "initial_capital": 100000,
    "max_position_pct": 0.20,  # Max 20% in single stock
    "stop_loss_pct": 0.05,
}
```

---

## Phase 2: Core Agents (Week 3-4)

### 2.1 Agent Architecture

Each agent follows this pattern:
```
┌─────────────────────────────────────────┐
│              Agent Base                  │
├─────────────────────────────────────────┤
│ - llm: BaseLLM                          │
│ - tools: List[Tool]                      │
│ - prompt_template: str                   │
│ - output_parser: OutputParser           │
├─────────────────────────────────────────┤
│ + analyze(context) -> Report            │
│ + get_tools() -> List[Tool]             │
└─────────────────────────────────────────┘
```

### 2.2 Analyst Agents

#### 2.2.1 Fundamental Analyst
**Purpose:** Evaluate company financials and intrinsic value

**Data Inputs:**
- Balance sheet, Income statement, Cash flow
- P/E, P/B, EV/EBITDA, Debt/Equity ratios
- Revenue growth, Profit margins
- Analyst estimates and targets

**Output Format:**
```json
{
  "ticker": "AAPL",
  "analysis_type": "fundamental",
  "rating": "bullish",
  "confidence": 0.75,
  "key_metrics": {
    "pe_ratio": 28.5,
    "pe_vs_sector": "above_average",
    "revenue_growth_yoy": 0.08,
    "profit_margin": 0.25
  },
  "strengths": ["Strong cash position", "Growing services revenue"],
  "weaknesses": ["iPhone growth slowing", "China exposure"],
  "fair_value_estimate": 195.00,
  "reasoning": "..."
}
```

#### 2.2.2 Sentiment Analyst
**Purpose:** Gauge market mood from social media and news

**Data Inputs:**
- Reddit posts (r/wallstreetbets, r/stocks, r/investing)
- Twitter/X sentiment
- News article sentiment scores
- Insider trading activity

**Output Format:**
```json
{
  "ticker": "AAPL",
  "analysis_type": "sentiment",
  "overall_sentiment": 0.65,  // -1 to 1
  "sentiment_trend": "improving",
  "social_volume": "high",
  "news_sentiment": 0.45,
  "insider_activity": "net_buying",
  "key_narratives": ["AI integration", "Vision Pro launch"],
  "risk_flags": ["Short interest increasing"]
}
```

#### 2.2.3 Technical Analyst
**Purpose:** Identify patterns and price trends

**Data Inputs:**
- OHLCV data (daily, weekly)
- 60 technical indicators (MACD, RSI, Bollinger, etc.)
- Support/resistance levels
- Volume analysis

**Output Format:**
```json
{
  "ticker": "AAPL",
  "analysis_type": "technical",
  "trend": "bullish",
  "trend_strength": 0.7,
  "indicators": {
    "rsi_14": 58,
    "macd_signal": "bullish_crossover",
    "sma_50_200": "golden_cross",
    "bollinger_position": "middle"
  },
  "support_levels": [175.00, 170.00, 165.00],
  "resistance_levels": [185.00, 190.00, 195.00],
  "patterns_detected": ["ascending_triangle"],
  "entry_suggestion": 178.50,
  "stop_loss": 172.00
}
```

#### 2.2.4 News Analyst
**Purpose:** Monitor macro events and company news

**Data Inputs:**
- Bloomberg/Reuters headlines
- SEC filings (8-K, 10-K, 10-Q)
- Earnings announcements
- Macro economic data

**Output Format:**
```json
{
  "ticker": "AAPL",
  "analysis_type": "news",
  "recent_events": [
    {"date": "2026-02-14", "event": "Q1 Earnings Beat", "impact": "positive"},
    {"date": "2026-02-10", "event": "EU DMA Compliance", "impact": "negative"}
  ],
  "upcoming_events": [
    {"date": "2026-03-15", "event": "Product Launch Event"}
  ],
  "macro_factors": {
    "fed_stance": "hawkish",
    "sector_rotation": "into_tech"
  },
  "news_impact_score": 0.6
}
```

### 2.3 Research Team (Debate Agents)

#### Bull Researcher
- Advocates for bullish positions
- Highlights growth catalysts
- Challenges bear arguments

#### Bear Researcher
- Advocates for caution/bearish positions
- Highlights risks and headwinds
- Challenges bull arguments

**Debate Protocol:**
```
Round 1: Initial positions based on analyst reports
Round 2: Counter-arguments and rebuttals
Round 3: Final synthesis and position strength
```

### 2.4 Trader Agent

**Purpose:** Synthesize all inputs into trading decision

**Decision Framework:**
```python
class TradingDecision:
    action: Literal["BUY", "SELL", "HOLD"]
    ticker: str
    confidence: float  # 0-1
    position_size: float  # % of portfolio
    entry_price: Optional[float]
    stop_loss: Optional[float]
    take_profit: Optional[float]
    time_horizon: Literal["day", "swing", "position"]
    reasoning: str
    dissenting_views: List[str]
```

### 2.5 Risk Management Team

**Three Personas:**
1. **Aggressive Manager:** Maximizes returns, higher risk tolerance
2. **Neutral Manager:** Balanced risk-reward
3. **Conservative Manager:** Capital preservation priority

**Risk Checks:**
- Position size limits
- Sector concentration
- Correlation analysis
- VaR/CVaR calculations
- Drawdown limits

### 2.6 Portfolio Manager

**Final Authority:**
- Approves/rejects proposed trades
- Enforces portfolio constraints
- Maintains audit trail
- Generates execution instructions

---

## Phase 3: Integration (Week 5-6)

### 3.1 LangGraph Workflow

```python
from langgraph.graph import StateGraph

class TradingState(TypedDict):
    ticker: str
    date: str
    market_data: Dict
    analyst_reports: List[Report]
    debate_transcript: str
    trader_decision: TradingDecision
    risk_assessment: RiskReport
    final_decision: FinalDecision

def build_trading_graph():
    workflow = StateGraph(TradingState)
    
    # Add nodes
    workflow.add_node("fetch_data", fetch_market_data)
    workflow.add_node("fundamental_analysis", run_fundamental)
    workflow.add_node("sentiment_analysis", run_sentiment)
    workflow.add_node("technical_analysis", run_technical)
    workflow.add_node("news_analysis", run_news)
    workflow.add_node("bull_research", run_bull)
    workflow.add_node("bear_research", run_bear)
    workflow.add_node("debate", run_debate)
    workflow.add_node("trader", make_decision)
    workflow.add_node("risk_management", assess_risk)
    workflow.add_node("portfolio_manager", final_approval)
    
    # Define edges (parallel where possible)
    workflow.add_edge("fetch_data", "fundamental_analysis")
    workflow.add_edge("fetch_data", "sentiment_analysis")
    workflow.add_edge("fetch_data", "technical_analysis")
    workflow.add_edge("fetch_data", "news_analysis")
    # ... continue
    
    return workflow.compile()
```

### 3.2 Communication Protocol

Agents communicate via structured reports, not raw chat:

```python
class AgentReport(BaseModel):
    agent_type: str
    ticker: str
    timestamp: datetime
    analysis: Dict[str, Any]
    confidence: float
    key_points: List[str]
    risks: List[str]
    recommendation: str
```

### 3.3 Multi-Provider LLM Support

```python
def get_llm(provider: str, model: str, task_type: str):
    """Factory for LLM instances."""
    if provider == "ollama":
        return ChatOllama(model=model)
    elif provider == "openai":
        return ChatOpenAI(model=model)
    elif provider == "anthropic":
        return ChatAnthropic(model=model)
```

---

## Phase 4: Testing & Optimization (Week 7-8)

### 4.1 Backtesting Framework

```python
class Backtester:
    def __init__(self, strategy, start_date, end_date, initial_capital):
        self.strategy = strategy
        self.portfolio = Portfolio(initial_capital)
        
    def run(self, tickers: List[str]) -> BacktestResult:
        for date in self.trading_days:
            for ticker in tickers:
                decision = self.strategy.decide(ticker, date)
                self.portfolio.execute(decision)
        return self.calculate_metrics()
    
    def calculate_metrics(self) -> BacktestResult:
        return BacktestResult(
            total_return=...,
            annualized_return=...,
            sharpe_ratio=...,
            max_drawdown=...,
            win_rate=...,
            profit_factor=...
        )
```

### 4.2 Evaluation Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Cumulative Return | (Final - Initial) / Initial | > 20% annually |
| Sharpe Ratio | (Return - Risk-free) / Std | > 1.5 |
| Max Drawdown | Max peak-to-trough loss | < 15% |
| Win Rate | Profitable trades / Total | > 55% |
| Profit Factor | Gross profit / Gross loss | > 1.5 |

### 4.3 A/B Testing

Test different configurations:
- LLM models (GPT-4 vs Claude vs Llama)
- Debate rounds (1 vs 3 vs 5)
- Risk personas weightings
- Technical indicator sets

---

## Phase 5: Production Deployment (Week 9+)

### 5.1 Paper Trading Mode

```python
class PaperTrader:
    """Simulated trading with real-time data."""
    
    def __init__(self, initial_capital: float):
        self.portfolio = Portfolio(initial_capital)
        self.orders = []
        
    async def run_daily(self, watchlist: List[str]):
        for ticker in watchlist:
            decision = await self.system.analyze(ticker)
            if decision.action != "HOLD":
                self.execute_paper_trade(decision)
                self.notify_user(decision)
```

### 5.2 Signal Generation (Non-Automated)

Generate signals for manual execution:
```
📊 TRADING SIGNAL - 2026-02-15 09:30 EST

Ticker: AAPL
Action: BUY
Confidence: 78%
Entry Zone: $178.00 - $179.50
Stop Loss: $172.00 (-3.4%)
Take Profit: $190.00 (+6.2%)

Rationale:
- Fundamental: Strong Q1 earnings, services growth
- Technical: Golden cross, RSI neutral
- Sentiment: Positive social buzz, insider buying
- News: Product event catalyst upcoming

Risk Assessment: MODERATE
Position Size: 5% of portfolio
```

### 5.3 Monitoring & Alerts

- Daily portfolio summary
- Real-time signal notifications
- Risk threshold alerts
- Performance tracking dashboard

---

## Technology Stack

| Component | Technology | Reason |
|-----------|------------|--------|
| Orchestration | LangGraph | State management, parallel agents |
| LLMs | Ollama (default), OpenAI, Anthropic | Cost control, flexibility |
| Data | yfinance, Finnhub, Alpha Vantage | Free/cheap, reliable |
| Storage | SQLite / PostgreSQL | Local-first, scalable |
| UI | Streamlit / CLI | Quick iteration |
| Testing | pytest, pytest-asyncio | Async support |

---

## Related Projects & Resources

### Similar Implementations

| Project | Description | Key Features |
|---------|-------------|--------------|
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | Original paper implementation | LangGraph, multi-provider |
| [TradingGoose](https://github.com/TradingGoose/TradingGoose.github.io) | Fork with portfolio management | Enhanced risk management |
| [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) | AI4Finance agent platform | SEC integration, reporting |
| [FinMem](https://github.com/pipiku915/FinMem-LLM-StockTrading) | Memory-enhanced trading | Layered memory system |
| [StockAgent](https://github.com/MingyuJ666/Stockagent) | Simulated trading env | Avoids test leakage |
| [PrimoAgent](https://github.com/ivebotunac/PrimoAgent) | Multi-agent analysis | 7 NLP features, backtesting |

### Useful Skills/Tools to Explore

1. **OpenClaw Trading Assistant** - Pre-built trading skill
2. **FinGPT Models** - Fine-tuned financial LLMs on HuggingFace
3. **TA-Lib** - Technical analysis library
4. **Backtrader / bt** - Backtesting frameworks

### Papers to Read

1. TradingAgents (Xiao et al., 2024) - Core framework
2. FinMem (Yu et al., 2023) - Layered memory for trading
3. FinGPT (Yang et al., 2023) - Financial LLM fine-tuning
4. QuantAgent (Wang et al., 2023) - Alpha mining with LLMs

---

## Risk Disclaimer

⚠️ **This system is for research and educational purposes only.**

- Past performance does not guarantee future results
- AI decisions are not always accurate
- Never risk money you cannot afford to lose
- Always do your own research before trading
- This is NOT financial advice

---

## Timeline Summary

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1-2 | Foundation | Data sources, config, environment |
| 3-4 | Core Agents | All 4 analysts, debate team, trader |
| 5-6 | Integration | LangGraph workflow, communication |
| 7-8 | Testing | Backtesting, optimization, evaluation |
| 9+ | Production | Paper trading, signals, monitoring |

---

## Next Steps

1. **Immediate:** Clone TradingAgents, run demo
2. **This Week:** Set up data sources, test API limits
3. **Next Week:** Implement first analyst (Fundamental)
4. **Ongoing:** Iterate based on backtest results

---

*Last Updated: 2026-02-15*
*Author: OpenClaw Assistant*
