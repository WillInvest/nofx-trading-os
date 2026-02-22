#!/usr/bin/env python3
"""
TradingAgents Dashboard Server

Serves the dashboard UI and provides JSON data from examples directory.
"""

import http.server
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse

# Paths
DASHBOARD_DIR = Path(__file__).parent
PROJECT_DIR = DASHBOARD_DIR.parent
EXAMPLES_DIR = PROJECT_DIR / "examples"

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        # Serve data endpoints
        if path == '/data/index.json':
            self.send_json(self.build_index())
        elif path.startswith('/data/'):
            self.serve_data_file(path[6:])  # Remove '/data/'
        else:
            super().do_GET()
    
    def build_index(self):
        """Build index of all analyses from examples directory."""
        index = {}
        
        if not EXAMPLES_DIR.exists():
            return index
        
        for folder in sorted(EXAMPLES_DIR.iterdir(), reverse=True):
            if not folder.is_dir():
                continue
            
            # Parse folder name: YYYY-MM-DD-SYMBOL
            match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)', folder.name)
            if not match:
                continue
            
            date, symbol = match.groups()
            key = folder.name
            
            # Load summary if exists - try multiple filenames
            summary_file = None
            for fname in ['08_summary.json', '10_summary.json', '17_summary.json']:
                if (folder / fname).exists():
                    summary_file = folder / fname
                    break
            summary = {}
            if summary_file and summary_file.exists():
                try:
                    with open(summary_file) as f:
                        summary = json.load(f)
                except:
                    pass
            
            # Extract recommendation
            rec = summary.get('recommendation', '')
            if isinstance(rec, str) and 'Recommendation.' in rec:
                rec = rec.replace('Recommendation.', '')
            
            # Confidence might be 0-1 or 0-100, normalize to 0-100
            conf = summary.get('confidence', 0)
            if conf is not None and conf <= 1:
                conf = conf * 100
            
            index[key] = {
                'symbol': symbol,
                'date': date,
                'price': summary.get('price'),
                'recommendation': rec,
                'confidence': conf,
                'action': summary.get('action'),
                'shares': summary.get('shares', 0),
                'timestamp': summary.get('timestamp', f'{date}T00:00:00'),
            }
        
        return index
    
    def serve_data_file(self, path):
        """Serve files from examples directory."""
        parts = path.strip('/').split('/')
        
        if len(parts) == 1:
            # Folder listing
            folder = EXAMPLES_DIR / parts[0]
            if folder.is_dir():
                files = [f.name for f in folder.iterdir() if f.is_file()]
                self.send_json(files)
            else:
                self.send_error(404)
        
        elif len(parts) == 2:
            folder, filename = parts
            
            # Special case: detail.json (aggregate data for dashboard)
            if filename == 'detail.json':
                self.send_json(self.build_detail(folder))
            else:
                # Serve actual file
                file_path = EXAMPLES_DIR / folder / filename
                if file_path.exists():
                    self.send_file(file_path)
                else:
                    self.send_error(404)
        else:
            self.send_error(404)
    
    def build_detail(self, folder_name):
        """Build detailed view data for a ticker."""
        folder = EXAMPLES_DIR / folder_name
        if not folder.exists():
            return {}
        
        detail = {
            'analysts': {},
            'debate': [],
            'stages': [],
            'files': [],
        }
        
        # List files
        detail['files'] = sorted([f.name for f in folder.iterdir() if f.is_file()])
        
        # Load analyst reports - try multiple possible filenames
        analyst_files = {
            'market': ['04_market_report.json', '06_market_report.json', '08_market_analyst.json'],
            'news': ['04c_news_report.json', '05_news_report.json', '07_news_report.json'], 
            'fundamentals': ['04e_fundamentals_report.json', '08_fundamentals_report.json', '10_fundamentals_analyst.json'],
            'social': ['04g_social_report.json', '04f_social_report.json', '11_social_analyst.json'],
            'risk': ['06_risk_assessment.json', '08_risk_assessment.json', '14_risk_debrief.json'],
        }
        
        for key, filenames in analyst_files.items():
            for filename in filenames:
                filepath = folder / filename
                if filepath.exists():
                    try:
                        with open(filepath) as f:
                            data = json.load(f)
                            # Try various field names for the content
                            content = (data.get('content') or 
                                      data.get('report') or 
                                      data.get('analysis') or 
                                      json.dumps(data, indent=2))
                            detail['analysts'][key] = content
                            break  # Found the file, stop looking
                    except Exception as e:
                        detail['analysts'][key] = f"Error loading: {e}"
        
        # Load debate rounds - try multiple filenames
        debate_file = None
        for fname in ['05_debate_rounds.json', '07_debate_rounds.json', '09_debate_rounds.json']:
            if (folder / fname).exists():
                debate_file = folder / fname
                break
        if debate_file.exists():
            try:
                with open(debate_file) as f:
                    debate_data = json.load(f)
                    # Handle both list format and dict with 'rounds' key
                    rounds = debate_data if isinstance(debate_data, list) else debate_data.get('rounds', [])
                    for r in rounds:
                        # Handle various formats
                        bull_arg = r.get('bull', '')
                        bear_arg = r.get('bear', '')
                        # If bull/bear are dicts, extract argument
                        if isinstance(bull_arg, dict):
                            bull_arg = bull_arg.get('argument', '')
                        if isinstance(bear_arg, dict):
                            bear_arg = bear_arg.get('argument', '')
                        detail['debate'].append({
                            'round': r.get('round', len(detail['debate']) + 1),
                            'bull': bull_arg,
                            'bear': bear_arg,
                        })
            except Exception as e:
                detail['debate'] = [{'error': str(e)}]
        
        # Build stages from file existence
        stage_files = [
            ('Data Collection', ['01_params.json', '02_ohlcv.json']),
            ('Technical Analysis', ['05_indicators.json']),
            ('Market Analysis', ['08_market_analyst.json']),
            ('News Analysis', ['07_news_analyst.json']),
            ('Bull/Bear Debate', ['09_debate_rounds.json']),
            ('Risk Assessment', ['14_risk_debrief.json']),
            ('Final Decision', ['17_summary.json']),
        ]
        
        for name, files in stage_files:
            exists = any((folder / f).exists() for f in files)
            detail['stages'].append({
                'name': name,
                'status': 'complete' if exists else '',
            })
        
        return detail
    
    def send_json(self, data):
        """Send JSON response."""
        content = json.dumps(data, indent=2).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(content))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(content)
    
    def send_file(self, filepath):
        """Send file with appropriate content type."""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            content_type = 'application/json' if filepath.suffix == '.json' else 'text/plain'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))

def main():
    import argparse
    parser = argparse.ArgumentParser(description='TradingAgents Dashboard Server')
    parser.add_argument('-p', '--port', type=int, default=9091, help='Port (default: 9091)')
    parser.add_argument('--host', default='0.0.0.0', help='Host (default: 0.0.0.0)')
    args = parser.parse_args()
    
    server = http.server.HTTPServer((args.host, args.port), DashboardHandler)
    print(f"🚀 TradingAgents Dashboard: http://{args.host}:{args.port}/")
    print(f"📁 Examples dir: {EXAMPLES_DIR}")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()

if __name__ == '__main__':
    main()
