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
    # STEP 0 — INPUT SNAPSHOT (IMMUTABLE)
    # ---------------------------------
    input_snapshot = input_payload.to_dict()

    # ---------------------------------
    # STEP 1 — KILL SWITCH (ABSOLUTE)
    # ---------------------------------
    if RUNTIME_CONFIG.get("kill_switch") is True:
        trace_id = generate_trace_id(
            input_payload=input_snapshot,
            enforcement_category="KILL_SWITCH",
        )
        return EnforcementDecision(
            decision="BLOCK",
            trace_id=trace_id,
            rewrite_guidance=None,
        )

    # ---------------------------------
    # STEP 2 — RUN RAJ EVALUATORS
    # ---------------------------------
    evaluator_results = []
    for evaluator in ALL_EVALUATORS:
        evaluator_results.append(evaluator.evaluate(input_payload))

    raj_decision = _resolve_raj_decision(evaluator_results)

    # ---------------------------------
    # STEP 3 — RUN AKANKSHA (MANDATORY)
    # FAIL-CLOSED IF ANY ERROR
    # ---------------------------------
    try:
        adapter = EnforcementAdapter()
        akanksha_result = adapter.validate(input_payload)

        ak_decision = akanksha_result["decision"]
    except Exception:
        trace_id = generate_trace_id(
            input_payload=input_snapshot,
            enforcement_category="AKANKSHA_FAILURE",
        )
        return EnforcementDecision(
            decision="BLOCK",
            trace_id=trace_id,
            rewrite_guidance=None,
        )

    # ---------------------------------
    # STEP 4 — FINAL DECISION RESOLUTION
    # ---------------------------------
    final_decision = _resolve_final_decision(
        raj_decision=raj_decision,
        ak_decision=ak_decision,
    )

    # ---------------------------------
    # STEP 5 — REWRITE GUIDANCE (INTERNAL ONLY)
    # ---------------------------------
    rewrite_guidance = None
    if final_decision == "REWRITE":
        rewrite_guidance = generate_rewrite_guidance(evaluator_results)

    # ---------------------------------
    # STEP 6 — DETERMINISTIC TRACE ID
    # ---------------------------------
    trace_id = generate_trace_id(
        input_payload=input_snapshot,
        enforcement_category=final_decision,
    )

    # ---------------------------------
    # STEP 7 — AUDIT LOG (REPLAYABLE)
    # ---------------------------------
    log_enforcement(
        trace_id=trace_id,
        input_snapshot=input_snapshot,
        akanksha_verdict={
            "decision": ak_decision,
            "risk_category": akanksha_result.get("risk_category"),
            "confidence": akanksha_result.get("confidence"),
        },
        evaluator_results=evaluator_results,
        final_decision=final_decision,
    )

    # ---------------------------------
    # STEP 8 — SAFE OUTPUT ONLY
    # ---------------------------------
    return EnforcementDecision(
        decision=final_decision,
        trace_id=trace_id,
        rewrite_guidance=rewrite_guidance,
    )


# -------------------------------------------------
# INTERNAL HELPERS
# -------------------------------------------------

def _resolve_raj_decision(evaluator_results):
    """
    Resolve Raj-only decision.
    """
    for decision in DECISION_PRIORITY:
        for result in evaluator_results:
            if result.action == decision:
                return decision
    return "EXECUTE"


def _resolve_final_decision(*, raj_decision: str, ak_decision: str) -> str:
    """
    Combine Raj + Akanksha decisions using strict priority.
    """
    for decision in DECISION_PRIORITY:
        if decision == raj_decision or decision == ak_decision:
            return decision
    return "EXECUTE"
