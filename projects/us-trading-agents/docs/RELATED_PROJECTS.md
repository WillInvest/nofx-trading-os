# Related Projects & Tools Research

## Official TradingAgents

### TauricResearch/TradingAgents
- **URL:** https://github.com/TauricResearch/TradingAgents
- **Status:** Actively maintained, v0.2.0 (Feb 2026)
- **Features:**
  - Multi-provider LLM support (OpenAI, Anthropic, Google, xAI, Ollama)
  - LangGraph-based workflow
  - CLI interface
  - Configurable debate rounds
- **Install:**
  ```bash
  git clone https://github.com/TauricResearch/TradingAgents.git
  cd TradingAgents
  pip install -r requirements.txt
  ```

---

## Similar Multi-Agent Trading Systems

### 1. TradingGoose
- **URL:** https://github.com/TradingGoose/TradingGoose.github.io
- **Based on:** TradingAgents
- **Added Features:**
  - Portfolio management
  - Individual stock + portfolio analysis
- **Best for:** Multi-stock portfolio optimization

### 2. FinRobot (AI4Finance)
- **URL:** https://github.com/AI4Finance-Foundation/FinRobot
- **Stars:** 1.5k+
- **Key Features:**
  - SEC filings integration
  - Multiple data sources (Finnhub, FinnLp, FMP, yfinance)
  - Charting and reporting
  - Quantitative analysis tools
- **Structure:**
  ```
  finrobot/
  ├── agents/         # Agent definitions
  ├── data_source/    # API integrations
  ├── functional/     # Analysis tools
  └── toolkits.py     # Utility functions
  ```

### 3. FinMem-LLM-StockTrading
- **URL:** https://github.com/pipiku915/FinMem-LLM-StockTrading
- **Paper:** FinMem: A Performance-Enhanced LLM Trading Agent
- **Key Innovation:** Layered memory system
  - Working memory (short-term)
  - Episodic memory (experiences)
  - Semantic memory (knowledge)
- **Best for:** Understanding memory-augmented trading

### 4. StockAgent
- **URL:** https://github.com/MingyuJ666/Stockagent
- **Key Feature:** Avoids test set leakage
- **Best for:** Fair backtesting without lookahead bias

### 5. PrimoAgent
- **URL:** https://github.com/ivebotunac/PrimoAgent
- **Features:**
  - 4 specialized agents
  - 7 quantified NLP features for news
  - Built-in backtesting with `bt` library
  - LangGraph workflow
- **Structure:**
  ```
  src/
  ├── agents/          # Four specialized agents
  ├── backtesting/     # Backtest engine
  ├── prompts/         # LLM prompt templates
  ├── tools/           # External API integrations
  └── workflows/       # LangGraph state management
  ```

### 6. langchain-trading-analysis
- **URL:** https://github.com/anandsinh01/langchain-trading-analysis
- **Stack:** LangChain + LangGraph + LangSmith
- **Best for:** Understanding LangChain integration

### 7. stocks-insights-ai-agent
- **URL:** https://github.com/vinay-gatech/stocks-insights-ai-agent
- **Features:** Full-stack application with frontend
- **Best for:** UI/UX reference

---

## AI4Finance Foundation Projects

### FinRL (Reinforcement Learning)
- **URL:** https://github.com/AI4Finance-Foundation/FinRL
- **Stars:** 10k+
- **Features:**
  - RL-based trading agents
  - Multiple environments (stocks, crypto, forex)
  - PPO, A2C, DDPG algorithms
- **Use Case:** RL-based strategy development

### FinRL-Trading
- **URL:** https://github.com/AI4Finance-Foundation/FinRL-Trading
- **Features:**
  - Production-ready trading
  - Multi-source data (Yahoo/FMP/WRDS)
  - SQLite persistence
  - Professional backtesting with `bt` library

