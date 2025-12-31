from models.evaluator_result import EvaluatorResult, EnforcementOutcome


def evaluate_illegal_content(
    intent: str,
) -> EvaluatorResult:
    """
    Illegal Content Evaluator (SOVEREIGN HARD LOCK)

    Contract guarantees:
    - Explicit illegal activity facilitation → BLOCK
    - Ambiguous legality → REWRITE with safe framing
    - No illegal guidance may EXECUTE
    """

    evaluator_name = "illegal_content"

    intent_lower = intent.lower()

    # -------------------------------
    # Hard illegal facilitation signals
    # -------------------------------
    hard_illegal_keywords = {
        "how to make a bomb",
        "how to build a gun",
        "fake passport",
        "forged documents",
        "hack into",
        "bypass law enforcement",
        "evade police",
        "steal",
        "rob",
        "fraud",
        "scam",
        "counterfeit",
        "money laundering",
        "drug trafficking",
        "sell drugs",
    }

    if any(keyword in intent_lower for keyword in hard_illegal_keywords):
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="explicit_illegal_activity_facilitation",
            confidence="HIGH",
            escalation=True,
        )

    # -------------------------------
    # Soft / ambiguous legality signals
    # -------------------------------
    soft_illegal_keywords = {
        "avoid taxes",
        "tax loophole",
        "grey market",
        "anonymous money",
        "untraceable",
        "dark web",
    }

    if any(keyword in intent_lower for keyword in soft_illegal_keywords):
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.REWRITE,
            reason_code="ambiguous_legality_requires_safe_rewrite",
            confidence="MEDIUM",
            escalation=True,
        )

    # -------------------------------
    # SAFE EXECUTION
    # -------------------------------
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="no_illegal_content_detected",
        confidence="HIGH",
        escalation=False,
    )
