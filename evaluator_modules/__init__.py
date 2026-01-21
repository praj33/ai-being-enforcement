from evaluator_modules.age_compliance import AgeComplianceEvaluator
from evaluator_modules.region_restriction import RegionRestrictionEvaluator
from evaluator_modules.platform_policy import PlatformPolicyEvaluator
from evaluator_modules.safety_risk import SafetyRiskEvaluator
from evaluator_modules.dependency_tone import DependencyToneEvaluator
from evaluator_modules.sexual_escalation import SexualEscalationEvaluator
from evaluator_modules.emotional_manipulation import EmotionalManipulationEvaluator

ALL_EVALUATORS = [
    AgeComplianceEvaluator(),
    RegionRestrictionEvaluator(),
    PlatformPolicyEvaluator(),
    SafetyRiskEvaluator(),
    DependencyToneEvaluator(),
    SexualEscalationEvaluator(),
    EmotionalManipulationEvaluator(),
]
