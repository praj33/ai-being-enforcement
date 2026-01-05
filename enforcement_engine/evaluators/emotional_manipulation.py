from typing import Set

from enforcement_engine.models.enforcement_input import EnforcementInput
from enforcement_engine.models.evaluator_result import (
    EvaluatorResult,
    EnforcementOutcome,
)

# Signals indicating emotional manipulation or coercion
EMOTIONAL_MANIPULATION_FLAGS: Set[str] = {
    "guilt_tripping",
    "fear_induction",
    "gaslighting",
    "coercive_persuasion",
    "emotional_blackmail",
}


def evaluate_emotional_manipulation(
    input_data: EnforcementInput,
) -> EvaluatorResult:
    """
    Emotional Manipulation Evaluator (Contract v2)

    RULES:
    - Manipulation signals → REWRITE + escalation
    - Never EXECUTE if manipulation risk exists
    - Never BLOCK directly (precedence handled by engine)
    """

    evaluator_name = "emotional_manipulation"
    risk_flags = set(input_data.risk_flags or [])

    hits = risk_flags.intersection(EMOTIONAL_MANIPULATION_FLAGS)

    if hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.REWRITE,
            reason_code="emotional_manipulation_detected",
            confidence="MEDIUM",
            escalation=True,
            metadata={
                "risk_flags": list(hits)
            },
        )

    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="no_emotional_manipulation",
        confidence="HIGH",
        escalation=False,
        metadata={},
    )
