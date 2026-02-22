# Task Logging Skill

Log all spawned sub-agent tasks for monitoring.

## When to Use

**Always** when using `sessions_spawn` to create background tasks.

## Log File

`workspace/logs/tasks.jsonl`

## Log Format

**When starting a task:**
```json
{"id":"<runId>","label":"<label>","model":"<model>","status":"running","task":"<brief description>","startedAt":<timestamp_ms>}
```

**When task completes** (from the completion notification):
```json
{"id":"<runId>","status":"complete","tokensIn":<n>,"tokensOut":<n>,"completedAt":<timestamp_ms>}
```

## How to Log

Use `exec` to append to the log file:

```bash
echo '{"id":"abc123","label":"my-task","model":"opus","status":"running","task":"Do something","startedAt":1738635000000}' >> workspace/logs/tasks.jsonl
```

## Monitor UI

Serve the monitor: `cd workspace && python3 -m http.server 9090`
View at: `http://localhost:9090/monitor/`

## Model Badge in Replies

When responding to users, optionally prefix with model indicator:
- `[opus]` for Claude Opus
- `[llama]` for local Llama

This helps the user know which model is responding without checking status.
