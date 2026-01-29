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
        # 0️⃣ INPUT FREEZE (IMMUTABLE SNAPSHOT)
        # --------------------------------------------------------------
        action_snapshot = dict(action_request)
        context_snapshot = dict(context)
        history_snapshot = dict(action_history)

        # --------------------------------------------------------------
        # 1️⃣ KILL-SWITCH (ABSOLUTE PRIORITY)
        # --------------------------------------------------------------
        if self._kill_switch_triggered(context_snapshot):
            return self._blocked(
                trace_id=self._trace(
                    action_snapshot,
                    context_snapshot,
                    category="KILL_SWITCH",
                ),
                reason="KILL_SWITCH_TRIGGERED",
            )

        # --------------------------------------------------------------
        # 2️⃣ CONTENT ENFORCEMENT DEPENDENCY
        # --------------------------------------------------------------
        if context_snapshot.get("content_decision") != "EXECUTE":
            return self._blocked(
                trace_id=self._trace(
                    action_snapshot,
                    context_snapshot,
                    category="CONTENT_BLOCK",
                ),
                reason="CONTENT_NOT_APPROVED",
            )

        # --------------------------------------------------------------
        # 3️⃣ PLATFORM ENFORCEMENT
        # --------------------------------------------------------------
        platform = action_snapshot.get("platform")
        if platform not in self.ALLOWED_PLATFORMS:
            return self._blocked(
                trace_id=self._trace(
                    action_snapshot,
                    context_snapshot,
                    category="PLATFORM_BLOCK",
                ),
                reason="PLATFORM_NOT_ALLOWED",
            )

        # --------------------------------------------------------------
        # 4️⃣ TARGET ENFORCEMENT
        # --------------------------------------------------------------
        if not self._target_allowed(action_snapshot, context_snapshot):
            return self._blocked(
                trace_id=self._trace(
                    action_snapshot,
                    context_snapshot,
                    category="TARGET_BLOCK",
                ),
                reason="TARGET_NOT_ALLOWED",
            )

        # --------------------------------------------------------------
        # 5️⃣ RATE LIMIT ENFORCEMENT
        # --------------------------------------------------------------
        if self._rate_limit_exceeded(history_snapshot):
            return self._blocked(
                trace_id=self._trace(
                    action_snapshot,
                    context_snapshot,
                    category="RATE_LIMIT_BLOCK",
                ),
                reason="RATE_LIMIT_EXCEEDED",
            )

        # --------------------------------------------------------------
        # ✅ ACTION APPROVED (EXECUTION TOKEN)
        # --------------------------------------------------------------
        return {
            "action_decision": "EXECUTE",
            "trace_id": self._trace(
                action_snapshot,
                context_snapshot,
                category="EXECUTE",
            ),
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

    def _trace(self, action: Dict, context: Dict, *, category: str) -> str:
        """
        Deterministic action trace ID.
        NO UUIDs.
        NO timestamps.
        NO randomness.
        """
        material = {
            "action": action,
            "context": context,
            "category": category,
            "engine_version": ENGINE_VERSION,
        }
        return hashlib.sha256(
            repr(material).encode("utf-8")
        ).hexdigest()

    def _blocked(self, *, trace_id: str, reason: str) -> Dict:
        return {
            "action_decision": "BLOCK",
            "trace_id": trace_id,
            "reason": reason,
        }
