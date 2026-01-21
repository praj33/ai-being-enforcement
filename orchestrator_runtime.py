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
    This is the last code allowed before real-world action.
    """

    def __init__(self):
        # 🔒 Real action enforcer (no mocks, no bypass)
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
        Any denial → HARD STOP.
        """

        decision = self.action_enforcer.approve_action(
            action_request=action_request,
            context=enforcement_context,
            action_history=action_history,
        )

        # 🚨 FAIL-CLOSED CHECK (MANDATORY)
        if decision.get("action_decision") != "EXECUTE":
            # ❌ ABSOLUTE BLOCK — NO SIDE EFFECTS
            raise RuntimeError(
                f"ACTION BLOCKED | reason={decision.get('reason')} | trace_id={decision['trace_id']}"
            )

        # ✅ Execution permitted (stub only — real action happens here)
        return {
            "status": "ACTION_EXECUTED",
            "trace_id": decision["trace_id"],
        }
