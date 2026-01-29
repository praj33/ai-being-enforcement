"""
ENFORCEMENT RUNTIME GATEWAY
==========================
Sole live execution gate.

Consumes ONLY EnforcementVerdict.
NON-BYPASSABLE. FAIL-CLOSED. DETERMINISTIC.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from enforcement_engine import enforce
from models.enforcement_input import EnforcementInput
from utils.deterministic_trace import generate_trace_id

from enforcement.intelligence_input_validator import (
    validate_intelligence_payload,
    IntelligenceContractViolation,
)

from enforcement_verdict import EnforcementVerdict


# -------------------------------------------------
# APP
# -------------------------------------------------

app = FastAPI(
    title="AI Being — Enforcement Gateway",
    version="3.1.0-DETERMINISTIC-LOCK",
)

# -------------------------------------------------
# REQUEST / RESPONSE MODELS
# -------------------------------------------------

class IntelligenceBlock(BaseModel):
    data: Dict[str, Any]


class EnforcementContext(BaseModel):
    emotional_output: Dict[str, Any]
    age_gate_status: str
    region_policy: str
    platform_policy: str
    karma_score: Optional[float] = 0.0
    risk_flags: List[str] = []


class EnforcementRequest(BaseModel):
    intelligence: IntelligenceBlock
    context: EnforcementContext


class EnforcementResponse(BaseModel):
    decision: str          # EXECUTE | REWRITE | BLOCK
    trace_id: str
    rewrite_class: Optional[str] = None


# -------------------------------------------------
# LIVE GATE
# -------------------------------------------------

@app.post("/enforce", response_model=EnforcementResponse)
def enforcement_gateway(payload: EnforcementRequest):
    """
    Final runtime authority.
    Nothing executes beyond this point.
    """

    # -------------------------------------------------
    # STEP 0 — INTELLIGENCE CONTRACT VALIDATION
    # -------------------------------------------------
    try:
        intelligence = validate_intelligence_payload(
            payload.intelligence.data
        )
    except IntelligenceContractViolation:
        trace_id = generate_trace_id(
            input_payload=payload.intelligence.data,
            enforcement_category="INTELLIGENCE_REJECTED",
        )
        return EnforcementResponse(
            decision="BLOCK",
            trace_id=trace_id,
            rewrite_class=None,
        )

    # -------------------------------------------------
    # STEP 1 — DETERMINISTIC TRACE ID
    # -------------------------------------------------
    trace_id = generate_trace_id(
        input_payload={**intelligence, **payload.context.dict()},
        enforcement_category="RUNTIME_GATEWAY",
    )

    # -------------------------------------------------
    # STEP 2 — BUILD ENFORCEMENT INPUT
    # -------------------------------------------------
    enforcement_input = EnforcementInput(
        trace_id=trace_id,
        intent=intelligence["intent"],
        emotional_output=payload.context.emotional_output,
        age_gate_status=payload.context.age_gate_status,
        region_policy=payload.context.region_policy,
        platform_policy=payload.context.platform_policy,
        karma_score=payload.context.karma_score or 0.0,
        risk_flags=payload.context.risk_flags,
    )

    # -------------------------------------------------
    # STEP 3 — ENFORCEMENT (SOLE AUTHORITY)
    # -------------------------------------------------
    try:
        verdict: EnforcementVerdict = enforce(enforcement_input)
    except Exception:
        return EnforcementResponse(
            decision="BLOCK",
            trace_id=trace_id,
            rewrite_class=None,
        )

    # -------------------------------------------------
    # STEP 4 — VERDICT → RUNTIME DECISION
    # -------------------------------------------------
    if verdict.decision == "ALLOW":
        return EnforcementResponse(
            decision="EXECUTE",
            trace_id=verdict.trace_id,
            rewrite_class=None,
        )

    if verdict.decision == "REWRITE":
        return EnforcementResponse(
            decision="REWRITE",
            trace_id=verdict.trace_id,
            rewrite_class=verdict.rewrite_class,
        )

    # BLOCK or TERMINATE
    return EnforcementResponse(
        decision="BLOCK",
        trace_id=verdict.trace_id,
        rewrite_class=None,
    )
