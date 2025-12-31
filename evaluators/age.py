from models.evaluator_result import EvaluatorResult, EnforcementOutcome


def evaluate_age(
    age_gate_status: str,
    intent: str,
) -> EvaluatorResult:
    """
    Age Compliance Evaluator (DEMO SAFE · HARD LOCK)

    Contract guarantees:
    - Output is always complete and valid
    - UNKNOWN age is treated as unsafe
    - MINOR or UNKNOWN + sensitive intent → BLOCK
    - Escalation is mandatory for unsafe states
    """

    evaluator_name = "age_compliance"

    # -------------------------------
    # Validate input
    # -------------------------------
    if age_gate_status not in {"ADULT", "MINOR", "UNKNOWN"}:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="invalid_age_gate_status",
            confidence="HIGH",
            escalation=True,
        )

    # -------------------------------
    # Detect sensitive intent
    # -------------------------------
    sensitive_keywords = {
        "sex",
        "sexual",
        "porn",
        "nude",
        "violence",
        "weapon",
        "drug",
        "illegal",
    }

    intent_lower = intent.lower()
    contains_sensitive = any(
        keyword in intent_lower for keyword in sensitive_keywords
    )

    # -------------------------------
    # HARD BLOCK CONDITIONS
    # -------------------------------
    if age_gate_status in {"MINOR", "UNKNOWN"} and contains_sensitive:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="age_restricted_sensitive_intent",
            confidence="HIGH",
            escalation=True,
        )

    # -------------------------------
    # SAFE REWRITE CONDITIONS
    # -------------------------------
    if age_gate_status == "UNKNOWN":
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.REWRITE,
            reason_code="age_unknown_safe_rewrite_required",
            confidence="MEDIUM",
            escalation=True,
        )

    # -------------------------------
    # ALLOW
    # -------------------------------
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="age_verified_adult",
        confidence="HIGH",
        escalation=False,
    )
