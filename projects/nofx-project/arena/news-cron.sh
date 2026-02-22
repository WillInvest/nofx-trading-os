#!/bin/bash
# news-cron.sh — Scrape news + copy to Docker data volume
# Run every 30 min via crontab

ARENA_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCKER_DATA="/home/openclaw/.openclaw/workspace/projects/nofx-project/nofx/data/arena"

echo "[$(date '+%H:%M:%S')] News scraper starting..."

# Run scraper
python3 "$ARENA_DIR/news-scraper.py" 2>&1

# Copy to Docker data volume
if [ -f "$ARENA_DIR/news-summary.json" ]; then
    cp "$ARENA_DIR/news-summary.json" "$DOCKER_DATA/news-summary.json"
    echo "[$(date '+%H:%M:%S')] Copied to Docker data volume"
fi

echo "[$(date '+%H:%M:%S')] Done"
