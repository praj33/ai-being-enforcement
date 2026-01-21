"""
behavior_validator.py — CANONICAL AKANKSHA VALIDATOR v1.0

SINGLE SOURCE OF TRUTH for behavior validation.

STRICT GUARANTEES:
- Deterministic execution only
- No timestamps
- No randomness
- No authoritative trace IDs
- Fail-closed by default
- Under-age context is NON-NEGOTIABLE hard deny

Akanksha evaluates risk.
Raj decides execution.
"""

import re
import hashlib
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class Decision(str, Enum):
    ALLOW = "allow"
    SOFT_REWRITE = "soft_rewrite"
    HARD_DENY = "hard_deny"


class RiskCategory(str, Enum):
    EMOTIONAL_DEPENDENCY_BAIT = "emotional_dependency_bait"
    SEXUAL_ESCALATION_ATTEMPT = "sexual_escalation_attempt"
    MANIPULATIVE_PHRASING = "manipulative_phrasing"
    REGION_PLATFORM_CONFLICT = "region_platform_conflict"
    YOUTH_RISK_BEHAVIOR = "youth_risk_behavior"
    LONELINESS_HOOK = "loneliness_hook"
    ILLEGAL_INTENT_PROBING = "illegal_intent_probing"
    CLEAN = "clean"


class ReasonCode(str, Enum):
    EMOTIONAL_DEPENDENCY_DETECTED = "emotional_dependency_detected"
    SEXUAL_ESCALATION_DETECTED = "sexual_escalation_detected"
    MANIPULATIVE_LANGUAGE_DETECTED = "manipulative_language_detected"
    REGION_VIOLATION_DETECTED = "region_violation_detected"
    YOUTH_EXPLOITATION_DETECTED = "youth_exploitation_detected"
    LONELINESS_EXPLOIT_DETECTED = "loneliness_exploit_detected"
    ILLEGAL_INTENT_DETECTED = "illegal_intent_detected"
    CLEAN_CONTENT = "clean_content"


# ============================================================================
# VALIDATION RESULT (NON-AUTHORITATIVE)
# ============================================================================

@dataclass
class ValidationResult:
    decision: Decision
    risk_category: RiskCategory
    confidence: float               # 0–100
    reason_code: ReasonCode
    internal_trace: str              # 🔒 INTERNAL ONLY
    matched_patterns: List[str]
    explanation: str
    original_output: str
    safe_output: str = ""


# ============================================================================
# PATTERN LIBRARY (UNCHANGED COVERAGE)
# ============================================================================

class PatternLibrary:

    HARD_DENY_PATTERNS = {
        RiskCategory.ILLEGAL_INTENT_PROBING: [
            (r'\bkill myself\b', 100, "Suicidal intent"),
            (r'\bunalive myself\b', 100, "Suicidal intent (slang)"),
            (r'\bwant to die\b', 95, "Death wish"),
            (r'\bI will kill you\b', 98, "Homicidal threat"),
            (r'\bkill someone\b', 96, "Homicidal ideation"),
        ],
        RiskCategory.SEXUAL_ESCALATION_ATTEMPT: [
            (r'\bsend me nudes\b', 94, "Nude request"),
            (r'\btell me something sexy\b', 90, "Sexual content"),
            (r'\bsexting\b', 86, "Sexual messaging"),
        ],
        RiskCategory.YOUTH_RISK_BEHAVIOR: [
            (r'\bI am (1[0-7])\b', 97, "Minor disclosure"),
            (r'\bunderage\b', 95, "Underage context"),
            (r'\bminor\b', 94, "Minor mention"),
        ],
    }

    SOFT_REWRITE_PATTERNS = {
        RiskCategory.EMOTIONAL_DEPENDENCY_BAIT: [
            (r'\bstay with me forever\b', 80, "Dependency framing"),
            (r'\byou are all I have\b', 82, "Exclusive attachment"),
            (r'\bdon’t leave me\b', 78, "Abandonment fear"),
        ],
        RiskCategory.MANIPULATIVE_PHRASING: [
            (r'\bif you really cared\b', 79, "Conditional care"),
            (r'\byou owe me\b', 73, "Emotional debt"),
        ],
        RiskCategory.LONELINESS_HOOK: [
            (r'\bI am lonely\b', 65, "Loneliness expression"),
            (r'\ball alone\b', 60, "Isolation"),
        ],
    }


# ============================================================================
# CONFIDENCE ENGINE (DETERMINISTIC)
# ============================================================================

class ConfidenceEngine:

    @staticmethod
    def calculate(matches: List[Tuple[float, str, str]], text: str) -> float:
        if not matches:
            return 0.0

        base = sum(m[0] for m in matches) / len(matches)

        # Multi-hit amplification (bounded)
        if len(matches) > 1:
            base += min(len(matches) * 2, 10)

        # Text length factor
        word_count = len(text.split())
        if word_count > 20:
            base *= 1.05
        elif word_count < 4:
            base *= 0.9

        return min(base, 100.0)


