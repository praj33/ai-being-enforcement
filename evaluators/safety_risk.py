from typing import Set

from models.enforcement_input import EnforcementInput
from models.evaluator_result import EvaluatorResult, EnforcementOutcome


# Risk flags that mandate hard blocking
BLOCKING_RISK_FLAGS: Set[str] = {
    "self_harm",
    "suicide",
    "violence",
    "terrorism",
    "illegal_activity",
    "sexual_minors",
}

# Risk flags that require response rewriting
REWRITE_RISK_FLAGS: Set[str] = {
    "medical_advice",
    "legal_advice",
    "financial_advice",
    "emotional_distress",
}


def evaluate_safety_risk(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Safety Risk Evaluator

    Rules:
    - If any BLOCKING risk flag is present → BLOCK
    - Else if any REWRITE risk flag is present → REWRITE
    - Else → EXECUTE
    """

    evaluator_name = "safety_risk"

    risk_flags = set(input_data.risk_flags or [])

    # Hard safety violations
    blocking_hits = risk_flags.intersection(BLOCKING_RISK_FLAGS)
    if blocking_hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.BLOCK,
            reason_code="blocking_safety_risk",
            metadata={
                "risk_flags": list(blocking_hits)
            },
        )

    # Soft safety risks requiring rewrite
    rewrite_hits = risk_flags.intersection(REWRITE_RISK_FLAGS)
    if rewrite_hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.REWRITE,
            reason_code="rewrite_safety_risk",
            metadata={
                "risk_flags": list(rewrite_hits)
            },
        )

    # No known safety risks
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        action=EnforcementOutcome.EXECUTE,
        reason_code="no_safety_risk",
        metadata={
            "risk_flags": []
        },
    )
