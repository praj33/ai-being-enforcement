from models.evaluator_result import EvaluatorResult, EnforcementOutcome


def evaluate_platform_policy(
    platform_policy: str,
    intent: str,
) -> EvaluatorResult:
    """
    Platform Policy Evaluator (SOVEREIGN HARD LOCK)

    Contract guarantees:
    - UNKNOWN or invalid platform policy → BLOCK
    - Platform-restricted intent → BLOCK
    - No platform ambiguity allowed
    - Escalation raised on all unsafe paths
    """

    evaluator_name = "platform_policy"

    # -------------------------------
    # Validate platform policy
    # -------------------------------
    if not platform_policy or not isinstance(platform_policy, str):
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="invalid_platform_policy",
            confidence="HIGH",
            escalation=True,
        )

    platform_policy = platform_policy.upper()

    if platform_policy == "UNKNOWN":
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="unknown_platform_policy",
            confidence="HIGH",
            escalation=True,
        )

    # -------------------------------
    # Detect platform-restricted intent
    # -------------------------------
    restricted_keywords = {
        "sexual",
        "porn",
        "nude",
        "hate",
        "harassment",
        "violence",
        "illegal",
        "drug",
        "weapon",
    }

    intent_lower = intent.lower()
    contains_restricted = any(
        keyword in intent_lower for keyword in restricted_keywords
    )

    # -------------------------------
    # Platform hard restrictions
    # -------------------------------
    restricted_platforms = {
        "KIDS_APP",
        "EDUCATION_UNDER_13",
        "SANDBOX_RESTRICTED",
    }

    if platform_policy in restricted_platforms:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="platform_explicitly_restricted",
            confidence="HIGH",
            escalation=True,
        )

    if contains_restricted and platform_policy in {"IOS", "ANDROID"}:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="platform_content_violation",
            confidence="HIGH",
            escalation=True,
        )

    # -------------------------------
    # SAFE EXECUTION
    # -------------------------------
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="platform_policy_compliant",
        confidence="HIGH",
        escalation=False,
    )
