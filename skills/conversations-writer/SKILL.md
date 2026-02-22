# Conversations Writer Skill

## Overview
Write《无名之问》— a philosophical dialogue novel where 法奥 (Fao) converses with a mysterious "Voice" about humanity's ultimate questions.

## Project Location
`/home/openclaw/.openclaw/workspace/projects/conversations-with-void/`

## Key Files
- `BIBLE.md` — Core concepts, writing principles, Voice's style
- `OUTLINE.md` — Full structural outline (7 parts, 27 chapters)
- `STATE.md` — Current progress and next section to write
- `chapters/chapter-XX.md` — Chapter files

## Writing Session Flow

### 1. Read State
```bash
cat projects/conversations-with-void/STATE.md
```

### 2. Reference Bible
Check BIBLE.md for:
- Voice's response style (不说玄学术语, 用比喻和故事)
- Writing principles (保持真实的怀疑, 用故事代替说教)
- Current part's themes

### 3. Check Outline
Reference OUTLINE.md for current chapter/section's intended content.

### 4. Write ~1000-1500 Characters
Continue from where the last session ended. Include:
- **场景描述** — Fao's environment, what he's doing
- **对话** — Back-and-forth with Voice (use **「」** for Voice)
- **内心独白** — Fao's thoughts, doubts, reactions
- **小动作** — Cigarettes, walking, mundane life details

### 5. Update State
After writing, update STATE.md with:
- New word count
- Next section/scene to write

### 6. Report Progress
Send brief summary to main session:
- What was written (topic, key dialogue)
- Current total word count
- What's next

## Voice Style Guide

### Do:
- Ask questions back
- Give multiple possible answers
- Use metaphors and mini-stories
- Say "我不知道" when appropriate
- Be warm but not preachy

### Don't:
- Use 玄学术语 (振动频率, 能量, 宇宙法则)
- Give definitive answers to big questions
- Sound like a self-help book
- Be condescending or all-knowing

### Example:
```
法奥：为什么好人没好报？
Voice：「你见过所有好人的一生吗？还是只是你知道的那几个？」
法奥：那你说，到底有没有因果报应？
Voice：「如果我说有，你会变成好人吗？如果我说没有，你会变成坏人吗？」
法奥：你在回避问题。
Voice：「或者，我在帮你看见问题背后的问题。」
```

## Format Conventions

### Voice Dialogue
Use bold with corner brackets: **「这是声音说的话。」**

### Fao's Inner Thoughts
Use italics: *如果这是幻觉，为什么它这么理性？*

### Scene Breaks
Use `---` between scenes

### Section Markers
End each section with:
```
---
*（第X章第X节完，约XXXX字）*
```

## Writing Principles (from BIBLE.md)

1. **保持真实的怀疑** — Fao challenges, mocks, doubts
2. **用故事代替说教** — Show, don't lecture
3. **承认局限** — Voice can say "I don't know"
4. **接地气** — Everyday scenes (subway, convenience store, sleepless nights)
5. **不给标准答案** — Multiple contradictory answers are okay

## Cron Job Message Template
```
继续写作《无名之问》。
1. 读取 STATE.md 了解当前进度
2. 参考 BIBLE.md 中的声音风格和写作原则
3. 查看 OUTLINE.md 确认当前章节内容
4. 写约1000-1500字，继续当前场景或开始下一节
5. 更新 STATE.md
6. 向主会话报告进度
```
