from execution_gateway import execution_gateway

result = execution_gateway(
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

print(result)
