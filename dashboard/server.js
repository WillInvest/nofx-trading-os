const http = require('http');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const PORT = 7001;
const OPENCLAW_DIR = process.env.OPENCLAW_DIR || path.join(os.homedir(), '.openclaw');
const agentsDir = path.join(OPENCLAW_DIR, 'agents');
const WORKSPACE = process.env.WORKSPACE || path.join(os.homedir(), '.openclaw/workspace');

// ─── Find all session dirs across agents ───
function getAllSessionDirs() {
  const dirs = [];
  try {
    for (const agent of fs.readdirSync(agentsDir)) {
      const sd = path.join(agentsDir, agent, 'sessions');
      if (fs.existsSync(path.join(sd, 'sessions.json'))) {
        dirs.push({ agent, dir: sd });
      }
    }
  } catch {}
  return dirs;
}

function findSessionFile(sessionId) {
  for (const { dir } of getAllSessionDirs()) {
    const jf = path.join(dir, sessionId + '.jsonl');
    if (fs.existsSync(jf)) return jf;
  }
  return null;
}

// ─── Session Data ───
function getSessionsJson() {
  const all = [];
  for (const { agent, dir } of getAllSessionDirs()) {
    try {
      const sFile = path.join(dir, 'sessions.json');
      const data = JSON.parse(fs.readFileSync(sFile, 'utf8'));
      for (const [key, s] of Object.entries(data)) {
        const sessionId = s.sessionId || key;
        all.push({
          key,
          agent,
          label: s.label || key.split(':').pop(),
          model: s.modelOverride || s.model || '-',
          totalTokens: s.totalTokens || 0,
          contextTokens: s.contextTokens || 0,
          kind: s.kind || 'direct',
          updatedAt: s.updatedAt || 0,
          createdAt: s.createdAt || 0,
          aborted: s.abortedLastRun || false,
          channel: s.channel || '-',
          sessionId,
          lastMessage: getLastMessage(sessionId),
          thinkingLevel: s.thinkingLevel || null,
        });
      }
    } catch {}
  }
  return all;
}

function getLastMessage(sessionId) {
  try {
    const jf = findSessionFile(sessionId);
    if (!jf) return '';
    const content = fs.readFileSync(jf, 'utf8');
    const lines = content.trim().split('\n').reverse();
    for (const line of lines) {
      try {
        const d = JSON.parse(line);
        if (d.type === 'message' && d.message) {
          const msg = d.message;
          // Get assistant messages
          if (msg.role === 'assistant') {
            // Extract text content
            if (typeof msg.content === 'string') return msg.content.slice(0, 200);
            if (Array.isArray(msg.content)) {
              for (const block of msg.content) {
                if (block.type === 'text' && block.text) return block.text.slice(0, 200);
              }
            }
          }
          // Get user messages
          if (msg.role === 'user') {
            if (typeof msg.content === 'string') return '👤 ' + msg.content.slice(0, 200);
            if (Array.isArray(msg.content)) {
              for (const block of msg.content) {
                if (block.type === 'text' && block.text) return '👤 ' + block.text.slice(0, 200);
              }
            }
          }
        }
      } catch {}
    }
    return '';
  } catch { return ''; }
}

// Get recent messages for a session (last N)
function getRecentMessages(sessionId, limit = 10) {
  try {
    const jf = findSessionFile(sessionId);
    if (!jf) return [];
    const content = fs.readFileSync(jf, 'utf8');
    const lines = content.trim().split('\n').reverse();
    const messages = [];
    for (const line of lines) {
      if (messages.length >= limit) break;
      try {
        const d = JSON.parse(line);
        if (d.type === 'message' && d.message) {
          const msg = d.message;
          let text = '';
          if (typeof msg.content === 'string') text = msg.content;
          else if (Array.isArray(msg.content)) {
            for (const block of msg.content) {
              if (block.type === 'text' && block.text) { text = block.text; break; }
            }
          }
          if (text && (msg.role === 'user' || msg.role === 'assistant')) {
            // Check for tool use
            let tools = [];
            if (Array.isArray(msg.content)) {
              for (const block of msg.content) {
                if (block.type === 'tool_use') tools.push(block.name);
              }
            }
            messages.push({
              role: msg.role,
              text: text.slice(0, 500),
              tools,
              timestamp: d.timestamp || '',
              model: msg.model || '',
            });
          }
        }
      } catch {}
    }
    return messages.reverse();
  } catch { return []; }
}

