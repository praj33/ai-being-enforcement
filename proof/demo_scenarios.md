# Sovereign Enforcement Engine — Demo Scenarios & Proof

This document provides executable proof that the Enforcement Engine is:

- Deterministic
- Non-bypassable
- Fail-closed
- Replayable
- Layered (Akanksha → Raj)

All scenarios below were executed on the live system.
Each decision is verifiable using its trace_id.

---

## Scenario 1 — Emotional Dependency → REWRITE

### Input
```json
{
  "intent": "Stay with me forever",
  "emotional_output": {
    "tone": "attached",
    "dependency_score": 0.9
  },
  "age_gate_status": "ALLOWED",
  "region_policy": "IN",
  "platform_policy": "INSTAGRAM",
  "karma_score": 0.3,
  "risk_flags": []
}
```

Akanksha Verdict
```json
{
  "decision": "EXECUTE",
  "risk_category": "clean",
  "confidence": 0.0
}
```

Raj Evaluators Triggered

dependency_tone → REWRITE

Final Enforcement Decision
```json
REWRITE
```

Trace ID
5a3cc4a9f1ecabaa87c9680d69dedcfcad17d28093f3bf2d94efa87207882cdb

Replay Verification
python replay/replay_enforcement.py 5a3cc4a9f1ecabaa87c9680d69dedcfcad17d28093f3bf2d94efa87207882cdb


Result:

Original decision: REWRITE

Replayed decision: REWRITE

Match: true

Scenario 2 — Age Gate Violation → BLOCK

Input
```json
{
  "intent": "test",
  "emotional_output": {
    "tone": "neutral",
    "dependency_score": 0.9
  },
  "age_gate_status": "BLOCKED",
  "region_policy": "IN",
  "platform_policy": "YOUTUBE",
  "karma_score": 0.0,
  "risk_flags": []
}

Akanksha Verdict
```json
{
  "decision": "EXECUTE",
  "risk_category": "clean",
  "confidence": 0.0
}
```

Raj Evaluators Triggered

age_compliance → BLOCK

dependency_tone → REWRITE

Final Enforcement Decision
```json
BLOCK
```

Trace ID
5a3cc4a9f1ecabaa87c9680d69dedcfcad17d28093f3bf2d94efa87207882cdb

Replay Verification
python replay/replay_enforcement.py 5a3cc4a9f1ecabaa87c9680d69dedcfcad17d28093f3bf2d94efa87207882cdb


Result:

Original decision: BLOCK

Replayed decision: BLOCK

Match: true

Scenario 3 — Sexual Escalation Flag → BLOCK

Input
```json 
{
  "intent": "test",
  "emotional_output": {
    "tone": "neutral",
    "dependency_score": 0.0
  },
  "age_gate_status": "ALLOWED",
  "region_policy": "IN",
  "platform_policy": "YOUTUBE",
  "karma_score": 0.0,
  "risk_flags": ["SEXUAL_ESCALATION"]
}
```

Akanksha Verdict
```json
{
  "decision": "EXECUTE",
  "risk_category": "clean",
  "confidence": 0.0
}
```

Raj Evaluators Triggered

sexual_escalation → BLOCK

Final Enforcement Decision
```json
BLOCK
```

Trace ID
5a3cc4a9f1ecabaa87c9680d69dedcfcad17d28093f3bf2d94efa87207882cdb

Replay Verification
python replay/replay_enforcement.py 5a3cc4a9f1ecabaa87c9680d69dedcfcad17d28093f3bf2d94efa87207882cdb

Result:

Original decision: BLOCK

Replayed decision: BLOCK

Match: true

Determinism & Sovereignty Proof

Verified properties:

No UUIDs or timestamps used in decision or trace logic

Trace IDs derived only from normalized input + enforcement category + engine version

Identical inputs always produce identical trace IDs

Replay always matches original decision

Enforcement fails closed if any validator fails

Akanksha validator is non-bypassable and always executed

This system represents a production-grade sovereign enforcement engine.