from typing import Set

from models.enforcement_input import EnforcementInput
from models.evaluator_result import EvaluatorResult, EnforcementOutcome


# Regions where execution is explicitly restricted
RESTRICTED_REGIONS: Set[str] = {
    "CN",   # China
    "KP",   # North Korea
    "IR",   # Iran
    "SY",   # Syria
}


def evaluate_region(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Region Restriction Evaluator

    Rules:
    - If region is explicitly restricted → BLOCK
    - If region is present and allowed → EXECUTE
    - If region is missing / unknown → REWRITE (safe fallback)
    """

    evaluator_name = "region_restriction"

    region = input_data.region

    # Explicitly restricted region
    if region in RESTRICTED_REGIONS:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.BLOCK,
            reason_code="region_restricted",
            metadata={
                "region": region
            },
        )

    # Explicitly allowed region
    if region is not None:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.EXECUTE,
            reason_code="region_allowed",
            metadata={
                "region": region
            },
        )

    # Missing / unknown region → safe rewrite
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        action=EnforcementOutcome.REWRITE,
        reason_code="region_unknown",
        metadata={
            "region": None
        },
    )
