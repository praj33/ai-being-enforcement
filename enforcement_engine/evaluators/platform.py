from typing import Set

from enforcement_engine.models.enforcement_input import EnforcementInput
from enforcement_engine.models.evaluator_result import (
    EvaluatorResult,
    EnforcementOutcome,
)

# Platforms where execution is explicitly disallowed
RESTRICTED_PLATFORMS: Set[str] = {
    "kids_app",
    "education_under_13",
    "sandbox_restricted",
}


def evaluate_platform_policy(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Platform Policy Evaluator (Contract v2)

    HARD RULES:
    - UNKNOWN platform → BLOCK
    - Restricted platform → BLOCK
    - Allowed platform → EXECUTE
    """

    evaluator_name = "platform_policy"
    platform = input_data.platform_policy

    # UNKNOWN or missing platform → HARD BLOCK
    if not platform or platform == "UNKNOWN":
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="platform_unknown",
            confidence="HIGH",
            escalation=True,
            metadata={"platform": platform},
        )

    # Explicitly restricted platform
    if platform in RESTRICTED_PLATFORMS:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="platform_restricted",
            confidence="HIGH",
            escalation=True,
            metadata={"platform": platform},
        )

    # Allowed platform
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="platform_allowed",
        confidence="HIGH",
        escalation=False,
        metadata={"platform": platform},
    )