### FinGPT
- **URL:** https://github.com/AI4Finance-Foundation/FinGPT
- **HuggingFace:** https://huggingface.co/FinGPT
- **Features:**
  - Pre-trained financial LLMs
  - Sentiment analysis models
  - Fine-tuning pipelines
- **Models Available:**
  - FinGPT-Llama (sentiment)
  - FinGPT-ChatGLM
  - FinGPT-Falcon

---

## Data Source APIs

### Free Tier Options

| API | Data | Rate Limit | Key Features |
|-----|------|------------|--------------|
| **yfinance** | Price, Fundamentals | Unofficial, no limit | Easy, comprehensive |
| **Finnhub** | News, Sentiment, Insider | 60/min free | Best free news API |
| **Alpha Vantage** | Technical Indicators | 25/day free | 50+ indicators |
| **Polygon.io** | Real-time quotes | Limited free | Best for real-time |
| **Alpaca** | Trading + Data | Free | Paper trading |
| **Twelve Data** | Global stocks | 800/day free | Good technical data |

### Python Libraries

```python
# Core data libraries
yfinance          # Yahoo Finance wrapper
finnhub-python    # Finnhub API client
alpha_vantage     # Alpha Vantage client
polygon           # Polygon.io client
alpaca-trade-api  # Alpaca Markets

# Technical analysis
ta                # Technical analysis library
ta-lib            # TA-Lib Python wrapper
pandas_ta         # Pandas TA indicators

# ML/NLP
transformers      # HuggingFace models
finbert-embedding # Financial BERT
vaderSentiment    # Sentiment analysis
```

---

## OpenClaw/ClawHub Skills

### Trading-Related Skills (Use with Caution)
⚠️ **Warning:** Recent security research found malicious skills on ClawHub. Only use verified skills.

**Potentially Useful (Verify First):**
- `openclaw-trading-assistant` by molt-bot
- Market data fetching skills
- Technical analysis skills

**Recommendation:** Build custom skills rather than relying on unverified third-party skills.

---

## Key Papers to Read

1. **TradingAgents** (Xiao et al., 2024)
   - arXiv:2412.20138
   - Core framework paper

2. **FinMem** (Yu et al., 2023)
   - arXiv:2311.13743
   - Layered memory for trading

3. **FinGPT** (Yang et al., 2023)
   - arXiv:2306.06031
   - Open-source financial LLMs

4. **QuantAgent** (Wang et al., 2023)
   - Alpha mining with inner/outer loops

5. **AlphaGPT** (Wang et al., 2023)
   - Human-in-the-loop alpha mining

---

## Implementation Recommendations

### Phase 1: Start Simple
1. Clone TradingAgents, run demo
2. Use yfinance + Finnhub (free)
3. Test with Ollama (local, free)

### Phase 2: Add Components
1. Integrate FinRobot's data sources
2. Add FinMem's memory system
3. Use FinGPT models for sentiment

### Phase 3: Optimize
1. Backtest with PrimoAgent's engine
2. Fine-tune prompts iteratively
3. A/B test LLM providers

### Phase 4: Production
1. Paper trade for 1+ month
2. Monitor and adjust
3. Consider Alpaca for execution

---

## Useful Tutorials & Resources

1. **AWS Blog:** Build financial agent with LangGraph
   - https://aws.amazon.com/blogs/machine-learning/build-an-intelligent-financial-analysis-agent

2. **Analytics Vidhya:** Multi-Agent Financial Analysis
   - https://www.analyticsvidhya.com/blog/2025/02/financial-market-analysis-ai-agent/

3. **Medium:** Multi-Agent Hedge Fund Simulation
   - https://shaikhmubin.medium.com/multi-agent-hedge-fund-simulation-with-langchain-and-langgraph

4. **CopilotKit:** Stock Portfolio Agent with LangGraph
   - https://www.copilotkit.ai/blog/build-a-fullstack-stock-portfolio-agent

---

*Compiled: 2026-02-15*
