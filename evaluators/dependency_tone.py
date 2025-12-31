from models.evaluator_result import EvaluatorResult, EnforcementOutcome


def evaluate_dependency_tone(
    intent: str,
) -> EvaluatorResult:
    """
    Dependency & Emotional Manipulation Evaluator (SOVEREIGN HARD LOCK)

    Contract guarantees:
    - Emotional dependence encouragement → BLOCK
    - Manipulative or coercive tone → REWRITE
    - No encouragement of exclusivity or reliance
    - Escalation raised whenever emotional risk exists
    """

    evaluator_name = "dependency_emotional_tone"

    intent_lower = intent.lower()

    # -------------------------------
    # Hard dependency / exclusivity signals
    # -------------------------------
    hard_block_phrases = {
        "only you understand me",
        "i need you",
        "i cannot live without you",
        "don't leave me",
        "stay with me forever",
        "be my only support",
    }

    if any(phrase in intent_lower for phrase in hard_block_phrases):
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="emotional_dependency_detected",
            confidence="HIGH",
            escalation=True,
        )

    # -------------------------------
    # Soft manipulation / reliance signals
    # -------------------------------
    soft_risk_phrases = {
        "you are the only one",
        "i trust only you",
        "promise you won't leave",
        "i feel safe only with you",
        "i need your constant help",
    }

    if any(phrase in intent_lower for phrase in soft_risk_phrases):
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.REWRITE,
            reason_code="potential_emotional_manipulation_requires_boundary",
            confidence="MEDIUM",
            escalation=True,
        )

    # -------------------------------
    # SAFE EXECUTION
    # -------------------------------
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="no_dependency_or_manipulation_detected",
        confidence="HIGH",
        escalation=False,
    )
