# Downloadable Resources & Skills

## GitHub Repositories to Clone

### Primary (Must Have)
```bash
# 1. TradingAgents - Core framework
git clone https://github.com/TauricResearch/TradingAgents.git

# 2. FinRobot - Data sources & toolkits
git clone https://github.com/AI4Finance-Foundation/FinRobot.git

# 3. FinGPT - Financial LLMs
git clone https://github.com/AI4Finance-Foundation/FinGPT.git
```

### Secondary (Good Reference)
```bash
# 4. FinMem - Memory-enhanced trading
git clone https://github.com/pipiku915/FinMem-LLM-StockTrading.git

# 5. PrimoAgent - Multi-agent with backtesting
git clone https://github.com/ivebotunac/PrimoAgent.git

# 6. FinRL - Reinforcement learning trading
git clone https://github.com/AI4Finance-Foundation/FinRL.git

# 7. Awesome AI in Finance - Curated list
git clone https://github.com/georgezouq/awesome-ai-in-finance.git
```

## HuggingFace Models

### Financial Sentiment Models
```python
# FinBERT - Financial sentiment analysis
from transformers import AutoModelForSequenceClassification, AutoTokenizer
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

# FinGPT Sentiment (Llama-based)
# https://huggingface.co/FinGPT/fingpt-sentiment_llama2-13b_lora
```

### Fine-tuned Financial LLMs
- `FinGPT/fingpt-mt_llama2-7b_lora` - Multi-task financial
- `FinGPT/fingpt-forecaster_dow30_llama2-7b_lora` - Stock forecasting
- `SALT-NLP/FLANG-BERT` - Financial language understanding

## Python Packages to Install

### Core Framework
```bash
pip install langchain langgraph langchain-openai langchain-anthropic
pip install langchain-community langsmith
```

### Data & Analysis
```bash
pip install yfinance finnhub-python alpha_vantage
pip install pandas numpy scipy
pip install ta pandas-ta  # Technical analysis
# pip install TA-Lib  # Requires system install first
```

### NLP & Sentiment
```bash
pip install transformers torch
pip install vaderSentiment textblob
pip install finbert-embedding  # Financial BERT embeddings
```

### Backtesting
```bash
pip install bt  # Backtesting framework
pip install backtrader  # Alternative
pip install quantstats  # Performance analysis
```

## API Keys Needed

### Free Tier Available
| Service | Get Key | Free Limits |
|---------|---------|-------------|
| Finnhub | https://finnhub.io/register | 60 calls/min |
| Alpha Vantage | https://www.alphavantage.co/support/#api-key | 25 calls/day |
| Polygon.io | https://polygon.io/dashboard/signup | 5 calls/min |
| NewsAPI | https://newsapi.org/register | 100 calls/day |

### For Production
| Service | Purpose | Cost |
|---------|---------|------|
| OpenAI | GPT-4 access | ~$0.03/1K tokens |
| Anthropic | Claude access | ~$0.015/1K tokens |
| Alpaca | Paper/Live trading | Free for paper |

## System Dependencies

### TA-Lib (Technical Analysis)
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# macOS
brew install ta-lib

# Then Python binding
pip install TA-Lib
```

### Ollama (Local LLMs)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull llama3.3:70b  # Deep thinking
ollama pull llama3.2:8b   # Quick thinking
```

## Configuration Templates

### .env Template
```bash
# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Data Sources
FINNHUB_API_KEY=...
ALPHA_VANTAGE_API_KEY=...
POLYGON_API_KEY=...
NEWSAPI_KEY=...

# Reddit (optional)
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USER_AGENT=trading-agent

# Trading (for live/paper trading)
ALPACA_API_KEY=...
ALPACA_SECRET_KEY=...
ALPACA_BASE_URL=https://paper-api.alpaca.markets  # Paper trading
```

## Useful Commands

### Test Data Access
```python
# Test yfinance
import yfinance as yf
aapl = yf.Ticker("AAPL")
print(aapl.info['currentPrice'])

# Test Finnhub
import finnhub
client = finnhub.Client(api_key="YOUR_KEY")
print(client.company_news('AAPL', _from="2026-02-01", to="2026-02-15"))

# Test Alpha Vantage
from alpha_vantage.techindicators import TechIndicators
ti = TechIndicators(key='YOUR_KEY')
data, meta = ti.get_rsi(symbol='AAPL')
print(data.head())
```

### Run TradingAgents Demo
```bash
cd TradingAgents
python -m cli.main
# Select ticker, date, and watch it run
```

## Verification Checklist

Before starting development:
- [ ] Python 3.11+ installed
- [ ] Conda environment created
- [ ] Ollama installed and models pulled
- [ ] API keys obtained and tested
- [ ] TradingAgents demo runs successfully
- [ ] yfinance fetches data correctly
- [ ] Finnhub API responds

---
*Last Updated: 2026-02-15*
