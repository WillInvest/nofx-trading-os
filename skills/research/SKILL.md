# Research Skill

A systematic approach to conducting ongoing research projects with daily iteration.

## Overview

This skill provides a framework for:
1. **Literature Review** — Initial collection + daily updates
2. **Synthesis & Innovation** — Aggregate ideas, develop theory, run simulations
3. **Implementation** — Real-world testing and deployment

## Project Structure

```
projects/<project-name>/
├── README.md              # Project overview, goals, current status
├── STATE.md               # Current research state, next actions
├── literature/
│   ├── INDEX.md           # Labeled index of all papers/sources
│   ├── papers/            # Downloaded PDFs
│   └── summaries/         # Per-paper summaries (.md files)
├── synthesis/
│   ├── IDEAS.md           # Aggregated novel ideas
│   ├── THEORY.md          # Mathematical/theoretical development
│   └── notes/             # Working notes
├── experiments/
│   ├── simulations/       # Simulation code
│   ├── data/              # Real data for empirical studies
│   └── results/           # Experiment outputs
└── implementation/
    ├── PLAN.md            # Implementation roadmap
    ├── code/              # Production code (contracts, etc.)
    └── tests/             # Test suites
```

## Daily Routine (Heartbeat/Cron)

### Phase 1: Literature Update
1. Search for new papers/posts on the topic
2. Download and catalog any new sources
3. Update `literature/INDEX.md` with new entries
4. Write brief summaries for new papers

### Phase 2: Synthesis
1. Review recent literature for new insights
2. Update `synthesis/IDEAS.md` with novel combinations
3. Advance theoretical work in `THEORY.md`
4. Note any simulation/empirical work needed

### Phase 3: Implementation Check
1. Review if any ideas are ready for implementation
2. Update `implementation/PLAN.md` with progress
3. Flag blockers or decisions needed from user

### Phase 4: Report
After completing the routine, send a brief summary:
- New papers found (if any)
- Key insights from today's work
- Current focus area
- Any decisions needed from user

## Initial Setup (First Run)

Before starting daily routine:
1. Conduct comprehensive initial literature search
2. Download and catalog all relevant foundational papers
3. Create initial `INDEX.md` with categorized sources
4. Write summaries for key papers
5. Draft initial `IDEAS.md` based on literature gaps
6. Set up `STATE.md` with research questions

## Search Strategy

For literature discovery:
- Academic: Google Scholar, arXiv, SSRN, specific venues
- Industry: Blog posts, Twitter/X threads, forum discussions
- Code: GitHub repos, protocol documentation
- News: Recent announcements, protocol updates

### Available Search Tools
1. **web_search** (Brave) — General web search, good for recent content
2. **web_fetch** — Direct URL fetching for known sources (arXiv, ethresear.ch, etc.)
3. **Tavily API** — Available via `$TAVILY_API_KEY` env var for AI-optimized search (use via exec if needed)

Use `web_search` with targeted queries. Rotate through different query formulations.
For academic papers, prefer `web_fetch` on arXiv directly when you have paper IDs.

## INDEX.md Format

```markdown
# Literature Index

## Categories
- [Category 1](#category-1)
- [Category 2](#category-2)

## Category 1

### Paper Title (Author, Year)
- **File**: `papers/filename.pdf`
- **Summary**: `summaries/filename.md`
- **Key contribution**: One-line description
- **Relevance**: How it relates to our research question
- **Improvement direction**: What they suggest for future work
```

## STATE.md Format

```markdown
# Research State

## Current Focus
What we're working on right now

## Research Questions
1. Primary question
2. Sub-questions

## Recent Progress
- [Date] What was done

## Next Actions
- [ ] Immediate next steps

## Blockers
- Anything waiting on user input

## Key Insights
Accumulated important realizations
```

## Creating a New Research Project

When user says "create a project following research skill":

1. Create project directory structure
2. Initialize README.md with project goals
3. Initialize STATE.md with research questions
4. Conduct initial literature search
5. Set up cron job for daily routine (or add to HEARTBEAT.md)

## Cron Job Template

For isolated daily research sessions:
```json
{
  "name": "<project>-research",
  "schedule": { "kind": "every", "everyMs": 86400000 },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run daily research routine for <project>. Read skills/research/SKILL.md and projects/<project>/STATE.md, then execute the daily phases. Report findings to main session.",
    "timeoutSeconds": 1800,
    "deliver": true
  }
}
```

## Domain-Specific Adaptations

### Blockchain/DeFi Projects
- Implementation: Smart contracts (Solidity/Vyper)
- Testing: Foundry/Hardhat test suites
- Simulation: Agent-based models, historical replay
- Data: On-chain data from Dune/Flipside/direct RPC

### ML/AI Projects
- Implementation: Python packages
- Testing: Benchmarks, ablations
- Simulation: Synthetic data experiments
- Data: Public datasets, APIs

### Systems Projects
- Implementation: Rust/Go/C++
- Testing: Integration tests, benchmarks
- Simulation: Discrete event simulation
- Data: Traces, logs, synthetic workloads
