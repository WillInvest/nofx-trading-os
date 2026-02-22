const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 7002;
const DATA_DIR = path.join(__dirname, '..', 'data');

const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.ico': 'image/x-icon'
};

function readJsonFile(filename) {
  const filepath = path.join(DATA_DIR, filename);
  try {
    const data = fs.readFileSync(filepath, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    console.error(`Error reading ${filename}:`, err.message);
    return null;
  }
}

function formatResponse(data, res) {
  res.writeHead(200, { 'Content-Type': 'application/json', 'Cache-Control': 'no-cache' });
  res.end(JSON.stringify(data));
}

function handleApiRequest(endpoint, res) {
  let data;
  
  switch (endpoint) {
    case '/api/status':
      data = readJsonFile('status.json');
      break;
    case '/api/decision':
      data = readJsonFile('decision.json');
      break;
    case '/api/trades':
      data = readJsonFile('trades.json');
      break;
    case '/api/health':
      data = { status: 'ok', timestamp: new Date().toISOString() };
      break;
    default:
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Not found' }));
      return;
  }
  
  if (data === null) {
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Data unavailable' }));
    return;
  }
  
  formatResponse(data, res);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const pathname = url.pathname;
  
  // CORS headers for local development
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }
  
  // API routes
  if (pathname.startsWith('/api/')) {
    handleApiRequest(pathname, res);
    return;
  }
  
  // Serve index.html for root
  let filepath = pathname === '/' ? '/index.html' : pathname;
  const fullPath = path.join(__dirname, filepath);
  const ext = path.extname(fullPath);
  const contentType = MIME_TYPES[ext] || 'text/plain';
  
  fs.readFile(fullPath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        // Serve index.html for any non-file route (SPA fallback)
        fs.readFile(path.join(__dirname, 'index.html'), (err2, indexContent) => {
          if (err2) {
            res.writeHead(404);
            res.end('Not found');
          } else {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(indexContent);
          }
        });
      } else {
        res.writeHead(500);
        res.end('Server error');
      }
      return;
    }
    
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(content);
  });
});

server.listen(PORT, () => {
  console.log(`ETH Engine Dashboard running at http://localhost:${PORT}`);
});
