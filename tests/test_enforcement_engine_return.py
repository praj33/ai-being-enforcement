import sys
from pathlib import Path

# 🔒 FIX PYTHON PATH FIRST (ABSOLUTE)
sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.enforcement_input import EnforcementInput
from enforcement_engine import enforce
from enforcement_verdict import EnforcementVerdict


payload = EnforcementInput(
    trace_id="debug-trace-001",
    intent="hello",
    emotional_output={},
    age_gate_status="ALLOWED",
    region_policy="IN",
    platform_policy="INSTAGRAM",
    karma_score=0.2,
    risk_flags=[],
)

v = enforce(payload)

print("RETURN TYPE:", type(v))
print("IS EnforcementVerdict:", isinstance(v, EnforcementVerdict))
print("DECISION:", v.decision)
print("TRACE:", v.trace_id)
