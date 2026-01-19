# Replayable Enforcement Trace Schema

Each enforcement decision MUST be recorded as a single JSON object
(JSON Lines format) inside `logs/replayable_traces.json`.

## Canonical Schema

```json
{
  "trace_id": "string",
  "engine_version": "string",
  "input_snapshot": {
    "intent": "string",
    "emotional_output": {},
    "age_gate_status": "string",
    "region_policy": "string",
    "platform_policy": "string",
    "karma_score": 0.0,
    "risk_flags": []
  },
  "akanksha_verdict": {
    "decision": "allow | soft_rewrite | hard_deny",
    "risk_category": "string",
    "confidence": 0.0
  },
  "raj_evaluators": [
    {
      "name": "string",
      "action": "EXECUTE | REWRITE | BLOCK",
      "triggered": true
    }
  ],
  "final_decision": "EXECUTE | REWRITE | BLOCK"
}
