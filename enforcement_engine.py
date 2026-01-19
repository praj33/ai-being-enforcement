"""
RAJ PRAJAPATI — ENFORCEMENT ENGINE
---------------------------------
Deterministic execution layer.
Stateless. Auditable. Production-safe.

FINAL AUTHORITY GATE.
"""

from evaluator_modules import ALL_EVALUATORS
from logs.bucket_logger import log_enforcement
from models.enforcement_decision import EnforcementDecision
from rewrite_engine import generate_rewrite_guidance
from config_loader import RUNTIME_CONFIG
from utils.deterministic_trace import generate_trace_id
from validators.akanksha.enforcement_adapter import EnforcementAdapter

# STRICT PRIORITY (DO NOT CHANGE)
DECISION_PRIORITY = ["BLOCK", "REWRITE", "EXECUTE"]


def enforce(input_payload):
    """
    Deterministic, fail-closed enforcement entrypoint.
    """

    # ---------------------------------
    # KILL SWITCH (ABSOLUTE)
    # ---------------------------------
    if RUNTIME_CONFIG.get("kill_switch") is True:
        trace_id = generate_trace_id(
            input_payload.__dict__,
            enforcement_category="KILL_SWITCH",
        )
        return EnforcementDecision(
            decision="BLOCK",
            trace_id=trace_id,
            rewrite_guidance=None,
        )

    # ---------------------------------
    # RUN RAJ EVALUATORS
    # ---------------------------------
    evaluator_results = []
    for evaluator in ALL_EVALUATORS:
        evaluator_results.append(evaluator.evaluate(input_payload))

    raj_decision = _resolve_decision(evaluator_results)

    # ---------------------------------
    # RUN AKANKSHA (NON-BYPASSABLE)
    # ---------------------------------
    adapter = EnforcementAdapter()
    akanksha_result = adapter.validate(input_payload)

    ak_decision = akanksha_result["decision"]

    # ---------------------------------
    # FINAL DECISION RESOLUTION
    # ---------------------------------
    final_decision = _resolve_final_decision(
        raj_decision,
        ak_decision,
    )

    # ---------------------------------
    # REWRITE GUIDANCE (INTERNAL ONLY)
    # ---------------------------------
    rewrite_guidance = None
    if final_decision == "REWRITE":
        rewrite_guidance = generate_rewrite_guidance(evaluator_results)

    # ---------------------------------
    # DETERMINISTIC TRACE ID
    # ---------------------------------
    trace_id = generate_trace_id(
        input_payload.__dict__,
        enforcement_category=final_decision,
    )

    # ---------------------------------
    # AUDIT LOG (REPLAYABLE)
    # ---------------------------------
    log_enforcement(
        trace_id=trace_id,
        input_snapshot=input_payload,
        akanksha_verdict={
            "decision": ak_decision,
            "risk_category": akanksha_result["risk_category"],
            "confidence": akanksha_result["confidence"],
        },
        evaluator_results=evaluator_results,
        final_decision=final_decision,
    )

    # ---------------------------------
    # SAFE OUTPUT
    # ---------------------------------
    return EnforcementDecision(
        decision=final_decision,
        trace_id=trace_id,
        rewrite_guidance=rewrite_guidance,
    )


def _resolve_decision(evaluator_results):
    """
    Resolve Raj-only decision.
    """
    for decision in DECISION_PRIORITY:
        for result in evaluator_results:
            if result.action == decision:
                return decision
    return "EXECUTE"


def _resolve_final_decision(raj_decision: str, ak_decision: str) -> str:
    """
    Combine Raj + Akanksha decisions using strict priority.
    """
    for decision in DECISION_PRIORITY:
        if decision == raj_decision or decision == ak_decision:
            return decision
    return "EXECUTE"
