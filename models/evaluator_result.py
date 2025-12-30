from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel


class EvaluatorAction(str, Enum):
    EXECUTE = "EXECUTE"
    REWRITE = "REWRITE"
    BLOCK = "BLOCK"


class EvaluatorResult(BaseModel):
    evaluator_name: str
    action: EvaluatorAction
    reason_code: str
    metadata: Optional[Dict[str, Any]] = None
