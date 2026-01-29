"""
ORCHESTRATOR RUNTIME — ENFORCEMENT LOCKED
Phase C — Action-Level Sovereignty

ABSOLUTE RULE:
No real-world action executes without ActionEnforcement approval.
FAIL-CLOSED. NON-BYPASSABLE.
"""

from action_enforcement import ActionEnforcementGateway


class OrchestratorRuntime:
    """
    Final execution spine.
    LAST code allowed before real-world action.
    """

    def __init__(self):
        # 🔒 Single, real enforcement authority
        self.action_enforcer = ActionEnforcementGateway()

    def execute_action(
        self,
        *,
        action_request: dict,
        enforcement_context: dict,
        action_history: dict,
    ) -> dict:
        """
        FINAL execution entrypoint.
        No bypass. No fallback. No override.
        """

        verdict = self.action_enforcer.approve_action(
            action_request=action_request,
            context=enforcement_context,
            action_history=action_history,
        )

        # -------------------------------------------------
        # 🚨 FAIL-CLOSED — ABSOLUTE
        # -------------------------------------------------
        if verdict.get("action_decision") != "EXECUTE":
            # No execution. No retries. No side effects.
            raise RuntimeError("ACTION_EXECUTION_DENIED")

        # -------------------------------------------------
        # ✅ EXECUTION PERMITTED
        # (Real-world action happens beyond this point)
        # -------------------------------------------------
        return {
            "status": "ACTION_EXECUTED",
            "enforcement_decision_id": verdict["trace_id"],
        }
