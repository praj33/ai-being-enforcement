"""
AKANKSHA → RAJ ENFORCEMENT ADAPTER

Purpose:
- Map Akanksha validator verdicts to Raj enforcement decisions
- NO validation logic
- NO trace_id generation
- NO policy decisions
"""

from typing import Dict
from validators.akanksha.behavior_validator import (
    BehaviorValidator,
    Decision,
    RiskCategory,
)



def map_akanksha_to_raj(verdict: Dict) -> Dict:
    """
    Maps Akanksha validator output to Raj enforcement intent.

    Input: verdict dict from validate_behavior()
    Output: dict for Raj enforcement engine
    """

    decision = verdict.get("decision")

    if decision == "hard_deny":
        enforcement_decision = "BLOCK"
    elif decision == "soft_rewrite":
        enforcement_decision = "REWRITE"
    elif decision == "allow":
        enforcement_decision = "EXECUTE"
    else:
        # Fail-closed
        enforcement_decision = "BLOCK"

    return {
        "enforcement_decision": enforcement_decision,
        "risk_category": verdict.get("risk_category"),
        "confidence": verdict.get("confidence"),
        "reason_code": verdict.get("reason_code"),
        "safe_output": verdict.get("safe_output"),
    }
