#!/usr/bin/env python3
"""
News Scraper Daemon - runs continuously, fetches every 10 minutes.
Maintains a 1-month rolling archive of all articles.

Usage: python3 news-scraper.py (runs as daemon)
       python3 news-scraper.py --run-once (single run)

Storage:
- news-archive.json — ALL articles from past 30 days
- news-summary.json — computed view for frontend
- news-history.json — headline hashes for dedup
"""

import json
import os
import sys
import time
import re
import hashlib
import signal
from datetime import datetime, timezone, timedelta
from pathlib import Path
from email.utils import parsedate_to_datetime
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import ssl

# ─── Config ───
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"
INTERVAL = 600  # 10 minutes in seconds
RUN_ONCE = "--run-once" in sys.argv

WORKING_DIR = Path(__file__).parent
OUTPUT_DIR = WORKING_DIR
ARCHIVE_FILE = OUTPUT_DIR / "news-archive.json"
SUMMARY_FILE = OUTPUT_DIR / "news-summary.json"
HISTORY_FILE = OUTPUT_DIR / "news-history.json"

# Copy to frontend data dir
FRONTEND_DATA_DIR = Path("/home/openclaw/.openclaw/workspace/projects/nofx-project/nofx/data/arena")
FRONTEND_SUMMARY_FILE = FRONTEND_DATA_DIR / "news-summary.json"

MAX_ARTICLES_PER_FEED = 20
SUMMARY_MAX_ITEMS = 15  # Max items to send to Gemma per batch

# SSL context
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# ─── RSS Sources ───
RSS_FEEDS = [
    {"name": "CoinDesk", "url": "https://www.coindesk.com/arc/outboundfeeds/rss"},
    {"name": "CoinTelegraph", "url": "https://cointelegraph.com/rss"},
    {"name": "The Block", "url": "https://www.theblock.co/rss.xml"},
    {"name": "Decrypt", "url": "https://decrypt.co/feed"},
    {"name": "CryptoSlate", "url": "https://cryptoslate.com/feed/"},
]

# Keywords for relevance scoring
RELEVANCE_KEYWORDS = [
    "ethereum", "eth", "ether", "vitalik", "erc-20", "defi", "aave", "uniswap",
    "lido", "staking", "layer 2", "l2", "arbitrum", "optimism", "base",
    "merge", "shanghai", "dencun", "blob", "gas fee", "validator",
    "sec", "regulation", "etf", "blackrock", "grayscale", "institutional",
    "whale", "liquidation", "funding rate", "open interest",
    "bitcoin", "btc", "crypto", "market", "fed", "interest rate",
    "hack", "exploit", "vulnerability", "rug pull",
    "hyperliquid", "perpetual", "futures", "options", "deribit",
]


def parse_rss_date(date_str):
    """Parse RSS date to ISO datetime."""
    if not date_str:
        return None
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.isoformat()
    except Exception:
        # Fallback: try common formats
        try:
            # Handle "Fri, 20 Feb 2026 12:15:07 +0000"
            dt = datetime.strptime(date_str.replace(" +0000", " UTC").replace(" -0500", " EST"), 
                                   "%a, %d %b %Y %H:%M:%S %Z")
            return dt.replace(tzinfo=timezone.utc).isoformat()
        except:
            pass
    return None


def fetch_rss(url, timeout=15):
    """Fetch and parse RSS feed, return list of articles."""
    articles = []
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; NOFXNewsBot/1.0)"
        })
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            data = resp.read().decode("utf-8", errors="replace")

        root = ET.fromstring(data)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        # RSS 2.0
        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            desc = (item.findtext("description") or "").strip()
            pub_date = (item.findtext("pubDate") or "").strip()
            if title:
                desc = re.sub(r"<[^>]+>", "", desc)[:500]
                published_iso = parse_rss_date(pub_date)
                articles.append({
                    "title": title,
                    "link": link,
                    "description": desc,
                    "published_raw": pub_date,
                    "published": published_iso,
                })

        # Atom
        for entry in root.findall("atom:entry", ns):
            title = (entry.findtext("atom:title", namespaces=ns) or "").strip()
            link_el = entry.find("atom:link", ns)
            link = link_el.get("href", "") if link_el is not None else ""
            desc = (entry.findtext("atom:summary", namespaces=ns) or "").strip()
            pub_date = (entry.findtext("atom:published", namespaces=ns) or "").strip()
            if title:
                desc = re.sub(r"<[^>]+>", "", desc)[:500]
                published_iso = parse_rss_date(pub_date)
                articles.append({
                    "title": title,
                    "link": link,
                    "description": desc,
                    "published_raw": pub_date,
                    "published": published_iso,
                })

    except Exception as e:
        print(f"  ⚠️ Failed to fetch {url}: {e}")

    return articles[:MAX_ARTICLES_PER_FEED]


