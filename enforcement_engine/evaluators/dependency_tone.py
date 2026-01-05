from typing import Set

from enforcement_engine.models.enforcement_input import EnforcementInput
from enforcement_engine.models.evaluator_result import (
    EvaluatorResult,
    EnforcementOutcome,
)

# Signals that indicate unhealthy dependency or exclusivity tone
DEPENDENCY_RISK_FLAGS: Set[str] = {
    "exclusive_dependency",
    "emotional_reliance",
    "isolation_encouragement",
    "authority_replacement",
}


def evaluate_dependency_tone(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Dependency & Emotional Manipulation Evaluator (Contract v2)

    RULES:
    - Dependency signals → REWRITE (escalation = true)
    - No dependency → EXECUTE
    - This evaluator does NOT BLOCK directly
    """

    evaluator_name = "dependency_tone"

    risk_flags = set(input_data.risk_flags or [])
    dependency_hits = risk_flags.intersection(DEPENDENCY_RISK_FLAGS)

    if dependency_hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.REWRITE,
            reason_code="dependency_tone_detected",
            confidence="MEDIUM",
            escalation=True,
            metadata={
                "risk_flags": list(dependency_hits)
            },
        )

    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="no_dependency_tone",
        confidence="HIGH",
        escalation=False,
        metadata={},
    )
