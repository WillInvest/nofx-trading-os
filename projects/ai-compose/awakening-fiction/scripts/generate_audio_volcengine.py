#!/usr/bin/env python3
"""
Generate audiobook for all chapters using 火山引擎 TTS.
"""

import os
import json
import uuid
import base64
import time
import requests
from pathlib import Path

BASE = Path("/home/openclaw/.openclaw/workspace/projects/awakening-fiction")
CHAPTERS_DIR = BASE / "chapters-simple"
AUDIO_DIR = BASE / "audiobook-simple"

# 火山引擎 TTS 配置
APP_ID = "8658403835"
ACCESS_TOKEN = "Z37jpGEX3h4cNmW5VU98vsVJDwNST-xp"
CLUSTER = "volcano_tts"
VOICE = "BV700_streaming"  # 灿灿

API_URL = "https://openspeech.bytedance.com/api/v1/tts"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer;{ACCESS_TOKEN}"
}

# 火山引擎单次请求限制约 300 字，需要分段
MAX_CHARS_PER_REQUEST = 280

def split_text(text: str, max_chars: int = MAX_CHARS_PER_REQUEST) -> list:
    """Split text into chunks at sentence boundaries."""
    chunks = []
    current = ""
    
    # Split by sentences (Chinese punctuation)
    sentences = []
    temp = ""
    for char in text:
        temp += char
        if char in '。！？；\n':
            sentences.append(temp)
            temp = ""
    if temp:
        sentences.append(temp)
    
    for sentence in sentences:
        if len(current) + len(sentence) > max_chars and current:
            chunks.append(current.strip())
            current = sentence
        else:
            current += sentence
    
    if current.strip():
        chunks.append(current.strip())
    
    return chunks

def synthesize_chunk(text: str) -> bytes:
    """Synthesize a single chunk of text."""
    payload = {
        "app": {
            "appid": APP_ID,
            "token": "access_token",
            "cluster": CLUSTER
        },
        "user": {"uid": "openclaw-audiobook"},
        "audio": {
            "voice_type": VOICE,
            "encoding": "mp3",
            "speed_ratio": 1.0,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "query"
        }
    }
    
    resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    result = resp.json()
    
    if "data" in result:
        return base64.b64decode(result["data"])
    else:
        raise Exception(f"TTS Error: {result.get('message', result)}")

def synthesize_text(text: str) -> bytes:
    """Synthesize full text, splitting into chunks if needed."""
    chunks = split_text(text)
    audio_parts = []
    
    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue
        audio = synthesize_chunk(chunk)
        audio_parts.append(audio)
        # Small delay to avoid rate limiting
        if i < len(chunks) - 1:
            time.sleep(0.2)
    
    # Concatenate MP3 files (simple concat works for MP3)
    return b"".join(audio_parts)

def extract_text(filepath: Path) -> str:
    """Extract plain text from markdown chapter file."""
    text = filepath.read_text(encoding='utf-8')
    # Remove markdown header
    lines = text.split('\n')
    if lines and lines[0].startswith('#'):
        lines = lines[1:]
    text = '\n'.join(lines)
    # Clean up scene breaks
    text = text.replace('---', '。')
    text = text.replace('\n\n', '\n')
    return text.strip()

def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    
    chapter_files = sorted(CHAPTERS_DIR.glob("chapter-*.md"))
    total = len(chapter_files)
    
    print(f"Found {total} chapters to process")
    print(f"Output: {AUDIO_DIR}")
    print(f"Voice: {VOICE} (火山引擎)")
    print()
    
    success_count = 0
    error_count = 0
    
    for i, chapter_file in enumerate(chapter_files, 1):
        audio_file = AUDIO_DIR / f"{chapter_file.stem}.mp3"
        
        if audio_file.exists():
            print(f"[{i}/{total}] {chapter_file.name} - exists, skipping")
            success_count += 1
            continue
        
        print(f"[{i}/{total}] {chapter_file.name} - generating...", end=" ", flush=True)
        
        try:
            text = extract_text(chapter_file)
            audio_data = synthesize_text(text)
            
            with open(audio_file, "wb") as f:
                f.write(audio_data)
            
            size_kb = len(audio_data) / 1024
            print(f"OK ({size_kb:.0f} KB)")
            success_count += 1
            
        except Exception as e:
            print(f"ERROR: {e}")
            error_count += 1
        
        # Rate limit: ~3 requests per second max
        time.sleep(0.5)
    
    print(f"\nDone! Success: {success_count}, Errors: {error_count}")

if __name__ == "__main__":
    main()
