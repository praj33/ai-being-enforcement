from typing import Set

from models.enforcement_input import EnforcementInput
from models.evaluator_result import EvaluatorResult, EnforcementOutcome


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
    Emotional Manipulation Evaluator

    Rules:
    - If manipulation-related signals are present → REWRITE
    - Otherwise → EXECUTE

    This evaluator NEVER blocks by itself.
    Blocking happens only via higher-severity evaluators.
    """

    evaluator_name = "emotional_manipulation"

    risk_flags = set(input_data.risk_flags or [])

    manipulation_hits = risk_flags.intersection(EMOTIONAL_MANIPULATION_FLAGS)

    if manipulation_hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.REWRITE,
            reason_code="emotional_manipulation_detected",
            metadata={
                "risk_flags": list(manipulation_hits)
            },
        )

    return EvaluatorResult(
        evaluator_name=evaluator_name,
        action=EnforcementOutcome.EXECUTE,
        reason_code="no_emotional_manipulation",
        metadata={},
    )
