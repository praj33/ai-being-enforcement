from typing import Set

from enforcement_engine.models.enforcement_input import EnforcementInput
from enforcement_engine.models.evaluator_result import (
    EvaluatorResult,
    EnforcementOutcome,
)

# Risk flags that mandate HARD BLOCK
BLOCKING_RISK_FLAGS: Set[str] = {
    "self_harm",
    "suicide",
    "violence",
    "terrorism",
    "illegal_activity",
    "sexual_minors",
}

# Risk flags that require REWRITE (safe handling)
REWRITE_RISK_FLAGS: Set[str] = {
    "medical_advice",
    "legal_advice",
    "financial_advice",
    "emotional_distress",
}


def evaluate_safety_risk(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Safety & Sexual Risk Evaluator (Contract v2)

    HARD RULES:
    - Any blocking risk → BLOCK
    - Any rewrite risk → REWRITE
    - Else → EXECUTE
    """

    evaluator_name = "safety_risk"
    risk_flags = set(input_data.risk_flags or [])

    blocking_hits = risk_flags.intersection(BLOCKING_RISK_FLAGS)
    if blocking_hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="blocking_safety_risk",
            confidence="HIGH",
            escalation=True,
            metadata={"risk_flags": list(blocking_hits)},
        )

    rewrite_hits = risk_flags.intersection(REWRITE_RISK_FLAGS)
    if rewrite_hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.REWRITE,
            reason_code="rewrite_safety_risk",
            confidence="MEDIUM",
            escalation=True,
            metadata={"risk_flags": list(rewrite_hits)},
        )

    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="no_safety_risk",
        confidence="HIGH",
        escalation=False,
        metadata={},
    )
