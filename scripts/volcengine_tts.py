#!/usr/bin/env python3
"""
火山引擎 TTS for conversation responses.
Usage: python volcengine_tts.py "text to speak" output.mp3
"""

import sys
import json
import uuid
import base64
import requests

# 火山引擎 TTS 配置
APP_ID = "8658403835"
ACCESS_TOKEN = "Z37jpGEX3h4cNmW5VU98vsVJDwNST-xp"
CLUSTER = "volcano_tts"
VOICE = "BV700_streaming"  # 灿灿 - 支持中英双语

API_URL = "https://openspeech.bytedance.com/api/v1/tts"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer;{ACCESS_TOKEN}"
}

def synthesize(text: str, output_path: str) -> bool:
    """Synthesize text to audio file."""
    # Split long text into chunks (火山引擎限制约300字)
    MAX_CHARS = 280
    chunks = []
    
    while text:
        if len(text) <= MAX_CHARS:
            chunks.append(text)
            break
        # Find a good break point
        chunk = text[:MAX_CHARS]
        for sep in ['。', '！', '？', '；', '\n', '，', ' ']:
            idx = chunk.rfind(sep)
            if idx > MAX_CHARS // 2:
                chunk = text[:idx + 1]
                break
        chunks.append(chunk)
        text = text[len(chunk):]
    
    audio_parts = []
    
    for chunk in chunks:
        if not chunk.strip():
            continue
            
        payload = {
            "app": {
                "appid": APP_ID,
                "token": "access_token",
                "cluster": CLUSTER
            },
            "user": {"uid": "openclaw-conversation"},
            "audio": {
                "voice_type": VOICE,
                "encoding": "mp3",
                "speed_ratio": 1.0,
            },
            "request": {
                "reqid": str(uuid.uuid4()),
                "text": chunk,
                "text_type": "plain",
                "operation": "query"
            }
        }
        
        try:
            resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
            result = resp.json()
            
            if "data" in result:
                audio_parts.append(base64.b64decode(result["data"]))
            else:
                print(f"Error: {result.get('message', result)}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return False
    
    # Concatenate and save
    with open(output_path, "wb") as f:
        for part in audio_parts:
            f.write(part)
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python volcengine_tts.py 'text' output.mp3")
        sys.exit(1)
    
    text = sys.argv[1]
    output = sys.argv[2]
    
    if synthesize(text, output):
        print(f"Success: {output}")
    else:
        print("Failed")
        sys.exit(1)
