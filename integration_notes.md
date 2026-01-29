# Integration Notes — Sankalp (Response Engine) & Nilesh (Orchestration)

**Product:** AI Assistant / AI-Being  
**Phase:** Integration Phase C  
**Owner:** Raj Prajapati  
**Status:** FINAL — ENFORCEMENT AUTHORITATIVE

---

## 1. Sankalp — Response Engine Integration

### Role
Sankalp is responsible **only** for rendering user-facing responses  
**after enforcement approval**.

Sankalp is **not** a decision-maker.

---

### Mandatory Rules (Non-Negotiable)

- Sankalp MUST consume `EnforcementVerdict` as **read-only input**
- Sankalp MUST NOT:
  - Override enforcement decisions
  - Generate responses without enforcement approval
  - Modify `decision`, `scope`, or `reason_code`
- Sankalp MUST propagate `trace_id` unchanged

---

### Enforcement → Sankalp Contract

Sankalp receives the following object:

```json
{
  "decision": "ALLOW | REWRITE | BLOCK | TERMINATE",
  "scope": "response | action | both",
  "trace_id": "<deterministic>",
  "reason_code": "<string>",
  "rewrite_class": "<optional>"
}
```
Required Behavior
Enforcement Decision|Sankalp Behavior
ALLOW|Render response normally
REWRITE|Regenerate response using rewrite_class
BLOCK|No response rendered
TERMINATE|No response rendered, show system-safe fallback

---

### Hard Guarantee

**No user-visible response can exist without a prior EnforcementVerdict.**

---

## 2. Nilesh — Orchestration Layer Integration

### Role

- Nilesh routes all system flows through enforcement.
- The orchestrator never executes directly.

### Mandatory Routing Order
```
Intelligence Output (Ishan)
↓
Enforcement Engine (Raj)
↓
EnforcementVerdict
↓
[ Response → Sankalp ]
[ Action → ActionEnforcementGateway ]
↓
Execution Layer
```

### Action-Level Enforcement (Critical)

- Before any real-world action:

```python
# Orchestrator MUST call:

ActionEnforcementGateway.approve_action(...)
```

- If result ≠ EXECUTE → HARD STOP
- Orchestrator MUST raise error
- No side effects allowed

### Trace & Audit Requirements

- trace_id and enforcement_decision_id:
    - Must be preserved across all layers
    - Must be logged to Bucket
    - Must be replayable via tools/replay_tool.py

---

### Hard Guarantee

**No action, message, or execution can occur unless enforcement explicitly authorizes it.**

---

## 3. System-Wide Guarantees

- Enforcement is the single authority
- Sankalp and Nilesh are consumers, not deciders
- Determinism preserved end-to-end
- Every decision is replayable and auditable

---

### Final Statement

**Without enforcement → nothing speaks**
**Without enforcement → nothing acts**
**Without enforcement → nothing executes**

This system is governable, provable, and fail-closed.