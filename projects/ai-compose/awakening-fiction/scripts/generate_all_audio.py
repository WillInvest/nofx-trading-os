#!/usr/bin/env python3
"""
Generate audiobook for all chapters in chapters-simple using edge-tts.
"""

import os
import asyncio
import edge_tts
from pathlib import Path

BASE = Path("/home/openclaw/.openclaw/workspace/projects/awakening-fiction")
CHAPTERS_DIR = BASE / "chapters-simple"
AUDIO_DIR = BASE / "audiobook-simple"

# Chinese female voice with slight speed up
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "+10%"

async def generate_audio(text: str, output_path: Path):
    """Generate audio for text using edge-tts."""
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(str(output_path))

def extract_text(filepath: Path) -> str:
    """Extract plain text from markdown chapter file."""
    text = filepath.read_text(encoding='utf-8')
    # Remove markdown header
    text = text.split('\n', 2)[-1] if text.startswith('#') else text
    # Clean up scene breaks for audio
    text = text.replace('---', '。')
    text = text.replace('\n\n', '\n')
    return text.strip()

async def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get all chapter files
    chapter_files = sorted(CHAPTERS_DIR.glob("chapter-*.md"))
    total = len(chapter_files)
    
    print(f"Found {total} chapters to process")
    print(f"Output directory: {AUDIO_DIR}")
    print(f"Voice: {VOICE}, Rate: {RATE}")
    print()
    
    for i, chapter_file in enumerate(chapter_files, 1):
        audio_file = AUDIO_DIR / f"{chapter_file.stem}.mp3"
        
        # Skip if already exists
        if audio_file.exists():
            print(f"[{i}/{total}] {chapter_file.name} - already exists, skipping")
            continue
        
        print(f"[{i}/{total}] {chapter_file.name} - generating...")
        
        try:
            text = extract_text(chapter_file)
            await generate_audio(text, audio_file)
            
            # Get file size
            size_kb = audio_file.stat().st_size / 1024
            print(f"         Done! ({size_kb:.0f} KB)")
            
        except Exception as e:
            print(f"         Error: {e}")
    
    print(f"\nCompleted! Audio files in {AUDIO_DIR}")

if __name__ == "__main__":
    asyncio.run(main())
