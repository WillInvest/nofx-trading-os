#!/usr/bin/env python3
"""mem0 memory service — CLI wrapper for add/search/get/ingest operations.

Usage:
  mem0-service.py add --user USER --message "conversation text"
  mem0-service.py add --user USER --file path/to/conversation.txt
  mem0-service.py search --user USER --query "what do I know about X"
  mem0-service.py search --agent AGENT --query "nofx trading decisions"
  mem0-service.py get --user USER [--limit 20]
  mem0-service.py ingest --user USER --dir memory/  # bulk ingest markdown files
  mem0-service.py stats
"""

import argparse
import json
import os
import sys
import glob
from datetime import datetime

# Suppress warnings
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

from mem0 import Memory

DEEPSEEK_API_KEY = "sk-a998cc65294642489687e0eb561733df"

CONFIG = {
    'llm': {
        'provider': 'deepseek',
        'config': {
            'model': 'deepseek-chat',
            'api_key': DEEPSEEK_API_KEY,
            'temperature': 0.1,
            'max_tokens': 4000,
        }
    },
    'embedder': {
        'provider': 'ollama',
        'config': {
            'model': 'nomic-embed-text',
        }
    },
    'vector_store': {
        'provider': 'qdrant',
        'config': {
            'collection_name': 'openclaw_memories',
            'host': 'localhost',
            'port': 6333,
            'embedding_model_dims': 768,
        }
    }
}

def get_memory():
    return Memory.from_config(CONFIG)

def cmd_add(args):
    m = get_memory()
    
    if args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    else:
        text = args.message
    
    if not text:
        print("Error: provide --message or --file", file=sys.stderr)
        sys.exit(1)
    
    # Build messages
    messages = [{"role": "user", "content": text}]
    
    kwargs = {}
    if args.user:
        kwargs['user_id'] = args.user
    if args.agent:
        kwargs['agent_id'] = args.agent
    if args.metadata:
        kwargs['metadata'] = json.loads(args.metadata)
    
    result = m.add(messages, **kwargs)
    print(json.dumps(result, indent=2, default=str))

def cmd_search(args):
    m = get_memory()
    
    kwargs = {'limit': args.limit or 10}
    if args.user:
        kwargs['user_id'] = args.user
    if args.agent:
        kwargs['agent_id'] = args.agent
    
    results = m.search(args.query, **kwargs)
    
    if args.compact:
        for r in results.get('results', []):
            score = r.get('score', 0)
            print(f"[{score:.2f}] {r['memory']}")
    else:
        print(json.dumps(results, indent=2, default=str))

def cmd_get(args):
    m = get_memory()
    
    kwargs = {}
    if args.user:
        kwargs['user_id'] = args.user
    if args.agent:
        kwargs['agent_id'] = args.agent
    
    results = m.get_all(**kwargs)
    
    memories = results.get('results', [])
    print(f"Total memories: {len(memories)}")
    for mem in memories[:args.limit or 50]:
        created = mem.get('created_at', '')[:19]
        print(f"  [{created}] {mem['memory']}")

def cmd_ingest(args):
    """Bulk ingest markdown files into mem0."""
    m = get_memory()
    
    pattern = os.path.join(args.dir, '*.md')
    files = sorted(glob.glob(pattern))
    
    if not files:
        print(f"No .md files found in {args.dir}")
        return
    
    total_memories = 0
    for filepath in files:
        basename = os.path.basename(filepath)
        print(f"\nIngesting {basename}...")
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        if not content.strip():
            print(f"  Skipped (empty)")
            continue
        
        # Split large files into chunks (~2000 chars each)
        chunks = []
        current = ""
        for line in content.split('\n'):
            if len(current) + len(line) > 2000:
                if current.strip():
                    chunks.append(current)
                current = line + '\n'
            else:
                current += line + '\n'
        if current.strip():
            chunks.append(current)
        
        for i, chunk in enumerate(chunks):
            messages = [{"role": "user", "content": chunk}]
            metadata = {"source": basename, "chunk": i}
            
            kwargs = {"metadata": metadata}
            if args.user:
                kwargs['user_id'] = args.user
            if args.agent:
                kwargs['agent_id'] = args.agent
            
            try:
                result = m.add(messages, **kwargs)
                count = len(result.get('results', []))
                total_memories += count
                print(f"  Chunk {i+1}/{len(chunks)}: extracted {count} memories")
            except Exception as e:
                print(f"  Chunk {i+1} error: {e}")
    
    print(f"\nDone! Total new memories: {total_memories}")

def cmd_stats(args):
    m = get_memory()
    
    # Get all memories
    all_mems = m.get_all()
    total = len(all_mems.get('results', []))
    
    # Count by user
    users = {}
    for mem in all_mems.get('results', []):
        uid = mem.get('user_id', 'unknown')
        users[uid] = users.get(uid, 0) + 1
    
    print(f"Total memories: {total}")
    for uid, count in sorted(users.items()):
        print(f"  {uid}: {count}")

def main():
    parser = argparse.ArgumentParser(description='mem0 memory service')
    sub = parser.add_subparsers(dest='command')
    
    # add
    p_add = sub.add_parser('add')
    p_add.add_argument('--user', '-u')
    p_add.add_argument('--agent', '-a')
    p_add.add_argument('--message', '-m')
    p_add.add_argument('--file', '-f')
    p_add.add_argument('--metadata')
    
    # search
    p_search = sub.add_parser('search')
    p_search.add_argument('--user', '-u')
    p_search.add_argument('--agent', '-a')
    p_search.add_argument('--query', '-q', required=True)
    p_search.add_argument('--limit', '-l', type=int, default=10)
    p_search.add_argument('--compact', '-c', action='store_true')
    
    # get
    p_get = sub.add_parser('get')
    p_get.add_argument('--user', '-u')
    p_get.add_argument('--agent', '-a')
    p_get.add_argument('--limit', '-l', type=int, default=50)
    
    # ingest
    p_ingest = sub.add_parser('ingest')
    p_ingest.add_argument('--user', '-u')
    p_ingest.add_argument('--agent', '-a')
    p_ingest.add_argument('--dir', '-d', required=True)
    
    # stats
    sub.add_parser('stats')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        cmd_add(args)
    elif args.command == 'search':
        cmd_search(args)
    elif args.command == 'get':
        cmd_get(args)
    elif args.command == 'ingest':
        cmd_ingest(args)
    elif args.command == 'stats':
        cmd_stats(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
