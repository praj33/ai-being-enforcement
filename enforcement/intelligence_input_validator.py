"""
INTELLIGENCE INPUT VALIDATOR
Fail-Closed Contract Enforcement
"""

from typing import Dict

EXPECTED_VERSION_HASH = "INTELLIGENCE_v1_LOCKED"

REQUIRED_FIELDS = {
    "trace_id": str,
    "intent": str,
    "suggested_action": str,
    "confidence": float,
    "version_hash": str,
}


class IntelligenceContractViolation(Exception):
    pass


def validate_intelligence_payload(payload: Dict) -> Dict:
    """
    Validates intelligence payload strictly.
    Any violation → FAIL CLOSED.
    """

    if not isinstance(payload, dict):
        raise IntelligenceContractViolation("Payload must be dict")

    # 1. Required fields check
    for field, field_type in REQUIRED_FIELDS.items():
        if field not in payload:
            raise IntelligenceContractViolation(f"Missing field: {field}")

        if not isinstance(payload[field], field_type):
            raise IntelligenceContractViolation(
                f"Invalid type for {field}"
            )

    # 2. No extra fields allowed
    unexpected = set(payload.keys()) - set(REQUIRED_FIELDS.keys())
    if unexpected:
        raise IntelligenceContractViolation(
            f"Unexpected fields: {unexpected}"
        )

    # 3. Confidence bounds
    if not (0.0 <= payload["confidence"] <= 1.0):
        raise IntelligenceContractViolation("Confidence out of bounds")

    # 4. Version lock
    if payload["version_hash"] != EXPECTED_VERSION_HASH:
        raise IntelligenceContractViolation("Version hash mismatch")

    return payload
