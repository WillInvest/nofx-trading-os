#!/usr/bin/env node
/**
 * Print OpenClaw API usage from session JSONL files.
 * Usage: node scripts/openclaw-usage.js
 * Env: OPENCLAW_DIR (default: ~/.openclaw)
 */
const fs = require('fs');
const path = require('path');
const os = require('os');

const OPENCLAW_DIR = process.env.OPENCLAW_DIR || path.join(os.homedir(), '.openclaw');
const SESS_DIR = path.join(OPENCLAW_DIR, 'agents', 'main', 'sessions');

const now = Date.now();
const fiveHoursMs = 5 * 3600000;
const oneDayMs = 86400000;
const todayStart = new Date();
todayStart.setUTCHours(0, 0, 0, 0);
const todayStartMs = todayStart.getTime();

function isSessionFile(name) {
  return name.endsWith('.jsonl') && name !== 'sessions.json';
}

let perModel5h = {};
let perModelToday = {};
let totalCost5h = 0;
let totalCostToday = 0;
let calls5h = 0;
let callsToday = 0;

if (!fs.existsSync(SESS_DIR)) {
  console.error('Sessions dir not found:', SESS_DIR);
  process.exit(1);
}

const files = fs.readdirSync(SESS_DIR).filter(isSessionFile);
for (const file of files) {
  const filePath = path.join(SESS_DIR, file);
  let content;
  try {
    content = fs.readFileSync(filePath, 'utf8');
  } catch {
    continue;
  }
  for (const line of content.split('\n')) {
    if (!line.trim()) continue;
    try {
      const d = JSON.parse(line);
      if (d.type !== 'message' || !d.message?.usage) continue;
      const msg = d.message;
      const ts = d.timestamp ? new Date(d.timestamp).getTime() : 0;
      if (!ts) continue;
      const model = msg.model || 'unknown';
      const inTok = (msg.usage.input || 0) + (msg.usage.cacheRead || 0) + (msg.usage.cacheWrite || 0);
      const outTok = msg.usage.output || 0;
      const cost = msg.usage.cost?.total ?? 0;

      if (now - ts < fiveHoursMs) {
        if (!perModel5h[model]) perModel5h[model] = { input: 0, output: 0, cost: 0, calls: 0 };
        perModel5h[model].input += inTok;
        perModel5h[model].output += outTok;
        perModel5h[model].cost += cost;
        perModel5h[model].calls++;
        totalCost5h += cost;
        calls5h++;
      }
      if (ts >= todayStartMs) {
        if (!perModelToday[model]) perModelToday[model] = { input: 0, output: 0, cost: 0, calls: 0 };
        perModelToday[model].input += inTok;
        perModelToday[model].output += outTok;
        perModelToday[model].cost += cost;
        perModelToday[model].calls++;
        totalCostToday += cost;
        callsToday++;
      }
    } catch {}
  }
}

function fmt(n) {
  if (n >= 1e6) return (n / 1e6).toFixed(2) + 'M';
  if (n >= 1e3) return (n / 1e3).toFixed(2) + 'K';
  return String(Math.round(n));
}

console.log('OpenClaw usage (from session logs)');
console.log('Sessions dir:', SESS_DIR);
console.log('');
console.log('Last 5 hours:');
console.log('  Total cost:    $' + totalCost5h.toFixed(4));
console.log('  API calls:     ' + calls5h);
for (const [model, data] of Object.entries(perModel5h)) {
  console.log('  ' + model + ':');
  console.log('    input: ' + fmt(data.input) + '  output: ' + fmt(data.output) + '  cost: $' + data.cost.toFixed(4) + '  calls: ' + data.calls);
}
console.log('');
console.log('Today (UTC):');
console.log('  Total cost:    $' + totalCostToday.toFixed(4));
console.log('  API calls:     ' + callsToday);
for (const [model, data] of Object.entries(perModelToday)) {
  console.log('  ' + model + ':');
  console.log('    input: ' + fmt(data.input) + '  output: ' + fmt(data.output) + '  cost: $' + data.cost.toFixed(4) + '  calls: ' + data.calls);
}