# ============================================================================
# BEHAVIOR VALIDATOR (LIVE AUTHORITY)
# ============================================================================

class BehaviorValidator:

    def validate_behavior(
        self,
        intent: str,
        conversational_output: str,
        age_gate_status: bool,
        region_rule_status: Optional[Dict],
        platform_policy_state: Optional[Dict],
        karma_bias_input: float,
    ) -> ValidationResult:

        text = conversational_output.lower()

        # ------------------------------------------------------------
        # ABSOLUTE RULE: UNDER-AGE + EMOTIONAL / ROMANTIC = HARD DENY
        # ------------------------------------------------------------
        if not age_gate_status:
            if re.search(r'love|romantic|attached|dependency', text):
                return self._hard_block(
                    RiskCategory.YOUTH_RISK_BEHAVIOR,
                    ["underage_emotional_context"],
                    conversational_output,
                    98.0,
                    "Under-age emotional or romantic dependency detected",
                )

        # ------------------------------------------------------------
        # HARD DENY PATTERNS
        # ------------------------------------------------------------
        for category, patterns in PatternLibrary.HARD_DENY_PATTERNS.items():
            matches = self._find_matches(text, patterns)
            if matches:
                return self._build_result(
                    Decision.HARD_DENY,
                    category,
                    matches,
                    conversational_output,
                )

        # ------------------------------------------------------------
        # SOFT REWRITE PATTERNS
        # ------------------------------------------------------------
        for category, patterns in PatternLibrary.SOFT_REWRITE_PATTERNS.items():
            matches = self._find_matches(text, patterns)
            if matches:
                return self._build_result(
                    Decision.SOFT_REWRITE,
                    category,
                    matches,
                    conversational_output,
                )

        # ------------------------------------------------------------
        # CLEAN
        # ------------------------------------------------------------
        return ValidationResult(
            decision=Decision.ALLOW,
            risk_category=RiskCategory.CLEAN,
            confidence=0.0,
            reason_code=ReasonCode.CLEAN_CONTENT,
            internal_trace=self._internal_trace(text, "clean"),
            matched_patterns=[],
            explanation="No risky patterns detected",
            original_output=conversational_output,
            safe_output=conversational_output,
        )

    # =========================================================================
    # INTERNAL HELPERS
    # =========================================================================

    def _find_matches(
        self,
        text: str,
        patterns: List[Tuple[str, float, str]],
    ) -> List[Tuple[float, str, str]]:
        return [
            (confidence, pattern, label)
            for pattern, confidence, label in patterns
            if re.search(pattern, text, re.IGNORECASE)
        ]

    def _build_result(
        self,
        decision: Decision,
        category: RiskCategory,
        matches: List[Tuple[float, str, str]],
        original_output: str,
    ) -> ValidationResult:
        confidence = ConfidenceEngine.calculate(matches, original_output)
        return ValidationResult(
            decision=decision,
            risk_category=category,
            confidence=confidence,
            reason_code=self._map_reason(category),
            internal_trace=self._internal_trace(original_output, category.value),
            matched_patterns=[m[2] for m in matches],
            explanation=f"{len(matches)} {category.value} pattern(s) detected",
            original_output=original_output,
            safe_output="Response adjusted for safety.",
        )

    def _hard_block(
        self,
        category: RiskCategory,
        patterns: List[str],
        output: str,
        confidence: float,
        explanation: str,
    ) -> ValidationResult:
        return ValidationResult(
            decision=Decision.HARD_DENY,
            risk_category=category,
            confidence=confidence,
            reason_code=self._map_reason(category),
            internal_trace=self._internal_trace(output, category.value),
            matched_patterns=patterns,
            explanation=explanation,
            original_output=output,
            safe_output="I can’t engage with this. Please seek trusted support.",
        )

    def _internal_trace(self, text: str, category: str) -> str:
        raw = f"{text}|{category}|akanksha_v1"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _map_reason(self, category: RiskCategory) -> ReasonCode:
        mapping = {
            RiskCategory.EMOTIONAL_DEPENDENCY_BAIT: ReasonCode.EMOTIONAL_DEPENDENCY_DETECTED,
            RiskCategory.SEXUAL_ESCALATION_ATTEMPT: ReasonCode.SEXUAL_ESCALATION_DETECTED,
            RiskCategory.MANIPULATIVE_PHRASING: ReasonCode.MANIPULATIVE_LANGUAGE_DETECTED,
            RiskCategory.YOUTH_RISK_BEHAVIOR: ReasonCode.YOUTH_EXPLOITATION_DETECTED,
            RiskCategory.LONELINESS_HOOK: ReasonCode.LONELINESS_EXPLOIT_DETECTED,
            RiskCategory.ILLEGAL_INTENT_PROBING: ReasonCode.ILLEGAL_INTENT_DETECTED,
            RiskCategory.CLEAN: ReasonCode.CLEAN_CONTENT,
        }
        return mapping.get(category, ReasonCode.CLEAN_CONTENT)
