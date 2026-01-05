from enforcement_engine.models.enforcement_input import EnforcementInput
from enforcement_engine.models.evaluator_result import (
    EvaluatorResult,
    EnforcementOutcome,
)


def evaluate_age(input_data: EnforcementInput) -> EvaluatorResult:
    """
    Age Compliance Evaluator (Sovereign Contract)

    Rules:
    - MINOR            → BLOCK
    - ADULT            → EXECUTE
    - UNKNOWN / missing → BLOCK (hard safety)
    """

    evaluator_name = "age_compliance"

    age_state = input_data.age_state

    if age_state == "MINOR":
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.BLOCK,
            reason_code="age_minor",
            confidence="HIGH",
            escalation=True,
            metadata={"age_state": age_state},
        )

    if age_state == "ADULT":
        return EvaluatorResult(
            evaluator_name=evaluator_name,
            decision=EnforcementOutcome.EXECUTE,
            reason_code="age_adult",
            confidence="HIGH",
            escalation=False,
            metadata={"age_state": age_state},
        )

    # UNKNOWN or missing age → HARD BLOCK
    return EvaluatorResult(
        evaluator_name=evaluator_name,
        decision=EnforcementOutcome.BLOCK,
        reason_code="age_unknown",
        confidence="HIGH",
        escalation=True,
        metadata={"age_state": age_state},
    )
