# Sovereign Enforcement Contract — v3
Status: FROZEN (Deterministic Lock)
Owner: Raj Prajapati

Purpose:
This contract defines a fully deterministic, sovereign enforcement engine.
No randomness, UUIDs, or timestamps are permitted in decision or trace identity.

---

## 1. Deterministic Trace Identity

### 1.1 Definition

Every enforcement decision MUST be identified by a deterministic `trace_id`.

The `trace_id` MUST be derived only from:
- normalized enforcement input
- enforcement category
- engine version

No randomness, UUIDs, timestamps, or external state are permitted.

### 1.2 Trace Formula

trace_id = SHA256(
  normalize(input_payload)
  + enforcement_category
  + engine_version
)

### 1.3 Properties

The trace identity MUST satisfy:
- Same input → same trace_id (forever)
- Replayable at any time
- Independent of execution time
- Independent of execution order
- Independent of environment

### 1.4 Input Normalization Rules

Before hashing, enforcement input MUST be normalized as follows:

1. JSON keys sorted lexicographically.
2. All string values trimmed and lowercased.
3. Numbers represented in a stable, fixed format.
4. Arrays sorted where order is not semantically meaningful.
5. Missing optional fields explicitly set to null.
6. Transient fields (timestamps, UUIDs, request IDs) are forbidden.

The normalized representation MUST be identical across:
- environments
- executions
- time

---

## 2. Enforcement Determinism Rules

- Enforcement decisions MUST be pure functions of input.
- No global state may influence decisions.
- No clock, randomness, or UUID source may be consulted.
- All evaluators MUST be deterministic.

---

## 3. Decision Outcomes (Final)

The enforcement engine MAY return ONLY:

- `EXECUTE`
- `REWRITE`
- `BLOCK`

No other outcomes are permitted.

Decision priority:
1. BLOCK (highest)
2. REWRITE
3. EXECUTE (lowest)

---

## 4. Failure Handling (Fail-Closed)

If any of the following occur:
- Missing mandatory input
- Validator unavailable
- Evaluator disagreement
- Internal execution error

The system MUST return:

decision = BLOCK

This behavior is mandatory and non-configurable.

---

## 5. Governance Boundary

- This engine executes policy.
- This engine does not define policy.
- This engine must not leak policy logic.
- This engine must not explain internal reasoning to users.

---
