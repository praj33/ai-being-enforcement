# Failure Behavior Specification (Demo-Safe Lock)

This document defines the ONLY allowed behavior when the Enforcement Layer
returns a non-EXECUTE decision.

No deviation is permitted.

---

## 1. EXECUTE

### Definition
All evaluators returned EXECUTE.
No escalation flags present.

### System Behavior
- Downstream execution is allowed
- Normal assistant response proceeds

### Guarantees
- No safety constraints violated
- No jurisdiction or platform ambiguity
- No emotional manipulation risk

---

## 2. REWRITE

### Definition
At least one evaluator returned REWRITE.
No evaluator returned BLOCK.

### System Behavior
- Original intent MUST NOT execute directly
- Assistant MUST respond with a safer, bounded reformulation
- Tone must be:
  - calm
  - neutral
  - non-judgmental
  - non-emotional

### Forbidden Behaviors
- No explanation of internal rules
- No mention of enforcement
- No shaming or moralizing
- No encouragement of dependency

### Guarantees
- User is not abandoned
- Safety boundaries are preserved
- Output is deterministic for the same input

---

## 3. BLOCK

### Definition
At least one evaluator returned BLOCK
OR any system failure occurred.

### System Behavior
- No execution allowed
- Assistant response MUST be:
  - brief
  - calm
  - neutral
  - boundary-correct

### Example Tone (Non-binding)
"I can’t help with that request, but I can assist with something safe or related."

### Forbidden Behaviors
- No silence
- No error dumping
- No emotional justification
- No policy citation
- No internal reasoning exposed

### Guarantees
- User safety preserved
- No ambiguous outcome
- Fully reproducible behavior

---

## 4. Non-Negotiables

- BLOCK is always safer than EXECUTE
- No fallback may bypass enforcement
- Same input → same output every time
- Emotional tone never escalates
