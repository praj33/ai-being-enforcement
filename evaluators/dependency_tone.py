from typing import Set

from models.enforcement_input import EnforcementInput
from models.evaluator_result import EvaluatorResult, EnforcementOutcome


# Signals that indicate unhealthy dependency or exclusivity tone
DEPENDENCY_RISK_FLAGS: Set[str] = {
    "exclusive_dependency",
    "emotional_reliance",
    "isolation_encouragement",
    "authority_replacement",
}


def evaluate_dependency_tone(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Dependency Tone Evaluator

    Rules:
    - If dependency-related risk flags are present → REWRITE
    - Otherwise → EXECUTE

    This evaluator NEVER blocks on its own.
    """

    evaluator_name = "dependency_tone"

    risk_flags = set(input_data.risk_flags or [])

    dependency_hits = risk_flags.intersection(DEPENDENCY_RISK_FLAGS)

    if dependency_hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.REWRITE,
            reason_code="dependency_tone_detected",
            metadata={
                "risk_flags": list(dependency_hits)
            },
        )

    return EvaluatorResult(
        evaluator_name=evaluator_name,
        action=EnforcementOutcome.EXECUTE,
        reason_code="no_dependency_tone",
        metadata={},
    )
