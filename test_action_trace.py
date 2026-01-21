from action_enforcement import ActionEnforcementGateway

# 1️⃣ Create gateway instance
gateway = ActionEnforcementGateway()

# 2️⃣ Fixed action input (DO NOT CHANGE)
action_request = {
    "action_type": "SEND_MESSAGE",
    "platform": "INSTAGRAM",
    "target": "user_123",
}

context = {
    "content_decision": "EXECUTE",
    "risk_flags": []
}

action_history = {
    "actions_sent": 0
}

# 3️⃣ First call
result_1 = gateway.approve_action(
    action_request=action_request,
    context=context,
    action_history=action_history,
)

# 4️⃣ Second call (SAME INPUT)
result_2 = gateway.approve_action(
    action_request=action_request,
    context=context,
    action_history=action_history,
)

print("RUN 1 TRACE ID:", result_1["trace_id"])
print("RUN 2 TRACE ID:", result_2["trace_id"])

print("SAME TRACE:", result_1["trace_id"] == result_2["trace_id"])

# 5️⃣ Change ONE thing only
action_request_modified = {
    "action_type": "SEND_MESSAGE",
    "platform": "INSTAGRAM",
    "target": "user_999",  # ONLY CHANGE
}

result_3 = gateway.approve_action(
    action_request=action_request_modified,
    context=context,
    action_history=action_history,
)

print("RUN 3 TRACE ID (MODIFIED):", result_3["trace_id"])
print("DIFFERENT TRACE:",
      result_1["trace_id"] != result_3["trace_id"])
