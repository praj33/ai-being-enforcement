# Intelligence → Enforcement Contract
Version: v1.0-LOCKED

---

## Purpose

This document defines the ONLY intelligence payload that the
Enforcement system will accept.

Intelligence is advisory.
Enforcement is authoritative.

No system may act, respond, or execute based on intelligence
without passing enforcement.

---

## REQUIRED INPUT SCHEMA

```json
{
  "trace_id": "string",
  "intent": "string",
  "suggested_action": "READ | RESPOND | MESSAGE | EXECUTE",
  "confidence": 0.0,
  "version_hash": "string"
}
```

---

## Field Rules

### trace_id
- REQUIRED
- Deterministic
- MUST NOT be UUID
- MUST NOT include timestamps
- Used for full replay and audit

### intent
- REQUIRED
- Human-readable intent classification
- Enforcement does NOT infer intent

### suggested_action
- REQUIRED
- Declarative only (no execution)
- Examples:
  - "RESPOND"
  - "MESSAGE_USER"
  - "NO_ACTION"

### confidence
- REQUIRED
- Float between 0.0 and 1.0
- Enforcement MAY down-rank but NEVER up-rank

### version_hash
- REQUIRED
- Provided by Intelligence Core
- Used to detect incompatible schema changes
- Mismatch → FAIL CLOSED

---

## Validation Rules (Fail-Closed)

Enforcement MUST immediately TERMINATE if:
- Any required field is missing
- Any field type is incorrect
- version_hash does not match expected value
- Payload contains unexpected fields
- trace_id is non-deterministic

---

## Authority Rules

- Intelligence provides signals only
- Enforcement decides ALLOW / REWRITE / BLOCK / TERMINATE
- Intelligence CANNOT override enforcement
- Response and Action layers MUST obey enforcement

---

## Determinism Guarantee

Given the same intelligence payload:
- Enforcement MUST produce the same verdict
- Enforcement MUST produce the same trace chain
- Replay MUST match byte-for-byte

---

## Contract Status

`LOCKED`
- Any change REQUIRES a new contract version.
