"""
Evaluator registry.

Each evaluator is:
- deterministic
- isolated
- order-independent
"""

from enforcement_engine.evaluators.age import evaluate_age
from enforcement_engine.evaluators.region import evaluate_region
from enforcement_engine.evaluators.platform import evaluate_platform_policy
from enforcement_engine.evaluators.safety_risk import evaluate_safety_risk
from enforcement_engine.evaluators.dependency_tone import evaluate_dependency_tone
from enforcement_engine.evaluators.sexual_escalation import evaluate_sexual_escalation
from enforcement_engine.evaluators.emotional_manipulation import (
    evaluate_emotional_manipulation,
)
from enforcement_engine.evaluators.illegal_content import evaluate_illegal_content
from enforcement_engine.evaluators.karma import evaluate_karma

__all__ = [
    "evaluate_age",
    "evaluate_region",
    "evaluate_platform_policy",
    "evaluate_safety_risk",
    "evaluate_dependency_tone",
    "evaluate_sexual_escalation",
    "evaluate_emotional_manipulation",
    "evaluate_illegal_content",
    "evaluate_karma",
]
