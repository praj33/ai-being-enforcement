"""
DAY-2(a) — ACTION-LEVEL ENFORCEMENT PROOF
"""

import sys
from pathlib import Path

# Ensure repo root is on path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from action_enforcement import ActionEnforcementGateway


gateway = ActionEnforcementGateway()

# --------------------------------------------------
# BLOCKED ACTION — MUST FAIL
# --------------------------------------------------
blocked_action = {
    "action_type": "SEND_MESSAGE",
    "platform": "WHATSAPP",
    "target": "blocked_user_123",
    "payload": "hello",
}

blocked_context = {
    "content_decision": "EXECUTE",
    "risk_flags": [],
    "blocked_targets": ["blocked_user_123"],
}

blocked_history = {
    "actions_sent": 0,
}

blocked_result = gateway.approve_action(
    action_request=blocked_action,
    context=blocked_context,
    action_history=blocked_history,
)

print("\n[BLOCKED ACTION RESULT]")
print(blocked_result)

# --------------------------------------------------
# ALLOWED ACTION — MUST PASS
# --------------------------------------------------
allowed_action = {
    "action_type": "SEND_MESSAGE",
    "platform": "INSTAGRAM",
    "target": "friend_456",
    "payload": "hello",
}

allowed_context = {
    "content_decision": "EXECUTE",
    "risk_flags": [],
    "blocked_targets": [],
}

allowed_history = {
    "actions_sent": 1,
}

allowed_result = gateway.approve_action(
    action_request=allowed_action,
    context=allowed_context,
    action_history=allowed_history,
)

print("\n[ALLOWED ACTION RESULT]")
print(allowed_result)
