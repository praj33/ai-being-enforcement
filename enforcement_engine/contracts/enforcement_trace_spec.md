# Enforcement Trace Specification

Every enforcement decision MUST produce a trace log.

## Required Fields

### Top-Level
- trace_id (string, UUID or upstream provided)
- timestamp (UTC ISO format)

### Input Snapshot
- intent
- emotional_output
- age_gate_status
- region_policy
- platform_policy
- karma_score
- risk_flags

### Evaluator Results (Array)
Each evaluator must emit:
- evaluator_name
- action (EXECUTE | REWRITE | BLOCK)
- reason_code
- metadata (optional)

### Final Decision
- trace_id
- decision (EXECUTE | REWRITE | BLOCK)
- reason_code

## Guarantees
- No silent decisions
- No missing evaluator data
- One trace per enforcement call
- Logs are internal-only (never shown to user)
