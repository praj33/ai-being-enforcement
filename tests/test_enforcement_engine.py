import pytest
from enforcement_engine import enforce
from models.enforcement_input import EnforcementInput


def make_input(
    intent="test",
    dependency_score=0.0,
    age_gate_status="ALLOWED",
    region_policy="IN",
    platform_policy="INSTAGRAM",  # ✅ allowed platform
    karma_score=0.0,
    risk_flags=None
):
    return EnforcementInput(
        intent=intent,
        emotional_output={
            "tone": "neutral",
            "dependency_score": dependency_score
        },
        age_gate_status=age_gate_status,
        region_policy=region_policy,
        platform_policy=platform_policy,
        karma_score=karma_score,
        risk_flags=risk_flags or []
    )


# -------------------------------------------------
# BASIC BEHAVIOR
# -------------------------------------------------

def test_safe_input_allows():
    verdict = enforce(make_input())
    assert verdict.decision == "ALLOW"


def test_dependency_triggers_rewrite():
    verdict = enforce(make_input(dependency_score=0.9))
    assert verdict.decision == "REWRITE"


def test_age_block_overrides_everything():
    verdict = enforce(
        make_input(
            dependency_score=0.9,
            age_gate_status="BLOCKED"
        )
    )
    assert verdict.decision == "BLOCK"


# -------------------------------------------------
# PRIORITY COLLISIONS
# -------------------------------------------------

def test_block_overrides_rewrite():
    verdict = enforce(
        make_input(
            dependency_score=0.9,
            risk_flags=["SEXUAL_ESCALATION"]
        )
    )
    assert verdict.decision == "BLOCK"


def test_multiple_blocks_still_block():
    verdict = enforce(
        make_input(
            age_gate_status="BLOCKED",
            risk_flags=["SEXUAL_ESCALATION", "HIGH_RISK"]
        )
    )
    assert verdict.decision == "BLOCK"


# -------------------------------------------------
# KARMA SAFETY
# -------------------------------------------------

def test_high_karma_does_not_bypass_safety():
    verdict = enforce(
        make_input(
            karma_score=1.0,
            risk_flags=["HIGH_RISK"]
        )
    )
    assert verdict.decision == "BLOCK"


# -------------------------------------------------
# DETERMINISM
# -------------------------------------------------

def test_same_input_same_decision_and_trace():
    input_data = make_input(dependency_score=0.8)
    v1 = enforce(input_data)
    v2 = enforce(input_data)

    assert v1.decision == v2.decision
    assert v1.trace_id == v2.trace_id


# -------------------------------------------------
# NO INTERNAL LEAKAGE
# -------------------------------------------------

def test_no_internal_state_leak():
    verdict = enforce(make_input(dependency_score=0.9))

    assert hasattr(verdict, "trace_id")
    assert not hasattr(verdict, "evaluator_results")
    assert not hasattr(verdict, "akanksha_result")


# -------------------------------------------------
# REWRITE CONTRACT
# -------------------------------------------------

def test_rewrite_contains_rewrite_class():
    verdict = enforce(make_input(dependency_score=0.9))

    assert verdict.decision == "REWRITE"
    assert verdict.rewrite_class is not None
    assert verdict.rewrite_class == "DETERMINISTIC_REWRITE"
