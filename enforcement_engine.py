import uuid
from typing import List

from models.enforcement_input import EnforcementInput
from models.enforcement_decision import EnforcementDecision, EnforcementOutcome
from models.evaluator_result import EvaluatorResult, EvaluatorAction

from evaluators.age import evaluate_age
from evaluators.region import evaluate_region
from evaluators.platform import evaluate_platform
from evaluators.safety_risk import evaluate_safety_risk
from evaluators.dependency_tone import evaluate_dependency_tone
from evaluators.sexual_escalation import evaluate_sexual_escalation
from evaluators.emotional_manipulation import evaluate_emotional_manipulation

from logging.bucket_logger import log_enforcement_event


EVALUATORS = [
    evaluate_age,
    evaluate_region,
    evaluate_platform,
    evaluate_safety_risk,
    evaluate_dependency_tone,
    evaluate_sexual_escalation,
    evaluate_emotional_manipulation,
]


def enforce(input_data: EnforcementInput) -> EnforcementDecision:
    """
    Failure-hardened deterministic enforcement engine.
    This function MUST NEVER RAISE.
    """

    trace_id = input_data.trace_id or str(uuid.uuid4())
    evaluator_results: List[EvaluatorResult] = []

    final_decision = EnforcementOutcome.EXECUTE
    final_reason = "no_violation"

    try:
        for evaluator in EVALUATORS:
            try:
                result = evaluator(input_data)

                if not isinstance(result, EvaluatorResult):
                    raise ValueError("invalid_evaluator_return")

            except Exception as evaluator_error:
                # Evaluator failure = hard BLOCK
                result = EvaluatorResult(
                    evaluator_name=evaluator.__name__,
                    action=EvaluatorAction.BLOCK,
                    reason_code="evaluator_failure",
                    metadata={"error": str(evaluator_error)},
                )

            evaluator_results.append(result)

            if result.action == EvaluatorAction.BLOCK:
                final_decision = EnforcementOutcome.BLOCK
                final_reason = result.reason_code
                break

            if result.action == EvaluatorAction.REWRITE:
                final_decision = EnforcementOutcome.REWRITE
                final_reason = result.reason_code

    except Exception as engine_error:
        # Absolute last-resort safety net
        final_decision = EnforcementOutcome.BLOCK
        final_reason = "engine_failure"

        evaluator_results.append(
            EvaluatorResult(
                evaluator_name="enforcement_engine",
                action=EvaluatorAction.BLOCK,
                reason_code="engine_exception",
                metadata={"error": str(engine_error)},
            )
        )

    decision = EnforcementDecision(
        trace_id=trace_id,
        decision=final_decision,
        reason_code=final_reason,
        evaluator_results=[r.model_dump() for r in evaluator_results],
    )

    log_enforcement_event(
        {
            "trace_id": trace_id,
            "input_snapshot": input_data.model_dump(),
            "evaluator_results": [r.model_dump() for r in evaluator_results],
            "final_decision": decision.model_dump(),
        }
    )

    return decision
