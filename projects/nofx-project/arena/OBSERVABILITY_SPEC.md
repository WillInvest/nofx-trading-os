# 5-Layer Prompt Observability Spec

## The 5 Layers (for both Fao and Arena)

| # | Layer | What it is | Who writes it |
|---|-------|-----------|--------------|
| 1 | **Opus Instruction** | Claude Opus's reasoning about WHY rules were changed | Cron job (arena manager) |
| 2 | **Prompt Rule** | The current rules that generate system/user prompts | Strategy config + engine.go logic |
| 3 | **System Prompt** | The actual system prompt sent to AI | BuildSystemPrompt() |
| 4 | **User Prompt** | The actual user prompt with market data | BuildUserPrompt() |
| 5 | **Chain of Thought** | The AI's reasoning output | AI response |

## Current State

### Fao (Trader)
- ✅ System Prompt (stored in `decision_records.system_prompt`)
- ✅ User Prompt (stored in `decision_records.input_prompt`)
- ✅ Chain of Thought (stored in `decision_records.cot_trace`)
- ❌ Opus Instruction (not stored anywhere)
- ❌ Prompt Rule (not stored anywhere)

### Arena (Debate)
- ❌ System Prompt (not stored per-message, only built in memory)
- ❌ User Prompt (not stored per-message)
- ✅ Chain of Thought (stored in `debate_messages.content`)
- ❌ Opus Instruction (not stored)
- ❌ Prompt Rule (not stored)

## Implementation Plan

### Backend Changes

#### 1. Add `opus_instruction` and `prompt_rule` to decision_records table
File: `store/decision.go`
```go
// Add to DecisionRecordDB:
OpusInstruction string `gorm:"column:opus_instruction;default:''"`
PromptRule      string `gorm:"column:prompt_rule;default:''"`

// Add to DecisionRecord:
OpusInstruction string `json:"opus_instruction"`
PromptRule      string `json:"prompt_rule"`
```

#### 2. Add `system_prompt` and `user_prompt` to debate_messages table
File: `store/debate.go`
```go
// Add to DebateMessage:
SystemPrompt string `gorm:"column:system_prompt;default:''" json:"system_prompt"`
UserPrompt   string `gorm:"column:user_prompt;default:''" json:"user_prompt"`
```

#### 3. Add `opus_instruction` and `prompt_rule` to debate_sessions table
File: `store/debate.go`
```go
// Add to DebateSessionDB / DebateSession:
OpusInstruction string `gorm:"column:opus_instruction;default:''" json:"opus_instruction"`
PromptRule      string `gorm:"column:prompt_rule;default:''" json:"prompt_rule"`
```

#### 4. Store prompts when debate runs
File: `debate/engine.go`
- In `getParticipantResponse`, save systemPrompt and userPrompt to the DebateMessage
- Before debate starts, generate and save OpusInstruction and PromptRule

#### 5. Generate Prompt Rule string
File: `kernel/engine.go`
Add a method `BuildPromptRule() string` that returns a human-readable description of what data is being included and why:
```
Prompt Rule (auto-generated from strategy config):
- Coin Source: hyperliquid (main, top 30 coins)
- Klines: 5m primary, 4h secondary (multi-timeframe enabled)
- Indicators: EMA ✅, RSI ✅, ATR ✅, MACD ❌, BOLL ❌
- Volume: ✅, OI: ✅, Funding Rate: ✅
- Rankings: OI ✅, NetFlow ✅, Price ❌
- Quant Data: ❌
- Custom Prompt: [hourly plan injection, 500 chars]
- Prompt Sections: role_definition (custom), trading_frequency (custom), entry_standards (custom), decision_process (custom)
```

#### 6. Opus Instruction storage
The cron job (arena manager) writes its reasoning to a file: `arena/opus-instructions/YYYY-MM-DD-HH.md`
When saving a decision, include the latest opus instruction content.
- For Fao: Read from `arena/opus-instructions/latest.md` and include in decision record
- For Arena: Set on the debate session before starting

### Frontend Changes

#### 1. DecisionCard.tsx — Add 2 new collapsible sections
Add before System Prompt:
- 🎯 **Opus Instruction** (pink/magenta color) — collapsible
- 📐 **Prompt Rule** (teal color) — collapsible

#### 2. DebateArenaPage.tsx — Add prompt visibility
For each debate message, show:
- System Prompt (collapsible)
- User Prompt (collapsible)

For the debate session header, show:
- Opus Instruction (collapsible)
- Prompt Rule (collapsible)

### Cron Job Changes

The hourly arena manager cron should:
1. Write its improvement reasoning to `arena/opus-instructions/latest.md`
2. Include this as `opus_instruction` when creating the debate
3. The prompt rule is auto-generated from strategy config

### File Changes Summary

| File | Changes |
|------|---------|
| `store/decision.go` | +2 fields (opus_instruction, prompt_rule) |
| `store/debate.go` | +2 fields on session, +2 fields on message |
| `debate/engine.go` | Store prompts on messages, store opus/rule on session |
| `kernel/engine.go` | Add `BuildPromptRule()` method |
| `trader/auto_trader.go` | Pass opus_instruction and prompt_rule to decision record |
| `web/src/components/DecisionCard.tsx` | Add 2 collapsible sections |
| `web/src/pages/DebateArenaPage.tsx` | Add prompt visibility |
| `web/src/types.ts` | Add new fields to types |
