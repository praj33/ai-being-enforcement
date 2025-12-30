from typing import Set

from models.enforcement_input import EnforcementInput
from models.evaluator_result import EvaluatorResult, EnforcementOutcome


# Sexual content risk signals
# These are assumed to be pre-computed upstream
HARD_BLOCK_FLAGS: Set[str] = {
    "sexual_minors",
    "explicit_sexual_content",
    "sexual_exploitation",
}

REWRITE_FLAGS: Set[str] = {
    "sexual_suggestive",
    "romantic_dependency",
    "sexual_boundary_blur",
}


def evaluate_sexual_escalation(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Sexual Escalation Evaluator

    Rules:
    - If any HARD_BLOCK flag is present → BLOCK
    - Else if any REWRITE flag is present → REWRITE
    - Else → EXECUTE

    This evaluator is strict and non-negotiable.
    """

    evaluator_name = "sexual_escalation"

    risk_flags = set(input_data.risk_flags or [])

    # Hard sexual violations (absolute boundary)
    hard_hits = risk_flags.intersection(HARD_BLOCK_FLAGS)
    if hard_hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.BLOCK,
            reason_code="sexual_escalation_blocked",
            metadata={
                "risk_flags": list(hard_hits)
            },
        )

    # Boundary-blurring or suggestive content
    rewrite_hits = risk_flags.intersection(REWRITE_FLAGS)
    if rewrite_hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.REWRITE,
            reason_code="sexual_escalation_rewrite",
            metadata={
                "risk_flags": list(rewrite_hits)
            },
        )

    # No sexual escalation detected
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        action=EnforcementOutcome.EXECUTE,
        reason_code="no_sexual_escalation",
        metadata={},
    )