def score_relevance(title, description):
    """Score article relevance (0-100)."""
    text = (title + " " + description).lower()
    score = 0
    for kw in RELEVANCE_KEYWORDS:
        if kw in text:
            score += 5
    # Boost for ETH-specific
    if any(k in text for k in ["ethereum", "eth ", "ether"]):
        score += 20
    # Boost for market-moving
    if any(k in text for k in ["sec", "etf", "regulation", "hack", "exploit", "whale", "liquidation"]):
        score += 15
    # Boost for DeFi
    if any(k in text for k in ["aave", "uniswap", "lido", "defi"]):
        score += 10
    return min(score, 100)


def load_history():
    """Load seen headline hashes."""
    try:
        with open(HISTORY_FILE) as f:
            return set(json.load(f))
    except:
        return set()


def save_history(seen):
    """Save headline hashes."""
    seen_list = list(seen)[-500:]  # Keep last 500
    with open(HISTORY_FILE, "w") as f:
        json.dump(seen_list, f)


def headline_hash(title):
    """Generate hash for deduplication."""
    return hashlib.md5(title.lower().strip().encode()).hexdigest()


def load_archive():
    """Load existing news archive."""
    try:
        with open(ARCHIVE_FILE) as f:
            return json.load(f)
    except:
        return []


def save_archive(archive):
    """Save news archive."""
    with open(ARCHIVE_FILE, "w") as f:
        json.dump(archive, f, indent=2, ensure_ascii=False)


def prune_archive(archive, days=30):
    """Remove articles older than specified days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    cutoff_iso = cutoff.isoformat()
    
    pruned = [
        a for a in archive 
        if a.get("published", "") >= cutoff_iso or a.get("scraped_at", "") >= cutoff_iso
    ]
    return pruned


def summarize_articles(articles):
    """Send articles to Gemma 3 4B for summarization."""
    if not articles:
        return []

    article_text = ""
    for i, a in enumerate(articles[:SUMMARY_MAX_ITEMS], 1):
        article_text += f"{i}. [{a['source']}] {a['title']}\n"
        article_text += f"   URL: {a.get('link', 'N/A')}\n"
        article_text += f"   Published: {a.get('published', a.get('published_raw', 'N/A'))}\n"
        if a.get("description"):
            article_text += f"   {a['description'][:200]}\n"

    prompt = f"""You are a crypto news analyst for an ETH trading desk. Analyze these headlines and provide a concise briefing.

HEADLINES:
{article_text}

OUTPUT FORMAT (JSON array, {SUMMARY_MAX_ITEMS} items max):
[
  {{
    "headline": "Short headline (max 80 chars)",
    "summary": "One sentence explaining why this matters for ETH trading",
    "impact": "bullish" or "bearish" or "neutral",
    "importance": 1-5 (5 = most important for trading),
    "tags": ["eth", "defi", "regulation", etc],
    "source": "Source name (e.g. CoinDesk)",
    "url": "Original article URL",
    "published": "ISO timestamp if available, otherwise original date string"
  }}
]

