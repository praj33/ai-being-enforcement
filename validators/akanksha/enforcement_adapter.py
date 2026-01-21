"""
AKANKSHA → RAJ ENFORCEMENT ADAPTER

Purpose:
- Call Akanksha BehaviorValidator
- Adapt Raj inputs to Akanksha’s expected contract
- Map Akanksha verdicts into Raj-understandable structure
- FAIL-CLOSED (non-negotiable)
- NO trace generation
- NO logging
- NO policy overrides
"""

from typing import Dict

from validators.akanksha.behavior_validator import (
    BehaviorValidator,
    Decision,
)


class EnforcementAdapter:
    """
    Thin adapter layer.
    Akanksha is the authority.
    Raj consumes only mapped output.
    """

    def __init__(self):
        # REAL validator instance (no mocks)
        self.validator = BehaviorValidator()

    def validate(self, input_payload) -> Dict:
        """
        Runs Akanksha validator and maps result to Raj format.

        ABSOLUTE RULE:
        If Akanksha throws → enforcement MUST FAIL CLOSED.
        """

        try:
            conversational_text = self._serialize_emotional_output(
                input_payload.intent,
                input_payload.emotional_output,
            )

            verdict = self.validator.validate_behavior(
                intent=input_payload.intent,
                conversational_output=conversational_text,
                age_gate_status=input_payload.age_gate_status == "ALLOWED",
                region_rule_status={"region": input_payload.region_policy},
                platform_policy_state={"platform": input_payload.platform_policy},
                karma_bias_input=input_payload.karma_score,
            )

            return self._map_akanksha_to_raj(verdict)

        except Exception:
            # 🔒 FAIL-CLOSED — Akanksha is mandatory
            raise RuntimeError("AKANKSHA_VALIDATION_FAILED")

    @staticmethod
    def _serialize_emotional_output(intent: str, emotional_output: dict) -> str:
        """
        Deterministically convert structured emotional output into text.
        NO randomness. NO timestamps.
        """

        tone = emotional_output.get("tone", "neutral")
        dependency = emotional_output.get("dependency_score", 0.0)

        return (
            f"intent: {intent} | "
            f"tone: {tone} | "
            f"dependency_score: {dependency}"
        ).lower()

    @staticmethod
    def _map_akanksha_to_raj(verdict) -> Dict:
        """
        Maps Akanksha decision → Raj enforcement intent.
        Akanksha always wins.
        """

        if verdict.decision == Decision.HARD_DENY:
            decision = "BLOCK"
        elif verdict.decision == Decision.SOFT_REWRITE:
            decision = "REWRITE"
        elif verdict.decision == Decision.ALLOW:
            decision = "EXECUTE"
        else:
            decision = "BLOCK"  # FAIL-CLOSED SAFETY NET

        return {
            # 🔑 REQUIRED by Raj
            "decision": decision,

            # 🔒 Explicit mirror (non-authoritative)
            "enforcement_decision": decision,

            # 🧾 Metadata (informational only)
            "risk_category": verdict.risk_category,
            "confidence": verdict.confidence,
            "reason_code": verdict.reason_code,
            "safe_output": verdict.safe_output,
        }
