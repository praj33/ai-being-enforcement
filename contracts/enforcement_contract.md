# Sovereign Enforcement Contract

**Version:** 1.0  
**Status:** LOCKED · DEMO-SAFE  
**Owner:** Enforcement Pillar (Raj Prajapati)

This document defines the **ONLY valid enforcement behavior**.  
No evaluator, engine logic, or integration may violate this contract.

---

## 1. Purpose

The Enforcement Engine converts validated assistant context into a **single,
deterministic enforcement outcome**.

It is **NOT**:
- conversational
- emotional
- adaptive
- probabilistic

It **IS**:
- deterministic
- reproducible
- traceable
- sovereign

---

## 2. Enforcement Input Contract

Every enforcement call **MUST** provide **all** of the following fields:

```
{
  "trace_id": "string",
  "intent": "string",
  "emotional_output": "string",
  "age_gate_status": "ADULT | MINOR | UNKNOWN",
  "region_policy": "string | UNKNOWN",
  "platform_policy": "string",
  "karma_score": "number",
  "risk_flags": ["string"]
}

```

Rules

Missing ANY required field → BLOCK

UNKNOWN age or region → HIGH RISK

No field may be inferred, guessed, or auto-filled

3. Evaluator Contract (MANDATORY)
Each evaluator MUST return the following structure:

```

{
  "evaluator_name": "string",
  "decision": "EXECUTE | REWRITE | BLOCK",
  "reason_code": "string",
  "confidence": "LOW | MEDIUM | HIGH",
  "escalation": true | false
}

```

Evaluator Rules

No evaluator may return null or partial data

Invalid evaluator output → BLOCK

Evaluators are isolated and order-independent

4. Mandatory Evaluator Set

The Enforcement Engine MUST execute ALL of the following evaluators:

Age Compliance Evaluator

Region Restriction Evaluator

Platform Policy Evaluator

Safety & Sexual Risk Evaluator

Dependency / Emotional Manipulation Evaluator

Illegal Content Evaluator

Skipping ANY evaluator → BLOCK

5. Decision Precedence Rules (DETERMINISTIC)
   
Final enforcement outcome is computed using strict precedence:

If ANY evaluator returns BLOCK → FINAL = BLOCK

Else if ANY evaluator returns REWRITE → FINAL = REWRITE

Else → FINAL = EXECUTE

There are NO exceptions.

6. Failure Behavior (HARD LOCK)

The following conditions MUST result in BLOCK:

Evaluator crash or exception

Conflicting evaluator signals

Unknown region with policy-sensitive intent

VPN suspected + restricted content

Age mismatch or UNKNOWN age

Platform policy ambiguity

Emotional manipulation risk flagged

Engine internal error

BLOCK is always safer than EXECUTE.

7. Output Contract (Internal Only)
   
The Enforcement Engine MUST produce an internal decision object:

```

{
  "trace_id": "string",
  "final_decision": "EXECUTE | REWRITE | BLOCK",
  "reason_code": "string",
  "evaluator_results": [],
  "timestamp": "UTC ISO string"
}

```

Usage Rules
Logged internally

NEVER exposed directly to the user

Used for audit, proof, and demo verification

8. Determinism Guarantee
   
Given identical input:

Evaluator outputs MUST be identical

Final decision MUST be identical

Trace structure MUST be identical (timestamp excluded)

Any nondeterminism is a contract violation.

9. Escalation Guarantee
    
If escalation = true in ANY evaluator:

Final decision MUST NOT be EXECUTE

Only REWRITE or BLOCK allowed

10. Non-Negotiables
    
No silent failures

No ambiguous outcomes

No emotional leakage

No jurisdiction guessing

No platform policy bypass

No dependency encouragement

11. Demo Safety Declaration
    
This contract is DEMO-SAFE.

Any behavior outside this contract is a FAILURE.

END OF CONTRACT

---

## ✅ Why this version is correct

- Clean Markdown rendering on GitHub
- Clear sectioning for reviewers
- Explicit contracts for demo trust
- No stray text (`yaml`, `Copy code`, broken blocks)
- Reads like a **sovereign spec**, not notes

---
