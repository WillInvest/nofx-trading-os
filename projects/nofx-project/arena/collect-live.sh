#!/bin/bash
# collect-live.sh — Merge data every minute (runs via crontab)
# This script combines hourly + live data for near-real-time frontend

set -euo pipefail

ARENA_DIR="/home/openclaw/.openclaw/workspace/projects/nofx-project/arena"

echo "[$(date '+%H:%M:%S')] Merging live data..."

# Merge all sources into debate-context.json
python3 "$ARENA_DIR/merge-live.py"

echo "[$(date '+%H:%M:%S')] Done"
