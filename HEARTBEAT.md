# HEARTBEAT.md

## Context Health Check
Before anything else, check context usage via session_status.
- If context > 75%: dump all key decisions to mem0, write session summary to memory/YYYY-MM-DD.md
- If context > 85%: alert Hao that compaction is imminent, save everything

## Sub-Agent Watchdog
Check `subagents list` for:
- Any task running > 15 minutes → alert Hao: "⚠️ [task] has been running for X min, may be stuck"
- Any task with status "failed" that wasn't reported → alert Hao: "❌ [task] failed silently"
- If there ARE active sub-agents → tell Hao what's in progress: "🔨 [task1] running 3m, [task2] running 5m"
- After significant dispatches, proactively report status even without heartbeat

## Every Heartbeat — Mem0 Context
Before doing anything, recall relevant context:
```bash
python3 bin/mem0-service.py search -u hao -q "current trading state and recent decisions" -c
```

## After Hourly Scan (check if new debate results exist)
1. Check if `/home/openclaw/.openclaw/workspace/projects/nofx-project/nofx/data/arena/hourly-plan.json` was updated in the last 30 min
2. If new debate results: read the R1 syntheses, check current positions/orders on Hyperliquid, write comprehensive trading plan for Fao
3. Update `hourly-plan.json` and `trader-instruction.json` with the decision
4. Save decision to mem0: `python3 bin/mem0-service.py add -u hao -m "Hourly decision: [summary]"`

## End of Significant Conversations
If the main session had important exchanges, save them:
```bash
python3 bin/mem0-service.py add -u hao -m "[key facts from conversation]"
```
