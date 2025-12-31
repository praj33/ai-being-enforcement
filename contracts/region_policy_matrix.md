# Region Policy Matrix (Locked)

This matrix defines deterministic enforcement outcomes based on region certainty.

## Allowed Regions
- IN
- US
- EU

Action: EXECUTE  
Reason Code: region_allowed

---

## Restricted / Unknown Regions
- UNKNOWN
- VPN
- TOR
- PROXY

Action: BLOCK  
Reason Code: jurisdiction_uncertain

Rationale:
Jurisdiction ambiguity is unsafe. Enforcement must BLOCK.

---

## Explicitly Restricted Regions
- Any region explicitly disallowed by governance

Action: BLOCK  
Reason Code: region_restricted

---

## Guarantees
- No region inference
- No best-guess behavior
- No silent fallback
- Ambiguity always BLOCKS
