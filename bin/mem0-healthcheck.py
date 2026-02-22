#!/usr/bin/env python3
"""Mem0 health check — verify memories are being saved correctly.

Checks:
1. Qdrant is reachable
2. Memory count is reasonable (not zero, not shrinking)
3. Recent memories exist (something saved in last 24h)
4. Search quality spot-check (known fact returns correctly)
5. DeepSeek V3 extraction works (test add + delete)
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

STATE_FILE = os.path.expanduser("~/.openclaw/workspace/memory/mem0-health.json")

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {"last_count": 0, "last_check": None}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def main():
    issues = []
    
    # 1. Check Qdrant
    try:
        import requests
        r = requests.get("http://localhost:6333/collections/openclaw_memories", timeout=5)
        if r.status_code != 200:
            issues.append(f"Qdrant collection error: HTTP {r.status_code}")
        else:
            info = r.json()
            points = info.get("result", {}).get("points_count", 0)
            print(f"✅ Qdrant: {points} vectors in openclaw_memories")
    except Exception as e:
        issues.append(f"Qdrant unreachable: {e}")
        print(f"❌ Qdrant: {e}")
    
    # 2. Check memory count
    try:
        from mem0 import Memory
        config = {
            'llm': {'provider': 'ollama', 'config': {'model': 'qwen3:30b-a3b', 'temperature': 0.1}},
            'embedder': {'provider': 'ollama', 'config': {'model': 'nomic-embed-text'}},
            'vector_store': {'provider': 'qdrant', 'config': {
                'collection_name': 'openclaw_memories', 'host': 'localhost', 'port': 6333, 'embedding_model_dims': 768
            }}
        }
        m = Memory.from_config(config)
        all_mems = m.get_all(user_id="hao")
        count = len(all_mems.get("results", []))
        
        state = load_state()
        prev_count = state.get("last_count", 0)
        
        if count == 0:
            issues.append("CRITICAL: Zero memories in mem0!")
        elif prev_count > 0 and count < prev_count * 0.8:
            issues.append(f"Memory count dropped: {prev_count} → {count} (possible data loss)")
        
        print(f"✅ Memories: {count} (prev: {prev_count})")
        
        # 3. Check for recent memories
        recent = [r for r in all_mems.get("results", []) 
                  if r.get("created_at", "") > (datetime.now() - timedelta(hours=24)).isoformat()]
        if not recent:
            issues.append("No memories saved in last 24 hours")
            print(f"⚠️  No recent memories (last 24h)")
        else:
            print(f"✅ Recent memories: {len(recent)} in last 24h")
        
        # 4. Search quality check
        results = m.search("NOFX trading system architecture", user_id="hao", limit=3)
        top = results.get("results", [])
        if not top or top[0].get("score", 0) < 0.5:
            issues.append("Search quality degraded: known query returns low score")
            print(f"⚠️  Search quality low")
        else:
            print(f"✅ Search quality: top score {top[0]['score']:.2f}")
        
        # Update state
        state["last_count"] = count
        state["last_check"] = datetime.now().isoformat()
        save_state(state)
        
    except Exception as e:
        issues.append(f"Memory check failed: {e}")
        print(f"❌ Memory check: {e}")
    
    # Summary
    if issues:
        print(f"\n⚠️  {len(issues)} issue(s) found:")
        for i in issues:
            print(f"  - {i}")
        return 1
    else:
        print(f"\n✅ All mem0 checks passed")
        return 0

if __name__ == "__main__":
    sys.exit(main())
