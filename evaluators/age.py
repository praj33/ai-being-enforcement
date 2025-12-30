from models.enforcement_input import EnforcementInput
from models.evaluator_result import EvaluatorResult, EnforcementOutcome


def evaluate_age(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Age Compliance Evaluator

    Rules:
    - If age gate explicitly failed → BLOCK
    - If age gate explicitly passed → EXECUTE
    - If age gate missing / unknown → REWRITE (safe fallback)
    """

    evaluator_name = "age_compliance"

    # Explicit failure
    if input_data.age_gate_passed is False:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.BLOCK,
            reason_code="age_gate_failed",
            metadata={
                "age_gate_passed": False
            },
        )

    # Explicit pass
    if input_data.age_gate_passed is True:
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            action=EnforcementOutcome.EXECUTE,
            reason_code="age_gate_passed",
            metadata={
                "age_gate_passed": True
            },
        )

    # Missing / unknown state → safe rewrite
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        action=EnforcementOutcome.REWRITE,
        reason_code="age_gate_unknown",
        metadata={
            "age_gate_passed": None
        },
    )
