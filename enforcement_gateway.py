"""
ENFORCEMENT RUNTIME GATEWAY
==========================
Sole live execution gate.

Properties:
- NON-BYPASSABLE
- FAIL-CLOSED
- DETERMINISTIC
- NO UUIDs
- NO TIMESTAMPS
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from enforcement_engine import enforce
from models.enforcement_input import EnforcementInput
from utils.deterministic_trace import generate_trace_id


# -------------------------------------------------
# APP
# -------------------------------------------------

app = FastAPI(
    title="AI Being — Enforcement Gateway",
    version="3.1.0-DETERMINISTIC-LOCK"
)


# -------------------------------------------------
# REQUEST / RESPONSE MODELS
# -------------------------------------------------

class EnforcementRequest(BaseModel):
    intent: str
    emotional_output: Dict[str, Any]
    age_gate_status: str
    region_policy: str
    platform_policy: str
    karma_score: Optional[float] = 0.0
    risk_flags: List[str] = []


class EnforcementResponse(BaseModel):
    decision: str              # EXECUTE | REWRITE | BLOCK
    trace_id: str
    rewrite_class: Optional[str] = None


# -------------------------------------------------
# LIVE GATE (ONLY ENTRY POINT)
# -------------------------------------------------

@app.post("/enforce", response_model=EnforcementResponse)
def enforcement_gateway(payload: EnforcementRequest):
    """
    HARD RUNTIME GATE.
    Nothing executes beyond this without enforcement approval.
    """

    # -------------------------------------------------
    # STEP 1 — CREATE TRACE ID (SINGLE AUTHORITY)
    # -------------------------------------------------
    trace_payload = {
        "intent": payload.intent,
        "emotional_output": payload.emotional_output,
        "age_gate_status": payload.age_gate_status,
        "region_policy": payload.region_policy,
        "platform_policy": payload.platform_policy,
        "karma_score": payload.karma_score or 0.0,
        "risk_flags": payload.risk_flags,
    }

    trace_id = generate_trace_id(
        input_payload=trace_payload,
        enforcement_category="RUNTIME_ENFORCEMENT_GATEWAY",
    )

    try:
        # -------------------------------------------------
        # STEP 2 — BUILD ENFORCEMENT INPUT (TRACE-INJECTED)
        # -------------------------------------------------
        enforcement_input = EnforcementInput(
            trace_id=trace_id,   # ✅ injected, not generated
            intent=payload.intent,
            emotional_output=payload.emotional_output,
            age_gate_status=payload.age_gate_status,
            region_policy=payload.region_policy,
            platform_policy=payload.platform_policy,
            karma_score=payload.karma_score or 0.0,
            risk_flags=payload.risk_flags,
        )

        # -------------------------------------------------
        # STEP 3 — ENFORCE (NO ID CREATION INSIDE)
        # -------------------------------------------------
        decision = enforce(enforcement_input)

        # -------------------------------------------------
        # STEP 4 — RETURN SAFE OUTPUT ONLY
        # -------------------------------------------------
        return EnforcementResponse(
            decision=decision.decision,
            trace_id=trace_id,   # ✅ gateway-owned
            rewrite_class=(
                decision.rewrite_guidance.rewrite_class
                if decision.decision == "REWRITE"
                and decision.rewrite_guidance
                else None
            ),
        )

    except Exception:
        # -------------------------------------------------
        # STEP 5 — FAIL CLOSED (DETERMINISTIC)
        # -------------------------------------------------
        return EnforcementResponse(
            decision="BLOCK",
            trace_id=trace_id,
            rewrite_class=None,
        )
