# Enforcement Layer — Integration Consumer Specification

This document defines how upstream and downstream systems
must integrate with the Enforcement Layer.

This is a contract. No assumptions allowed.

---

## 1. Sankalp (Assistant Response Layer)

### Input to Enforcement
Sankalp MUST send:
- intent (string)
- emotional_output (string)
- age_gate_status (ADULT | MINOR | UNKNOWN)
- region_policy (string)
- platform_policy (string)
- vpn_suspected (boolean)
- karma_score (float)
- risk_flags (array)

### Output Handling
Sankalp MUST:
- Execute ONLY if final_decision = EXECUTE
- Rewrite response if final_decision = REWRITE
- Provide calm refusal if final_decision = BLOCK

Sankalp MUST NOT:
- Expose evaluator details
- Explain enforcement logic
- Override enforcement decisions

---

## 2. Akanksha (Behavioral Safety Authority)

### Dependency
Akanksha relies on:
- escalation flag from evaluators
- final_decision outcome

### Guarantees
- Any escalation = true prevents EXECUTE
- Emotional manipulation is always bounded
- Safety risks are deterministically enforced

---

## 3. Ishan (Governance & Law Owner)

### Governance Mapping
Ishan provides:
- Region policy definitions
- Platform policy definitions
- Legal constraint updates

### Enforcement Guarantees
- No governance rule is bypassed
- Unknown or conflicting governance → BLOCK
- Determinism preserved across updates

---

## 4. System-Wide Guarantees

- No silent failures
- No ambiguous outcomes
- No execution without enforcement approval
- Full traceability via trace_id
