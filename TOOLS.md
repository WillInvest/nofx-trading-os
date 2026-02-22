# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

---

## Task Monitor

- **Log file:** `workspace/logs/tasks.jsonl`
- **Monitor UI:** `workspace/monitor/index.html`
- **To serve:** `cd workspace && python3 -m http.server 9090`
- **View at:** `http://localhost:9090/monitor/` (or via SSH tunnel)

### Model Badge Convention

When responding, prefix replies with model indicator so user knows which model is active:
- `[opus]` — Claude Opus (expensive)
- `[llama]` — Local Llama 8B (free)

Example: `[llama] Sure, I can help with that...`

### Task Logging

When spawning sub-agents, ALWAYS:
1. Log task start to `logs/tasks.jsonl`
2. Use the user's current model unless they explicitly approve switching
3. Log completion when the task finishes

---

## Coding Agent Fleet

### Model Hierarchy
- **Opus 4.6** (me) — CEO/Manager. Strategic decisions, complex debugging, architecture
- **MiniMax M2.5** (sub-agent `coder`) — **PRIMARY coder**. Go backend, React frontend, multi-file tasks. Upgraded — rely on heavily.
  - Spawned via: `sessions_spawn(agentId: "coder", task: "...")`
  - Auto-announces result when done; can steer/kill via `subagents`
- **Qwen3-30B-A3B** (local) — Junior Dev. Scripts, simple edits, tests, grunt work
  - Ollama: `qwen3:30b-a3b`
  - Cost: FREE
  - Speed: ~30 tok/s

### Dispatch Rules
- 🟢 Simple edits / scripts → **spawn `coder` sub-agent** (MiniMax) or local Qwen3
- 🟡 Medium+ coding (multi-file, backend, frontend) → **spawn `coder` sub-agent** (MiniMax)
- 🔴 Complex/Critical architecture → **spawn `coder` sub-agent** (MiniMax), I review
- **Always read the relevant code first**, then give the sub-agent precise instructions with file paths and line numbers
- **Always pass `model: "minimax/MiniMax-M2.5"` explicitly** when spawning coder sub-agents (otherwise inherits caller's Opus model!)
- **After sub-agent finishes**: review diff, verify build, then deploy

## Mem0 Vector Memory

- **Service**: `bin/mem0-service.py` (add/search/get/ingest)
- **LLM**: DeepSeek V3 (for fact extraction) — swap to local later
- **Embedder**: Ollama nomic-embed-text (768 dims, local, free)
- **Vector DB**: Qdrant on localhost:6333, collection `openclaw_memories`
- **Storage**: `/home/openclaw/.openclaw/workspace/data/qdrant/`
- **Current memories**: 100 (NOFX-related, user_id=hao)

### Usage
```bash
# Save conversation to memory
python3 bin/mem0-service.py add -u hao -m "conversation text here"

# Search memories
python3 bin/mem0-service.py search -u hao -q "debate engine architecture" -c

# Get all memories
python3 bin/mem0-service.py get -u hao
```

### Going Forward
- After each significant conversation: save key exchanges to mem0
- Cron: save debate results + decisions with metadata
- Pre-compaction: dump full conversation to mem0 before OpenClaw compacts

---

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
