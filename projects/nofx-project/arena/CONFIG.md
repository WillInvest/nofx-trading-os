# NOFX Arena - Trading Intelligence System

## Architecture
- **Hourly Debate**: V3 Bull (3 rounds) vs V3 Bear (3 rounds) → R1 Judge → 1-Hour Plan
- **5-min Cycles**: Trader Fao reads hourly plan, makes short-term decisions
- **Hourly Review**: Claude Opus reviews debate quality, system health, prompt improvements
- **Daily Review**: Strategic overview, profitability analysis, suggestions

## Models
- DeepSeek V3 (deepseek-chat): Bull & Bear analysts
- DeepSeek R1 (deepseek-reasoner): Judge / final decision maker
- Claude Opus 4.6: Manager (reviews, improves, reports)

## IDs
- User: 34dd0d3b-bf61-4a6a-82fc-0f0af42355c1
- Strategy: 45386a53-debe-4e33-8e86-2041e50b8ed6
- DeepSeek V3: 34dd0d3b-bf61-4a6a-82fc-0f0af42355c1_deepseek
- DeepSeek R1: 34dd0d3b-bf61-4a6a-82fc-0f0af42355c1_deepseek_r1
- Trader Fao: f4f5f8d1_34dd0d3b-bf61-4a6a-82fc-0f0af42355c1_deepseek_1771480382
- JWT Secret: Fm9Dd/bc2ix30BkhbC22lKy2m/0CDjedaX/TAwkQMGc=

## API
- Backend: http://localhost:8090
- Frontend: http://localhost:3001

## Files
- arena/hourly-plan.json - Current 1-hour trading plan
- arena/debate-history/ - Past debate summaries
- arena/prompt-versions/ - Prompt improvement history
- arena/performance.json - Model performance tracking
