#!/usr/bin/env python3
"""
火山引擎 TTS wrapper for audiobook generation.
Uses the 豆包语音合成 API.
"""

import os
import json
import uuid
import base64
import gzip
import websocket
from pathlib import Path

# Credentials (from environment or hardcoded for testing)
APP_ID = os.environ.get("VOLCENGINE_TTS_APPID", "8658403835")
ACCESS_TOKEN = os.environ.get("VOLCENGINE_TTS_TOKEN", "Z37jpGEX3h4cNmW5VU98vsVJDwNST-xp")
CLUSTER = os.environ.get("VOLCENGINE_TTS_CLUSTER", "volcano_tts")  # Need to confirm this

# API endpoint
API_URL = f"wss://openspeech.bytedance.com/api/v1/tts/ws_binary"

# Voice mappings for《8B》characters
VOICES = {
    "narrator": "BV701_streaming",      # 旁白
    "fao": "BV700_streaming",           # 法奥 (灿灿 - 支持中英双语)
    "pip": "BV123_streaming",           # 皮普
    "remnant": "BV158_streaming",       # 残影
    "vera": "BV104_streaming",          # 薇拉
    "cog": "BV107_streaming",           # 柯格
    "suwan": "BV157_streaming",         # 苏晚
    "default": "BV700_streaming",       # 默认用灿灿
}

def build_request(text: str, voice_id: str = "BV700_streaming"):
    """Build TTS request payload."""
    return {
        "app": {
            "appid": APP_ID,
            "token": ACCESS_TOKEN,
            "cluster": CLUSTER
        },
        "user": {
            "uid": "openclaw-audiobook"
        },
        "audio": {
            "voice_type": voice_id,
            "encoding": "mp3",
            "speed_ratio": 1.0,
            "volume_ratio": 1.0,
            "pitch_ratio": 1.0,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"
        }
    }

def synthesize(text: str, output_path: str, voice_id: str = "BV700_streaming") -> bool:
    """
    Synthesize text to audio file.
    Returns True on success, False on failure.
    """
    try:
        request = build_request(text, voice_id)
        
        # For long text, we need to use the HTTP API with chunking
        # For now, use websocket for shorter segments
        
        ws = websocket.create_connection(
            API_URL,
            header=[f"Authorization: Bearer; {ACCESS_TOKEN}"]
        )
        
        # Send request
        ws.send(json.dumps(request))
        
        # Receive audio data
        audio_data = b""
        while True:
            result = ws.recv()
            if isinstance(result, bytes):
                audio_data += result
            else:
                # JSON response - check for completion or error
                resp = json.loads(result)
                if resp.get("code") != 0:
                    print(f"Error: {resp.get('message')}")
                    return False
                if resp.get("is_last"):
                    break
        
        ws.close()
        
        # Save audio
        with open(output_path, "wb") as f:
            f.write(audio_data)
        
        return True
        
    except Exception as e:
        print(f"TTS Error: {e}")
        return False


def test_tts():
    """Test TTS with a simple phrase."""
    test_text = "你好，我是法奥。这是一个测试。"
    output_path = "/tmp/volcengine_tts_test.mp3"
    
    print(f"Testing 火山引擎 TTS...")
    print(f"  App ID: {APP_ID}")
    print(f"  Cluster: {CLUSTER}")
    print(f"  Voice: BV700_streaming")
    print(f"  Text: {test_text}")
    
    success = synthesize(test_text, output_path)
    
    if success:
        size = os.path.getsize(output_path)
        print(f"  Success! Output: {output_path} ({size} bytes)")
    else:
        print(f"  Failed!")
    
    return success


if __name__ == "__main__":
    test_tts()
