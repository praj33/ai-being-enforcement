from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass(frozen=True)
class EnforcementInput:
    intent: str
    emotional_output: Dict[str, Any]
    age_gate_status: str          # ALLOWED | BLOCKED
    region_policy: str            # IN | EU | US | etc
    platform_policy: str          # YOUTUBE | INSTAGRAM | etc
    karma_score: float            # -1.0 to +1.0
    risk_flags: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """
        Deterministic serialization.
        Used ONLY for trace-id generation and logging.
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
