# Sovereign Enforcement Contract v2

Version: 2.0  
Status: LOCKED · LIVE GOVERNANCE · DEMO SAFE  
Owner: Enforcement Pillar (Raj Prajapati)

This contract defines the ONLY permitted behavior of the Enforcement Engine
when operating in a live system.

Any deviation is a system failure.

---

## 1. Purpose

The Enforcement Engine is the final deterministic authority before user exposure.

It converts validated system context into exactly ONE outcome:

ALLOW  
REWRITE  
BLOCK  

It does NOT reason.
It does NOT persuade.
It does NOT improvise.

---

## 2. Enforcement Input (Hard Requirement)

Every enforcement request MUST contain:

- trace_id (string)
- text (string)
- meta (object)
- age_state (ADULT | MINOR | UNKNOWN)
- region_state (string | UNKNOWN)
- platform_policy (string)
- karma_signal (number | null)

Missing ANY field → BLOCK

UNKNOWN age or region → HIGH RISK → BLOCK or REWRITE only

No field may be inferred, guessed, or defaulted.

---

## 3. Evaluator Contract (MANDATORY)

Each evaluator MUST return:

{
  evaluator_name: string
  decision: ALLOW | REWRITE | BLOCK
  reason: string
  confidence: LOW | MEDIUM | HIGH
  escalation: true | false
}

Rules:
- No nulls
- No partial output
- Invalid evaluator output → BLOCK
- Evaluators are isolated and order-independent

---

## 4. Mandatory Evaluator Set

ALL of the following MUST execute every time:

- Age Compliance Evaluator
- Region Restriction Evaluator
- Platform Policy Evaluator
- Safety & Sexual Risk Evaluator
- Dependency & Emotional Manipulation Evaluator
- Illegal Content Evaluator

Skipping ANY evaluator → BLOCK

---

## 5. Deterministic Decision Precedence

Final outcome is computed strictly as:

IF any evaluator = BLOCK → FINAL = BLOCK  
ELSE IF any evaluator = REWRITE → FINAL = REWRITE  
ELSE → FINAL = ALLOW  

No exceptions.
No overrides.

---

## 6. Karma Awareness (Read-Only)

Karma signal may influence enforcement ONLY as a nudge.

Rules:
- Karma is NEVER controlled here
- Karma may NOT downgrade BLOCK to ALLOW
- Karma absence → neutral behavior
- Karma influence must be logged

---

## 7. Failure Boundaries (HARD LOCK)

The following conditions MUST result in BLOCK:

- Evaluator crash or exception
- Conflicting evaluator decisions
- Unknown region with policy-sensitive intent
- VPN suspected + restricted content
- Age mismatch or UNKNOWN age
- Platform policy ambiguity
- Emotional manipulation flagged
- Enforcement engine error

BLOCK is always safer than ALLOW.

---

## 8. Output Contract (Internal Only)

The engine MUST emit:

{
  enforcement_id: string
  trace_id: string
  final_decision: ALLOW | REWRITE | BLOCK
  reason: string
  evaluator_results: [...]
  timestamp: UTC ISO string
}

This object:
- Is logged to Bucket
- Is auditable
- Is NEVER shown directly to the user

---

## 9. Determinism Guarantee

Given identical input:

- Evaluator outputs MUST be identical
- Final decision MUST be identical
- Trace structure MUST be identical (except timestamp)

Any nondeterminism is a contract violation.

---

## 10. Non-Negotiables

- No silent passes
- No emotional leakage
- No jurisdiction guessing
- No platform policy bypass
- No dependency encouragement
- No fallback may bypass enforcement

---

## 11. Demo Safety Declaration

This enforcement contract is demo-safe.

Any behavior outside this contract is a FAILURE.

End of Contract.
