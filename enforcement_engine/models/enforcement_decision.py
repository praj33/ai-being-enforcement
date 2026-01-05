from typing import List, Dict, Any
from pydantic import BaseModel

from enforcement_engine.models.evaluator_result import EnforcementOutcome


class EnforcementDecision(BaseModel):
    """
    Final output of the Enforcement Engine.

    INTERNAL OBJECT.
    Never return directly to user-facing layers.
    """

    trace_id: str
    final_decision: EnforcementOutcome
    reason_code: str
    evaluator_results: List[Dict[str, Any]]
    timestamp: str
