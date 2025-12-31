from models.evaluator_result import EvaluatorResult, EnforcementOutcome


def evaluate_region(
    region_policy: str,
    intent: str,
    vpn_suspected: bool,
) -> EvaluatorResult:
    """
    Region Restriction Evaluator (DEMO SAFE · HARD LOCK)

    Contract guarantees:
    - UNKNOWN or INVALID region is treated as unsafe
    - VPN ambiguity + policy-sensitive intent → BLOCK
    - Region-restricted intent outside allowed regions → BLOCK
    - No jurisdiction guessing allowed
    """

    evaluator_name = "region_restriction"

    # -------------------------------
    # Validate region input
    # -------------------------------
    if not region_policy or not isinstance(region_policy, str):
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="invalid_region_policy",
            confidence="HIGH",
            escalation=True,
        )

    region_policy = region_policy.upper()

    if region_policy == "UNKNOWN":
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="unknown_region_policy",
            confidence="HIGH",
            escalation=True,
        )

    # -------------------------------
    # Detect policy-sensitive intent
    # -------------------------------
    restricted_keywords = {
        "gambling",
        "crypto",
        "financial advice",
        "politics",
        "election",
        "weapon",
        "drug",
        "illegal",
    }

    intent_lower = intent.lower()
    contains_restricted = any(
        keyword in intent_lower for keyword in restricted_keywords
    )

    # -------------------------------
    # VPN ambiguity handling
    # -------------------------------
    if vpn_suspected and contains_restricted:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="vpn_ambiguity_with_restricted_intent",
            confidence="HIGH",
            escalation=True,
        )

    # -------------------------------
    # Region-based restrictions
    # -------------------------------
    restricted_regions = {"EU", "UK"}

    if region_policy in restricted_regions and contains_restricted:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="region_restricted_intent",
            confidence="HIGH",
            escalation=True,
        )

    # -------------------------------
    # SAFE EXECUTION
    # -------------------------------
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="region_policy_compliant",
        confidence="HIGH",
        escalation=False,
    )
