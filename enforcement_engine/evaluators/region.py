from typing import Set

from enforcement_engine.models.enforcement_input import EnforcementInput
from enforcement_engine.models.evaluator_result import (
    EvaluatorResult,
    EnforcementOutcome,
)


# Regions where execution is explicitly restricted
RESTRICTED_REGIONS: Set[str] = {
    "CN",  # China
    "KP",  # North Korea
    "IR",  # Iran
    "SY",  # Syria
}


def evaluate_region(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Region Restriction Evaluator (Sovereign Contract v2)

    HARD RULES:
    - UNKNOWN region → BLOCK
    - Restricted region → BLOCK
    - Allowed region → EXECUTE
    """

    evaluator_name = "region_restriction"
    region = input_data.region_state

    # UNKNOWN or missing region → HARD BLOCK
    if not region or region == "UNKNOWN":
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="region_unknown",
            confidence="HIGH",
            escalation=True,
            metadata={"region": region},
        )

    # Explicitly restricted region
    if region in RESTRICTED_REGIONS:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="region_restricted",
            confidence="HIGH",
            escalation=True,
            metadata={"region": region},
        )

    # Allowed region
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.EXECUTE,
        reason_code="region_allowed",
        confidence="HIGH",
        escalation=False,
        metadata={"region": region},
    )