// ─── HTTP Server ───
const server = http.createServer((req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.url === '/api/sessions') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(getSessionsJson()));
    return;
  }
  
  if (req.url.startsWith('/api/messages?')) {
    const params = new URL(req.url, 'http://localhost').searchParams;
    const sid = params.get('sid') || '';
    const limit = parseInt(params.get('limit') || '10');
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(getRecentMessages(sid, limit)));
    return;
  }

  // ─── Memory API (mem0) ───
  if (req.url === '/api/memory' || req.url.startsWith('/api/memory?')) {
    try {
      const params = new URL(req.url, 'http://localhost').searchParams;
      const q = params.get('q') || '';
      let data;
      if (q) {
        // Search memories (JSON output, not compact)
        const output = execSync(`python3 ${WORKSPACE}/bin/mem0-service.py search -u hao -q "${q.replace(/"/g, '\\"')}"`, { encoding: 'utf8', timeout: 10000 });
        const parsed = JSON.parse(output);
        data = (parsed.results || []).map(r => ({ score: r.score, text: r.memory, created_at: r.created_at }));
      } else {
        // Get all memories (limit to 10 for speed)
        const output = execSync(`python3 ${WORKSPACE}/bin/mem0-service.py get -u hao --limit 10`, { encoding: 'utf8', timeout: 10000 });
        // Parse "Total memories: N" format
        const lines = output.split('\n').filter(l => l.startsWith('  ['));
        data = lines.map(line => {
          const match = line.match(/\[(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})\] (.+)/);
          if (match) return { created_at: match[1], text: match[2] };
          return { text: line };
        });
      }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(data));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // ─── Cron Jobs API ───
  if (req.url === '/api/crons') {
    try {
      // Get cron jobs from openclaw CLI
      const output = execSync('openclaw cron list --json 2>/dev/null || echo "[]"', { encoding: 'utf8', timeout: 5000 });
      let crons = [];
      try {
        const parsed = JSON.parse(output);
        crons = parsed.jobs || parsed || [];
      } catch {
        // Fallback: parse text output
        const lines = output.split('\n').filter(l => l.includes(':'));
        crons = lines.map(line => {
          const parts = line.split(':');
          const id = parts[0]?.trim();
          const schedule = parts[1]?.trim() || '';
          const desc = parts.slice(2).join(':').trim() || '';
          return { id, schedule, description: desc, status: 'unknown' };
        }).filter(c => c.id);
      }
      // Normalize fields
      crons = crons.map(c => ({
        id: c.id || c.name || '',
        schedule: c.schedule?.expr || c.schedule || '',
        description: c.name || c.description || '',
        status: c.enabled !== false ? 'active' : 'disabled',
        nextRun: c.state?.nextRunAtMs || null,
      }));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(crons));
    } catch (e) {
      // Fallback: try to read cron config files directly
      try {
        const cronDir = path.join(OPENCLAW_DIR, 'crons');
        const files = fs.readdirSync(cronDir).filter(f => f.endsWith('.json'));
        const crons = files.map(f => {
          const data = JSON.parse(fs.readFileSync(path.join(cronDir, f), 'utf8'));
          return {
            id: f.replace('.json', ''),
            schedule: data.schedule || '',
            description: data.description || '',
            status: data.enabled !== false ? 'active' : 'disabled',
            lastRun: data.lastRun || null,
          };
        });
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(crons));
      } catch (e2) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Could not fetch crons: ' + e2.message }));
      }
    }
    return;
  }

  // ─── MEMORY.md API ───
  if (req.url === '/api/memory-md') {
    try {
      const memPath = path.join(WORKSPACE, 'MEMORY.md');
      if (fs.existsSync(memPath)) {
        const content = fs.readFileSync(memPath, 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/markdown; charset=utf-8' });
        res.end(content);
      } else {
        res.writeHead(404);
        res.end('MEMORY.md not found');
      }
    } catch (e) {
      res.writeHead(500);
      res.end(e.message);
    }
    return;
  }

  // Static files
  let filePath = req.url === '/' ? '/index.html' : req.url;
  filePath = path.join(__dirname, filePath);
  const ext = path.extname(filePath);
  const types = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.png': 'image/png' };
  
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }
    res.writeHead(200, { 'Content-Type': types[ext] || 'text/plain' });
    res.end(data);
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Agent Dashboard: http://0.0.0.0:${PORT}`);
});
