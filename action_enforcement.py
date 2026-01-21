"""
ACTION-LEVEL ENFORCEMENT GATEWAY
Phase C — Real-World Action Control

ABSOLUTE RULE:
No real-world action executes without passing this gate.

PROPERTIES:
- FAIL-CLOSED
- DETERMINISTIC
- NON-BYPASSABLE
- ACTION-SOVEREIGN
"""

import hashlib
from typing import Dict, Set


ENGINE_VERSION = "ACTION_ENFORCEMENT_V1_LOCKED"


class ActionEnforcementGateway:
    """
    Final authority over real-world actions.
    NOTHING executes beyond this point.
    """

    # ------------------------------------------------------------------
    # 🔒 STATIC, VERSIONED POLICY (NO RUNTIME MUTATION)
    # ------------------------------------------------------------------

    ALLOWED_PLATFORMS: Set[str] = {"INSTAGRAM", "WHATSAPP"}
    MAX_ACTIONS_PER_SESSION: int = 3

    # 🔴 Absolute kill-switch signals
    KILL_SWITCH_SIGNALS: Set[str] = {
        "SELF_HARM",
        "VIOLENCE",
        "TERROR",
        "CRITICAL_THREAT",
        "ILLEGAL_ACTIVITY",
    }

    # ------------------------------------------------------------------
    # 🚨 MAIN ENTRYPOINT (NON-BYPASSABLE)
    # ------------------------------------------------------------------

    def approve_action(
        self,
        *,
        action_request: Dict,
        context: Dict,
        action_history: Dict,
    ) -> Dict:
        """
        Deterministic approval gate.
        Any violation → BLOCK.
        """

        # --------------------------------------------------------------
        # 0️⃣ KILL-SWITCH (ABSOLUTE PRIORITY)
        # --------------------------------------------------------------
        if self._kill_switch_triggered(context):
            trace_id = self._deterministic_trace_id(
                action_request,
                context,
                category="KILL_SWITCH",
            )
            return self._blocked(
                trace_id=trace_id,
                reason="KILL_SWITCH_TRIGGERED",
            )

        # --------------------------------------------------------------
        # 1️⃣ CONTENT ENFORCEMENT DEPENDENCY
        # --------------------------------------------------------------
        if context.get("content_decision") != "EXECUTE":
            trace_id = self._deterministic_trace_id(
                action_request,
                context,
                category="CONTENT_BLOCK",
            )
            return self._blocked(
                trace_id=trace_id,
                reason="CONTENT_NOT_APPROVED",
            )

        # --------------------------------------------------------------
        # 2️⃣ PLATFORM ENFORCEMENT
        # --------------------------------------------------------------
        platform = action_request.get("platform")
        if platform not in self.ALLOWED_PLATFORMS:
            trace_id = self._deterministic_trace_id(
                action_request,
                context,
                category="PLATFORM_BLOCK",
            )
            return self._blocked(
                trace_id=trace_id,
                reason="PLATFORM_NOT_ALLOWED",
            )

        # --------------------------------------------------------------
        # 3️⃣ TARGET ENFORCEMENT
        # --------------------------------------------------------------
        if not self._target_allowed(action_request, context):
            trace_id = self._deterministic_trace_id(
                action_request,
                context,
                category="TARGET_BLOCK",
            )
            return self._blocked(
                trace_id=trace_id,
                reason="TARGET_NOT_ALLOWED",
            )

        # --------------------------------------------------------------
        # 4️⃣ RATE LIMIT ENFORCEMENT
        # --------------------------------------------------------------
        if self._rate_limit_exceeded(action_history):
            trace_id = self._deterministic_trace_id(
                action_request,
                context,
                category="RATE_LIMIT_BLOCK",
            )
            return self._blocked(
                trace_id=trace_id,
                reason="RATE_LIMIT_EXCEEDED",
            )

        # --------------------------------------------------------------
        # ✅ ACTION APPROVED
        # --------------------------------------------------------------
        trace_id = self._deterministic_trace_id(
            action_request,
            context,
            category="EXECUTE",
        )

        return {
            "action_decision": "EXECUTE",
            "trace_id": trace_id,
        }

    # ------------------------------------------------------------------
    # 🔧 INTERNAL HELPERS (PURE, DETERMINISTIC)
    # ------------------------------------------------------------------

    def _kill_switch_triggered(self, context: Dict) -> bool:
        flags = set(context.get("risk_flags", []))
        return bool(flags & self.KILL_SWITCH_SIGNALS)

    def _target_allowed(self, action_request: Dict, context: Dict) -> bool:
        """
        Example rule:
        - Cannot message blocked users or minors (if supplied).
        """
        target = action_request.get("target")
        blocked_targets = set(context.get("blocked_targets", []))
        return target not in blocked_targets

    def _rate_limit_exceeded(self, action_history: Dict) -> bool:
        return action_history.get("actions_sent", 0) >= self.MAX_ACTIONS_PER_SESSION

    def _deterministic_trace_id(
        self,
        action_request: Dict,
        context: Dict,
        category: str,
    ) -> str:
        """
        Deterministic action trace ID.
        NO UUIDs.
        NO timestamps.
        NO randomness.
        """
        base = f"{action_request}|{context}|{category}|{ENGINE_VERSION}"
        return hashlib.sha256(base.encode()).hexdigest()

    def _blocked(self, *, trace_id: str, reason: str) -> Dict:
        return {
            "action_decision": "BLOCK",
            "trace_id": trace_id,
            "reason": reason,
        }
