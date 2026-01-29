from enforcement_authorizer import ExecutionAuthorizer

auth = ExecutionAuthorizer()

ALLOW = auth.authorize(
    enforcement_result={"decision": "EXECUTE"},
    execution_scope={
        "action_type": "SEND_MESSAGE",
        "platform": "INSTAGRAM",
        "target": "user_42",
    },
)

BLOCK = auth.authorize(
    enforcement_result={"decision": "REWRITE"},
    execution_scope={
        "action_type": "SEND_MESSAGE",
        "platform": "INSTAGRAM",
        "target": "user_42",
    },
)

ALLOW_AGAIN = auth.authorize(
    enforcement_result={"decision": "EXECUTE"},
    execution_scope={
        "action_type": "SEND_MESSAGE",
        "platform": "INSTAGRAM",
        "target": "user_42",
    },
)

print("ALLOW →", ALLOW)
print("BLOCK →", BLOCK)
print("ALLOW AGAIN →", ALLOW_AGAIN)
