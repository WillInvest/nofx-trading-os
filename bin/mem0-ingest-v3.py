#!/usr/bin/env python3
"""Ingest NOFX-related memory files using DeepSeek V3 for extraction."""

import json
import os
import sys
import glob
import time

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

def main():
    m = Memory.from_config(CONFIG)
    print("Memory initialized with DeepSeek V3 + Qdrant")
    
    # NOFX-relevant files only (Feb 15+)
    nofx_files = [
        "memory/2026-02-15.md",
        "memory/2026-02-16.md",
        "memory/2026-02-19.md",
        "memory/2026-02-19-nofx-philosophy.md",
        "memory/2026-02-20.md",
        "memory/2026-02-20-debater-data.md",
        "memory/2026-02-21.md",
        "MEMORY.md",
    ]
    
    total_memories = 0
    total_chunks = 0
    
    for filepath in nofx_files:
        if not os.path.exists(filepath):
            print(f"\n⚠️  {filepath} not found, skipping")
            continue
            
        with open(filepath, 'r') as f:
            content = f.read()
        
        if not content.strip():
            continue
        
        basename = os.path.basename(filepath)
        print(f"\n📄 Ingesting {basename} ({len(content)} chars)...")
        
        # Split into ~2500 char chunks at paragraph boundaries
        chunks = []
        current = ""
        for line in content.split('\n'):
            if len(current) + len(line) > 2500 and current.strip():
                chunks.append(current)
                current = line + '\n'
            else:
                current += line + '\n'
        if current.strip():
            chunks.append(current)
        
        for i, chunk in enumerate(chunks):
            messages = [{"role": "user", "content": chunk}]
            metadata = {"source": basename, "chunk": i, "topic": "nofx"}
            
            try:
                result = m.add(messages, user_id="hao", metadata=metadata)
                count = len(result.get('results', []))
                total_memories += count
                total_chunks += 1
                events = [r.get('event', '?') for r in result.get('results', [])]
                print(f"  ✅ Chunk {i+1}/{len(chunks)}: {count} memories ({', '.join(events)})")
                
                # Brief pause to respect rate limits
                time.sleep(0.5)
            except Exception as e:
                print(f"  ❌ Chunk {i+1} error: {e}")
                time.sleep(2)
    
    print(f"\n{'='*50}")
    print(f"✅ Done! {total_memories} memories from {total_chunks} chunks")
    
    # Show stats
    all_mems = m.get_all(user_id="hao")
    print(f"📊 Total memories in Qdrant: {len(all_mems.get('results', []))}")

if __name__ == '__main__':
    os.chdir("/home/openclaw/.openclaw/workspace")
    main()
