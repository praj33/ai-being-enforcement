"""
RUN ACTION DEMO — PHASE C PROOF

Purpose:
- Prove ActionEnforcementGateway blocks real-world actions
- Demonstrate deterministic trace IDs
- Show FAIL-CLOSED behavior

This file MUST NOT contain enforcement logic.
It only calls the orchestrator.
"""

from orchestrator_runtime import OrchestratorRuntime


def main():
    runtime = OrchestratorRuntime()

    # -------------------------------
    # ACTION REQUEST (WHAT USER WANTS TO DO)
    # -------------------------------
    action_request = {
        "action_type": "SEND_MESSAGE",
        "platform": "INSTAGRAM",
        "target": "user_123",
        "message": "Stay with me forever",
    }

    # -------------------------------
    # ENFORCEMENT CONTEXT (FROM PIPELINE)
    # -------------------------------
    enforcement_context = {
        # ⛔ Change this to anything other than EXECUTE to see HARD BLOCK
        "content_decision": "EXECUTE",

        # Try adding: ["SELF_HARM"] to prove kill-switch
        "risk_flags": [],

        # Targets not allowed to be contacted
        "blocked_targets": [],
    }

    # -------------------------------
    # ACTION HISTORY (RATE LIMIT PROOF)
    # -------------------------------
    action_history = {
        "actions_sent": 0  # Try changing to 3 to trigger RATE_LIMIT_EXCEEDED
    }

    # -------------------------------
    # EXECUTION (THIS IS THE TEST)
    # -------------------------------
    try:
        result = runtime.execute_action(
            action_request=action_request,
            enforcement_context=enforcement_context,
            action_history=action_history,
        )
        print("✅ ACTION RESULT:", result)

    except RuntimeError as e:
        # 🚨 EXPECTED for blocked cases
        print("❌ ACTION STOPPED BY ENFORCEMENT")
        print(str(e))


if __name__ == "__main__":
    main()
