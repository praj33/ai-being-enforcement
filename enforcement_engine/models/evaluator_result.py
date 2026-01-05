from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel


class EnforcementOutcome(str, Enum):
    EXECUTE = "EXECUTE"
    REWRITE = "REWRITE"
    BLOCK = "BLOCK"


class EvaluatorResult(BaseModel):
    evaluator_name: str
    decision: EnforcementOutcome
    reason_code: str
    confidence: str  # LOW | MEDIUM | HIGH
    escalation: bool
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evaluator_name": self.evaluator_name,
            "decision": self.decision.value,
            "reason_code": self.reason_code,
            "confidence": self.confidence,
            "escalation": self.escalation,
            "metadata": self.metadata or {},
        }
