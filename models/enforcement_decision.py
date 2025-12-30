from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel


class EnforcementOutcome(str, Enum):
    EXECUTE = "EXECUTE"
    REWRITE = "REWRITE"
    BLOCK = "BLOCK"


class EnforcementDecision(BaseModel):
    """
    Final output of the Enforcement Engine.

    INTERNAL OBJECT.
    Never return directly to user-facing layers.
    """

    trace_id: str
    decision: EnforcementOutcome
    reason_code: str
    evaluator_results: List[Dict[str, Any]]
