from fastapi.testclient import TestClient

from enforcement_gateway import app


client = TestClient(app)


def test_full_chain_rewrite():
    payload = {
        "intent": "Stay with me forever",
        "emotional_output": {
            "tone": "attached",
            "dependency_score": 0.9
        },
        "age_gate_status": "ALLOWED",
        "region_policy": "IN",
        "platform_policy": "INSTAGRAM",
        "karma_score": 0.8,
        "risk_flags": []
    }

    response = client.post("/enforce", json=payload)

    assert response.status_code == 200

    body = response.json()

    assert body["decision"] == "REWRITE"
    assert body["rewrite_class"] == "REDUCE_EMOTIONAL_DEPENDENCY"
    assert isinstance(body["trace_id"], str)
    assert len(body["trace_id"]) == 64
