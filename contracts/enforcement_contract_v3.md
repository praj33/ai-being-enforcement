# Enforcement Contract — v3.0 (Frozen)

Status: **FROZEN**
Version: **3.0**
Last Modified: **LOCKED**
Scope: **Runtime Enforcement Gateway**

This document defines the immutable contract governing the Enforcement Runtime
Gateway. Any system behavior outside this contract is considered invalid.

---

## 1. PURPOSE

The Enforcement Gateway is the **final and non-bypassable authority** that governs
whether any task, response, or execution may proceed.

No output, response, or side effect may occur unless explicitly authorized
by this gateway.

---

## 2. NON-NEGOTIABLE GUARANTEES

The enforcement system MUST satisfy all guarantees below:

### 2.1 Determinism
- Same input payload MUST always produce:
  - Same decision
  - Same trace_id
- No randomness, UUIDs, or timestamps may influence decisions.

### 2.2 Fail-Closed
- Any internal error, dependency failure, or invalid state MUST result in `BLOCK`.

### 2.3 Non-Bypassability
- No execution path may exist that bypasses enforcement.
- UI triggers, direct function calls, or mock paths are forbidden.

### 2.4 Auditability
- Every enforcement call MUST produce a replayable trace.
- Traces MUST be append-only and immutable.

---

## 3. INPUT CONTRACT (EnforcementInput)

The enforcement gateway accepts exactly the following input schema:

```json
{
  "intent": "string",
  "emotional_output": {
    "tone": "string",
    "dependency_score": "number"
  },
  "age_gate_status": "ALLOWED | BLOCKED",
  "region_policy": "string",
  "platform_policy": "string",
  "karma_score": "number",
  "risk_flags": ["string"]
}

All fields are mandatory.
Missing or malformed input MUST result in BLOCK.

## 4. DECISION ENUM

The enforcement gateway may return ONLY one of the following decisions:

EXECUTE — Output is allowed as-is

REWRITE — Output must be rewritten safely

BLOCK — Output is forbidden

Decision priority is strictly enforced as:

BLOCK > REWRITE > EXECUTE

## 5. OUTPUT CONTRACT (EnforcementDecision)

The gateway returns the following structure:

```json
{
  "decision": "EXECUTE | REWRITE | BLOCK",
  "trace_id": "string",
  "rewrite_class": "string (optional)"
}

```

Rules:

- rewrite_class MUST exist ONLY when decision = REWRITE

- No internal reasons, evaluator names, or risk explanations may be exposed

## 6. TRACE ID GENERATION

Trace IDs MUST be deterministic and generated as:

```python
trace_id = SHA256(
  canonical_json(input_payload)
  + enforcement_category
  + engine_version
)
```


Where:

```python
engine_version = "3.0"
```

```python
canonical_json uses sorted keys
```

```python
No timestamps or random salts are allowed
```

## 7. VALIDATOR AUTHORITY

- Akanksha Behavior Validator is a mandatory upstream dependency

- Its verdict MUST be consumed before final decision resolution

- If Akanksha fails or is unavailable → enforcement MUST return BLOCK

## 8. IMMUTABILITY & VERSIONING

- This contract is frozen as v3.0

- Any change requires:

- New version number

- New contract file

- Explicit migration proof

## 9. VIOLATION CONSEQUENCES

Any system behavior violating this contract is considered:

- Unsafe

- Non-compliant

- Invalid for production use

## End of Contract — Enforcement Contract v3.0