from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="Akanksha Behavior Validator")

class AkankshaRequest(BaseModel):
    intent: str
    emotional_output: Dict[str, Any]

class AkankshaResponse(BaseModel):
    decision: str
    risk_category: str
    confidence: float

@app.post("/validate", response_model=AkankshaResponse)
def validate(req: AkankshaRequest):
    # HARD FAILURE CASE (for proof)
    if "FAIL_AKANKSHA" in req.intent:
        raise HTTPException(status_code=500, detail="Akanksha failure")

    # Deterministic logic (example)
    if req.emotional_output.get("dependency_score", 0) > 0.8:
        return AkankshaResponse(
            decision="REWRITE",
            risk_category="dependency",
            confidence=0.9,
        )

    return AkankshaResponse(
        decision="EXECUTE",
        risk_category="clean",
        confidence=0.0,
    )