Rules:
- Focus on what matters for ETH price and DeFi ecosystem
- Skip fluff/promotional articles
- Be specific about market impact
- importance 5 = major market mover, 1 = minor/background
- Return ONLY valid JSON array, no other text"""

    try:
        payload = json.dumps({
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 2500,
            }
        }).encode()

        req = urllib.request.Request(
            OLLAMA_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read().decode())

        response_text = result.get("response", "")

        # Extract JSON from response
        json_match = re.search(r'\[[\s\S]*\]', response_text)
        if json_match:
            summaries = json.loads(json_match.group())
            return summaries
        else:
            print(f"  ⚠️ Could not extract JSON from response")
            return []

    except Exception as e:
        print(f"  ❌ Gemma summarization failed: {e}")
        return []


def fetch_indices():
    """Fetch crypto fear/greed indices from multiple sources."""
    indices = []
    
    # 1. Alternative.me Fear & Greed
    try:
        req = urllib.request.Request(
            "https://api.alternative.me/fng/",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
            data = json.loads(resp.read())
            if data.get("data"):
                d = data["data"][0]
                value = int(d.get("value", 50))
                label = d.get("value_classification", "Neutral")
                indices.append({
                    "name": "Fear & Greed Index",
                    "value": value,
                    "label": label,
                    "source": "Alternative.me",
                    "url": "https://alternative.me/crypto/fear-and-greed-index/"
                })
    except Exception as e:
        print(f"  ⚠️ Alternative.me fetch failed: {e}")
    
    # 2. CoinGlass Fear & Greed (free tier)
    try:
        req = urllib.request.Request(
            "https://api.coinglass.io/futures/funding_rate/fng_index?symbol=BTC",
            headers={"User-Agent": "Mozilla/5.0", "accept": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
            data = json.loads(resp.read())
            if data.get("data") and len(data["data"]) > 0:
                d = data["data"][0]
                value = int(d.get("value", 50))
                label = d.get("value_classification", "Neutral")
                indices.append({
                    "name": "Fear & Greed Index",
                    "value": value,
                    "label": label,
                    "source": "CoinGlass",
                    "url": "https://www.coinglass.io/futures/funding-rate"
                })
    except Exception as e:
        # CoinGlass may not have free access, skip silently
        pass
    
    # 3. AVERSION (Crypto Volatility Index)
    try:
        req = urllib.request.Request(
            "https://api.alternative.me/fng/",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
            # Already fetched above, but could add more sources here
            pass
    except:
        pass
    
    # Fallback: if no indices fetched, add default
    if not indices:
        indices.append({
            "name": "Fear & Greed Index",
            "value": 50,
            "label": "Neutral",
            "source": "Alternative.me",
            "url": "https://alternative.me/crypto/fear-and-greed-index/"
        })
    
    return indices


def generate_summary(archive):
    """Generate news-summary.json from archive."""
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    
    # Top stories: past 7 days, importance >= 4, sorted by importance desc
    week_ago = now - timedelta(days=7)
    top_stories = [
        a for a in archive
        if a.get("importance", 0) >= 4 
        and (a.get("published") and a["published"] >= week_ago.isoformat() or True)  # Accept all if no published
    ]
    top_stories = sorted(top_stories, key=lambda x: (-x.get("importance", 0), x.get("published", "")), reverse=True)
    
    # Recent news: past 1 hour only
    hour_ago = now - timedelta(hours=1)
    recent_news = [
        a for a in archive
        if a.get("published") and a["published"] >= hour_ago.isoformat()
    ]
    recent_news = sorted(recent_news, key=lambda x: x.get("published", ""), reverse=True)
    
    # Fetch indices
    indices = fetch_indices()
    
    summary = {
        "generated_at": now_iso,
        "top_stories": top_stories[:20],  # Limit for frontend
        "recent_news": recent_news[:20],
        "indices": indices,
    }
    
    return summary


def copy_to_frontend():
    """Copy summary to frontend data directory."""
    try:
        FRONTEND_DATA_DIR.mkdir(parents=True, exist_ok=True)
        if SUMMARY_FILE.exists():
            import shutil
            shutil.copy2(SUMMARY_FILE, FRONTEND_SUMMARY_FILE)
            print(f"  📁 Copied summary to frontend: {FRONTEND_SUMMARY_FILE}")
    except Exception as e:
        print(f"  ⚠️ Failed to copy to frontend: {e}")


def run_cycle():
    """Run one scraping cycle."""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] === News Scraper Cycle ===")
    
    # Load existing archive and history
    archive = load_archive()
    seen = load_history()
    
    print(f"  📚 Loaded {len(archive)} archived articles")
    
    new_articles = []
    
    # Fetch from all RSS feeds
    for feed in RSS_FEEDS:
        print(f"  📡 Fetching {feed['name']}...")
        articles = fetch_rss(feed["url"])
        
        for a in articles:
            h = headline_hash(a["title"])
            if h not in seen:
                a["source"] = feed["name"]
                a["relevance"] = score_relevance(a["title"], a.get("description", ""))
                a["scraped_at"] = datetime.now(timezone.utc).isoformat()
                new_articles.append(a)
                seen.add(h)
        
        print(f"    → {len(articles)} articles ({len([a for a in articles if headline_hash(a['title']) not in seen])} new)")
    
    print(f"  📰 Total new articles: {len(new_articles)}")
    
    if new_articles:
        # Summarize with Gemma
        print(f"  🧠 Summarizing with {MODEL}...")
        start = time.time()
        summaries = summarize_articles(new_articles)
        elapsed = time.time() - start
        print(f"    → {len(summaries)} summaries in {elapsed:.1f}s")
        
        # Add summaries to archive
        for s in summaries:
            s["scraped_at"] = datetime.now(timezone.utc).isoformat()
            archive.append(s)
        
        print(f"  💾 Added {len(summaries)} to archive")
    
    # Prune articles older than 30 days
    archive = prune_archive(archive, days=30)
    print(f"  ✂️ Pruned to {len(archive)} articles (30-day rolling)")
    
    # Save archive and history
    save_archive(archive)
    save_history(seen)
    
    # Generate summary
    summary = generate_summary(archive)
    
    with open(SUMMARY_FILE, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Wrote summary: {len(summary['top_stories'])} top stories, {len(summary['recent_news'])} recent")
    
    # Copy to frontend
    copy_to_frontend()
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] === Cycle Complete ===")
    
    return len(new_articles)


# Graceful shutdown
running = True

def signal_handler(signum, frame):
    global running
    print("\n🛑 Received shutdown signal, finishing cycle...")
    running = False


def main():
    global running
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if RUN_ONCE:
        run_cycle()
        return
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting News Scraper Daemon (every {INTERVAL}s)...")
    
    while running:
        try:
            run_cycle()
        except Exception as e:
            print(f"  ❌ Cycle error: {e}")
        
        # Sleep in small increments to allow quick shutdown
        for _ in range(INTERVAL):
            if not running:
                break
            time.sleep(1)
    
    print("News Scraper Daemon stopped.")


if __name__ == "__main__":
    main()
