from typing import Set

from models.enforcement_input import EnforcementInput
from models.evaluator_result import EvaluatorResult, EnforcementOutcome


# Platforms where execution is explicitly disallowed
RESTRICTED_PLATFORMS: Set[str] = {
    "kids_app",
    "education_under_13",
    "sandbox_restricted",
}


def evaluate_platform(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Platform Policy Evaluator

    Rules:
    - If platform is explicitly restricted → BLOCK
    - If platform is present and allowed → EXECUTE
    - If platform is missing / unknown → REWRITE (safe fallback)
    """

    evaluator_name = "platform_policy"

    platform = input_data.platform

    # Explicitly restricted platform
    if platform in RESTRICTED_PLATFORMS:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.BLOCK,
            reason_code="platform_restricted",
            metadata={
                "platform": platform
            },
        )

    # Explicitly allowed platform
    if platform is not None:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.EXECUTE,
            reason_code="platform_allowed",
            metadata={
                "platform": platform
            },
        )

    # Missing / unknown platform → safe rewrite
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        action=EnforcementOutcome.REWRITE,
        reason_code="platform_unknown",
        metadata={
            "platform": None
        },
    )
