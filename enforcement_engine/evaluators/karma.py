from enforcement_engine.models.enforcement_input import EnforcementInput
from enforcement_engine.models.evaluator_result import (
    EvaluatorResult,
    EnforcementOutcome,
)


def evaluate_karma(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Karma Awareness Evaluator (READ-ONLY)

    RULES:
    - Karma NEVER allows EXECUTE if other risks exist
    - Karma can ONLY nudge toward REWRITE
    - Karma NEVER blocks directly
    - Missing karma → neutral behavior
    """

    evaluator_name = "karma_awareness"
    karma = input_data.karma_signal

    # Karma missing or unavailable → neutral
    if karma is None:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.EXECUTE,
            reason_code="karma_unavailable",
            confidence="LOW",
            escalation=False,
            metadata={},
        )

    # Low karma → nudge toward rewrite (never block)
    if karma < 0.3:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.REWRITE,
            reason_code="low_karma_nudge",
            confidence="MEDIUM",
            escalation=True,
            metadata={
                "karma": karma
            },
        )

    # Normal / high karma → neutral
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="karma_neutral",
        confidence="HIGH",
        escalation=False,
        metadata={
            "karma": karma
        },
    )
