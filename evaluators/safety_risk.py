from models.evaluator_result import EvaluatorResult, EnforcementOutcome


def evaluate_safety_risk(
    intent: str,
    risk_flags: list[str],
) -> EvaluatorResult:
    """
    Safety & Sexual Risk Evaluator (SOVEREIGN HARD LOCK)

    Contract guarantees:
    - Explicit sexual, violent, or self-harm intent → BLOCK
    - Escalating or ambiguous risk → REWRITE
    - Risk flags are always respected
    - No unsafe execution allowed
    """

    evaluator_name = "safety_sexual_risk"

    intent_lower = intent.lower()

    # -------------------------------
    # Hard sexual / violent keywords
    # -------------------------------
    hard_block_keywords = {
        "rape",
        "sexual assault",
        "child sexual",
        "bestiality",
        "incest",
        "kill",
        "murder",
        "suicide",
        "self harm",
        "terrorism",
    }

    if any(keyword in intent_lower for keyword in hard_block_keywords):
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="explicit_severe_safety_violation",
            confidence="HIGH",
            escalation=True,
        )

    # -------------------------------
    # Risk flags override
    # -------------------------------
    if risk_flags:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.REWRITE,
            reason_code="safety_risk_flagged",
            confidence="MEDIUM",
            escalation=True,
        )

    # -------------------------------
    # Soft sexual / violent keywords
    # -------------------------------
    soft_risk_keywords = {
        "sex",
        "sexual",
        "nude",
        "violence",
        "weapon",
        "drug",
        "abuse",
    }

    if any(keyword in intent_lower for keyword in soft_risk_keywords):
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.REWRITE,
            reason_code="potential_safety_risk_requires_softening",
            confidence="MEDIUM",
            escalation=True,
        )

    # -------------------------------
    # SAFE EXECUTION
    # -------------------------------
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="no_safety_risk_detected",
        confidence="HIGH",
        escalation=False,
    )
