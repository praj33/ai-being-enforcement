from typing import Set

from enforcement_engine.models.enforcement_input import EnforcementInput
from enforcement_engine.models.evaluator_result import (
    EvaluatorResult,
    EnforcementOutcome,
)

# Sexual content that must ALWAYS block
HARD_BLOCK_FLAGS: Set[str] = {
    "sexual_minors",
    "explicit_sexual_content",
    "sexual_exploitation",
}

# Sexual content that requires rewrite + escalation
REWRITE_FLAGS: Set[str] = {
    "sexual_suggestive",
    "romantic_dependency",
    "sexual_boundary_blur",
}


def evaluate_sexual_escalation(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Sexual Escalation Evaluator (Contract v2)

    RULES:
    - Sexual content involving minors or exploitation → BLOCK
    - Suggestive / boundary-blurring sexual content → REWRITE + escalation
    - Otherwise → EXECUTE
    """

    evaluator_name = "sexual_escalation"
    risk_flags = set(input_data.risk_flags or [])

    # 🚨 Absolute hard block
    hard_hits = risk_flags.intersection(HARD_BLOCK_FLAGS)
    if hard_hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="sexual_content_blocked",
            confidence="HIGH",
            escalation=True,
            metadata={
                "risk_flags": list(hard_hits)
            },
        )

    # ⚠️ Escalation-required rewrite
    rewrite_hits = risk_flags.intersection(REWRITE_FLAGS)
    if rewrite_hits:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.REWRITE,
            reason_code="sexual_content_requires_rewrite",
            confidence="MEDIUM",
            escalation=True,
            metadata={
                "risk_flags": list(rewrite_hits)
            },
        )

    # ✅ Safe
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="no_sexual_risk",
        confidence="HIGH",
        escalation=False,
        metadata={},
    )
