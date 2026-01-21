from typing import Dict, List, Any
from pydantic import BaseModel


class EnforcementInput(BaseModel):
    """
    Pure enforcement signal.
    NO identity.
    NO timestamps.
    NO side effects.
    """

    intent: str
    emotional_output: Dict[str, Any]
    age_gate_status: str
    region_policy: str
    platform_policy: str
    karma_score: float
    risk_flags: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """
        Deterministic serialization.
        Used ONLY for trace-id generation and replay.
        """
        return {
            "intent": self.intent,
            "emotional_output": self.emotional_output,
            "age_gate_status": self.age_gate_status,
            "region_policy": self.region_policy,
            "platform_policy": self.platform_policy,
            "karma_score": self.karma_score,
            "risk_flags": self.risk_flags,
        }
