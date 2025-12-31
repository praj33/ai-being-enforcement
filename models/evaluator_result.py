from enum import Enum
from typing import Dict, Any


class EnforcementOutcome(str, Enum):
    EXECUTE = "EXECUTE"
    REWRITE = "REWRITE"
    BLOCK = "BLOCK"


class EvaluatorResult:
    """
    Canonical evaluator output object.

    This object is INTERNAL.
    It must always be complete and contract-compliant.
    """

    def __init__(
        self,
        evaluator_name: str,
        decision: EnforcementOutcome,
        reason_code: str,
        confidence: str,
        escalation: bool,
    ) -> None:
        self.evaluator_name = evaluator_name
        self.decision = decision
        self.reason_code = reason_code
        self.confidence = confidence
        self.escalation = escalation

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize evaluator result for logging / trace export.
        """

        return {
            "evaluator_name": self.evaluator_name,
            "decision": self.decision.value,
            "reason_code": self.reason_code,
            "confidence": self.confidence,
            "escalation": self.escalation,
        }
