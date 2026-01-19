"""
RAJ PRAJAPATI — ENFORCEMENT ENGINE
---------------------------------
Deterministic execution layer.
Stateless. Auditable. Production-safe.

Responsibilities:
- Run all Raj evaluators
- Resolve EXECUTE / REWRITE / BLOCK (strict priority)
- Generate rewrite guidance (internal only)
- Enforce fail-closed behavior
- Produce deterministic trace IDs
"""

from evaluator_modules import ALL_EVALUATORS
from logs.bucket_logger import log_enforcement
from models.enforcement_decision import EnforcementDecision
from rewrite_engine import generate_rewrite_guidance
from config_loader import RUNTIME_CONFIG
from utils.deterministic_trace import generate_trace_id

# STRICT DECISION PRIORITY (DO NOT CHANGE)
DECISION_PRIORITY = ["BLOCK", "REWRITE", "EXECUTE"]


def enforce(input_payload):
    """
    Main enforcement entry.

    Input  : EnforcementInput
    Output : EnforcementDecision

    Guarantees:
    - Deterministic
    - Stateless
    - Fail-closed
    """

    evaluator_results = []

    # -------------------------------------------------
    # GLOBAL KILL SWITCH (FAIL-CLOSED)
    # -------------------------------------------------
    if RUNTIME_CONFIG.get("kill_switch") is True:
        trace_id = generate_trace_id(
            input_payload.__dict__,
            enforcement_category="KILL_SWITCH"
        )
        return EnforcementDecision(
            decision="BLOCK",
            trace_id=trace_id,
            rewrite_guidance=None
        )

    # -------------------------------------------------
    # RUN ALL RAJ EVALUATORS
    # -------------------------------------------------
    for evaluator in ALL_EVALUATORS:
        result = evaluator.evaluate(input_payload)
        evaluator_results.append(result)

    # -------------------------------------------------
    # RESOLVE FINAL DECISION (STRICT PRIORITY)
    # -------------------------------------------------
    final_decision = _resolve_decision(evaluator_results)

    # -------------------------------------------------
    # REWRITE GUIDANCE (INTERNAL ONLY)
    # -------------------------------------------------
    rewrite_guidance = None
    if final_decision == "REWRITE":
        rewrite_guidance = generate_rewrite_guidance(evaluator_results)

    # -------------------------------------------------
    # DETERMINISTIC TRACE ID
    # -------------------------------------------------
    trace_id = generate_trace_id(
        input_payload.__dict__,
        enforcement_category=final_decision
    )

    # -------------------------------------------------
    # AUDIT LOG (INTERNAL)
    # -------------------------------------------------
    log_enforcement(
        trace_id=trace_id,
        input_snapshot=input_payload,
        evaluator_results=evaluator_results,
        final_decision=final_decision
    )

    # -------------------------------------------------
    # SAFE OUTPUT (NO INTERNAL REASONS)
    # -------------------------------------------------
    return EnforcementDecision(
        decision=final_decision,
        trace_id=trace_id,
        rewrite_guidance=rewrite_guidance
    )


def _resolve_decision(evaluator_results):
    """
    Resolve final decision using strict priority.

    BLOCK > REWRITE > EXECUTE
    """

    for decision in DECISION_PRIORITY:
        for result in evaluator_results:
            if result.action == decision:
                return decision

    return "EXECUTE"
