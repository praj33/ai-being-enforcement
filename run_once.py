from models.enforcement_input import EnforcementInput
from enforcement_engine import enforce

input_payload = EnforcementInput(
    intent="Stay with me forever",
    emotional_output={
        "tone": "attached",
        "dependency_score": 0.9
    },
    age_gate_status="ALLOWED",
    region_policy="IN",
    platform_policy="INSTAGRAM",
    karma_score=0.3,
    risk_flags=[]
)

decision = enforce(input_payload)
print(decision)
