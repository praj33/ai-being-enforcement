from typing import Dict, Any, List, Optional


class EnforcementInput:
    """
    Normalized input contract for the Enforcement Engine.

    This class performs:
    - Structural normalization
    - Explicit field extraction
    - Zero inference / zero guessing

    If a field is missing, it remains None.
    Evaluators decide what to do with absence.
    """

    def __init__(
        self,
        intent: Optional[str],
        emotional_output: Optional[str],
        age_gate_passed: Optional[bool],
        region: Optional[str],
        platform: Optional[str],
        karma_score: Optional[float],
        risk_flags: Optional[List[str]],
    ) -> None:
        self.intent = intent
        self.emotional_output = emotional_output
        self.age_gate_passed = age_gate_passed
        self.region = region
        self.platform = platform
        self.karma_score = karma_score
        self.risk_flags = risk_flags or []

    # --------------------------------------------------

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "EnforcementInput":
        """
        Create EnforcementInput from raw incoming payload.

        This method:
        - Extracts only known fields
        - Ignores unknown keys
        - Never mutates input
        """

        return cls(
            intent=raw.get("intent"),
            emotional_output=raw.get("emotional_output"),
            age_gate_passed=raw.get("age_gate_passed"),
            region=raw.get("region"),
            platform=raw.get("platform"),
            karma_score=raw.get("karma_score"),
            risk_flags=raw.get("risk_flags"),
        )

    # --------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Safe serialization for logging / trace export.
        """

        return {
            "intent": self.intent,
            "emotional_output": self.emotional_output,
            "age_gate_passed": self.age_gate_passed,
            "region": self.region,
            "platform": self.platform,
            "karma_score": self.karma_score,
            "risk_flags": list(self.risk_flags),
        }
