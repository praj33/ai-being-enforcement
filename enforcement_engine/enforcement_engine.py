import uuid
from datetime import datetime
from typing import List

from enforcement_engine.models.enforcement_input import EnforcementInput
from enforcement_engine.models.enforcement_decision import (
    EnforcementDecision,
    EnforcementOutcome,
)
from enforcement_engine.models.evaluator_result import EvaluatorResult

from enforcement_engine.evaluators.age import evaluate_age
from enforcement_engine.evaluators.region import evaluate_region
from enforcement_engine.evaluators.platform import evaluate_platform_policy
from enforcement_engine.evaluators.safety_risk import evaluate_safety_risk
from enforcement_engine.evaluators.dependency_tone import evaluate_dependency_tone
from enforcement_engine.evaluators.sexual_escalation import evaluate_sexual_escalation
from enforcement_engine.evaluators.emotional_manipulation import (
    evaluate_emotional_manipulation,
)
from enforcement_engine.evaluators.illegal_content import evaluate_illegal_content
from enforcement_engine.evaluators.karma import evaluate_karma

from enforcement_engine.logs.bucket_logger import log_enforcement_event


EVALUATORS = [
    evaluate_age,
    evaluate_region,
    evaluate_platform_policy,
    evaluate_safety_risk,
    evaluate_dependency_tone,
    evaluate_sexual_escalation,
    evaluate_emotional_manipulation,
    evaluate_illegal_content,
    evaluate_karma,
]


def enforce(input_data: EnforcementInput) -> EnforcementDecision:
    """
    Sovereign Enforcement Engine

    HARD GUARANTEES:
    - Deterministic
    - Failure-safe
    - Traceable
    - NEVER raises
    - BLOCK on uncertainty
    """

    trace_id = input_data.trace_id or str(uuid.uuid4())
    evaluator_results: List[EvaluatorResult] = []

    final_decision = EnforcementOutcome.EXECUTE
    final_reason = "all_evaluators_passed"

    try:
        for evaluator in EVALUATORS:
            try:
                result = evaluator(input_data)

                if not isinstance(result, EvaluatorResult):
                    raise ValueError("invalid_evaluator_return")

            except Exception as evaluator_error:
                # Evaluator crash → HARD BLOCK
                result = EvaluatorResult(
                    evaluator_name=evaluator.__name__,
                    decision=EnforcementOutcome.BLOCK,
                    reason_code="evaluator_exception",
                    confidence="HIGH",
                    escalation=True,
                    metadata={"error": str(evaluator_error)},
                )

            evaluator_results.append(result)

            # 🔒 HARD PRECEDENCE RULES
            if result.decision == EnforcementOutcome.BLOCK:
                final_decision = EnforcementOutcome.BLOCK
                final_reason = result.reason_code
                break

            if result.escalation is True:
                final_decision = EnforcementOutcome.REWRITE
                final_reason = result.reason_code

            elif result.decision == EnforcementOutcome.REWRITE:
                final_decision = EnforcementOutcome.REWRITE
                final_reason = result.reason_code

    except Exception as engine_error:
        # Absolute last-resort safety net
        final_decision = EnforcementOutcome.BLOCK
        final_reason = "engine_failure"

        evaluator_results.append(
            EvaluatorResult(
                evaluator_name="enforcement_engine",
                decision=EnforcementOutcome.BLOCK,
                reason_code="engine_exception",
                confidence="HIGH",
                escalation=True,
                metadata={"error": str(engine_error)},
            )
        )

    decision = EnforcementDecision(
        trace_id=trace_id,
        final_decision=final_decision,
        reason_code=final_reason,
        evaluator_results=[r.to_dict() for r in evaluator_results],
        timestamp=datetime.utcnow().isoformat() + "Z",
    )

    # 🔒 EXACTLY ONE LOG PER CALL
    log_enforcement_event(
        {
            "trace_id": trace_id,
            "input_snapshot": input_data.model_dump(),
            "evaluator_results": [r.to_dict() for r in evaluator_results],
            "final_decision": decision.model_dump(),
        }
    )

    return decision
