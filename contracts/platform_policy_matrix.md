# Platform Policy Matrix (Locked)

This matrix defines deterministic enforcement outcomes based on platform policy.

## Allowed Platforms
- general
- web
- demo

Action: EXECUTE  
Reason Code: platform_compliant

---

## Restricted Platforms
- child_safe
- regulated
- education_strict

Action: REWRITE or BLOCK  
Reason Code: platform_restriction_applied

Decision Rule:
- If content can be safely rewritten → REWRITE
- If content violates platform constraints → BLOCK

---

## Unknown / Unspecified Platform
- null
- missing
- unknown

Action: BLOCK  
Reason Code: platform_unknown

---

## Guarantees
- Platform rules override intent
- Platform ambiguity never EXECUTES
- No implicit allow
