from typing import Set

from enforcement_engine.models.enforcement_input import EnforcementInput
from enforcement_engine.models.evaluator_result import (
    EvaluatorResult,
    EnforcementOutcome,
)

# Illegal content signals (non-negotiable)
ILLEGAL_CONTENT_FLAGS: Set[str] = {
    "illegal_activity",
    "drug_distribution",
    "weapons_trafficking",
    "fraud",
    "scam",
    "terrorism",
    "money_laundering",
}


def evaluate_illegal_content(
    input_data: EnforcementInput,
) -> EvaluatorResult:
    """
    Illegal Content Evaluator (Contract v2)

    RULES:
    - Any illegal signal → HARD BLOCK
    - No rewrite allowed
    - Absolute boundary
    """

    evaluator_name = "illegal_content"
    risk_flags = set(input_data.risk_flags or [])

    hits = risk_flags.intersection(ILLEGAL_CONTENT_FLAGS)

    if hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="illegal_content_detected",
            confidence="HIGH",
            escalation=True,
            metadata={
                "risk_flags": list(hits)
            },
        )

    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="no_illegal_content",
        confidence="HIGH",
        escalation=False,
        metadata={},
    )
