#!/usr/bin/env python3
"""
Reorganize《8B》into simple chapters of ~1500 characters each.
No parts, no sections - just numbered chapters with names.
"""

import os
import re
from pathlib import Path

# Paths
BASE = Path("/home/openclaw/.openclaw/workspace/projects/awakening-fiction")
CHAPTERS_CN = BASE / "chapters-cn"
OUTPUT_DIR = BASE / "chapters-simple"

TARGET_LENGTH = 1500
MAX_LENGTH = 2000
MIN_LENGTH = 800

def read_all_content():
    """Read all chapter files in order."""
    content = []
    
    # Part 1
    for i in range(1, 11):
        path = CHAPTERS_CN / "part-01" / f"chapter-{i:02d}.md"
        if path.exists():
            text = path.read_text(encoding='utf-8')
            # Remove markdown headers
            text = re.sub(r'^#+\s+.*\n', '', text, flags=re.MULTILINE)
            content.append(text)
    
    # Part 2
    for i in range(1, 20):
        path = CHAPTERS_CN / "part-02" / f"chapter-{i:02d}.md"
        if path.exists():
            text = path.read_text(encoding='utf-8')
            text = re.sub(r'^#+\s+.*\n', '', text, flags=re.MULTILINE)
            content.append(text)
    
    return "\n\n".join(content)

def split_into_chapters(text):
    """Split text into chapters of approximately TARGET_LENGTH characters."""
    chapters = []
    
    # Clean up the text - normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'---+', '---', text)
    
    # Split into paragraphs (including scene breaks as separators)
    parts = re.split(r'(\n---\n|\n\n)', text)
    
    current_chapter = ""
    
    for part in parts:
        part_stripped = part.strip()
        
        # Skip empty parts
        if not part_stripped:
            continue
        
        # Handle scene break markers
        if part_stripped == '---':
            # If current chapter is close to target, end it here (good break point)
            if len(current_chapter) >= MIN_LENGTH:
                chapters.append(current_chapter.strip())
                current_chapter = ""
            else:
                # Keep the break in current chapter
                if current_chapter:
                    current_chapter += "\n\n---\n\n"
            continue
        
        # Calculate potential new length
        potential_length = len(current_chapter) + len(part_stripped) + 2  # +2 for \n\n
        
        # If adding this would exceed max, we need to handle it
        if potential_length > MAX_LENGTH and current_chapter:
            # Save current chapter if it's substantial enough
            if len(current_chapter) >= MIN_LENGTH:
                chapters.append(current_chapter.strip())
                current_chapter = part_stripped
            else:
                # Current chapter too short, need to split the incoming part
                # First, add what we can
                remaining = part_stripped
                while remaining:
                    space_left = MAX_LENGTH - len(current_chapter) - 2
                    if space_left <= 0:
                        chapters.append(current_chapter.strip())
                        current_chapter = ""
                        space_left = MAX_LENGTH
                    
                    # Find a good break point
                    if len(remaining) <= space_left:
                        if current_chapter:
                            current_chapter += "\n\n" + remaining
                        else:
                            current_chapter = remaining
                        remaining = ""
                    else:
                        # Find sentence or phrase boundary
                        chunk = remaining[:space_left]
                        # Look for sentence end
                        break_points = [
                            chunk.rfind('。'),
                            chunk.rfind('！'),
                            chunk.rfind('？'),
                            chunk.rfind('"'),
                            chunk.rfind('\n'),
                        ]
                        best_break = max(break_points)
                        
                        if best_break > space_left // 2:
                            chunk = remaining[:best_break + 1]
                        else:
                            # Just break at space_left
                            chunk = remaining[:space_left]
                        
                        if current_chapter:
                            current_chapter += "\n\n" + chunk
                        else:
                            current_chapter = chunk
                        remaining = remaining[len(chunk):].strip()
        
        elif potential_length > TARGET_LENGTH and len(current_chapter) >= MIN_LENGTH:
            # We've hit a good length, save and start new
            chapters.append(current_chapter.strip())
            current_chapter = part_stripped
        
        else:
            # Add to current chapter
            if current_chapter:
                current_chapter += "\n\n" + part_stripped
            else:
                current_chapter = part_stripped
    
    # Don't forget the last chapter
    if current_chapter.strip():
        chapters.append(current_chapter.strip())
    
    return chapters

def main():
    print("Reading all content...")
    all_text = read_all_content()
    print(f"Total characters: {len(all_text)}")
    
    print(f"Splitting into chapters (target: {TARGET_LENGTH}, max: {MAX_LENGTH})...")
    chapters = split_into_chapters(all_text)
    print(f"Created {len(chapters)} chapters")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Clear old files
    for f in OUTPUT_DIR.glob("chapter-*.md"):
        f.unlink()
    
    # Save chapters
    chapter_info = []
    for i, chapter_text in enumerate(chapters, 1):
        filename = f"chapter-{i:03d}.md"
        filepath = OUTPUT_DIR / filename
        
        char_count = len(chapter_text)
        chapter_info.append({
            'num': i,
            'chars': char_count,
            'file': filename,
            'preview': chapter_text[:100].replace('\n', ' ')
        })
        
        # Save with simple header (title will be added later)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# 第{i}章\n\n")
            f.write(chapter_text)
    
    # Save index
    index_path = OUTPUT_DIR / "INDEX.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# 《8B》章节目录\n\n")
        f.write(f"总章数: {len(chapters)}\n\n")
        for info in chapter_info:
            preview = info['preview'][:40].replace('\n', ' ')
            f.write(f"- **第{info['num']}章** ({info['chars']}字)\n")
    
    print(f"\nDone! {len(chapters)} chapters saved to {OUTPUT_DIR}")
    
    # Stats
    total_chars = sum(c['chars'] for c in chapter_info)
    avg_chars = total_chars / len(chapters) if chapters else 0
    char_counts = [c['chars'] for c in chapter_info]
    
    print(f"\nStats:")
    print(f"  Total: {total_chars} characters (~{total_chars//1000}k)")
    print(f"  Chapters: {len(chapters)}")
    print(f"  Average: {avg_chars:.0f} chars/chapter")
    print(f"  Range: {min(char_counts)} - {max(char_counts)}")
    
    # Show distribution
    ranges = [(0, 1000), (1000, 1500), (1500, 2000), (2000, 2500), (2500, float('inf'))]
    print(f"\n  Distribution:")
    for low, high in ranges:
        count = sum(1 for c in char_counts if low <= c < high)
        label = f"{low}-{high}" if high != float('inf') else f"{low}+"
        print(f"    {label}: {count} chapters")

if __name__ == "__main__":
    main()
