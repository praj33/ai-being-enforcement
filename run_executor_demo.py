from executor_runtime import ExecutorRuntime

executor = ExecutorRuntime()

# ✅ Allowed case
allowed_auth = {
    "execution_allowed": True,
    "execution_token": "deterministic_token_example",
    "execution_scope": {
        "action": "SEND_MESSAGE",
        "platform": "INSTAGRAM",
        "target": "user_42",
    },
}

print(executor.execute(authorization=allowed_auth))


# ❌ Blocked case (no token)
blocked_auth = {
    "execution_allowed": True,
    "execution_scope": {
        "action": "SEND_MESSAGE",
        "platform": "INSTAGRAM",
        "target": "user_42",
    },
}

print(executor.execute(authorization=blocked_auth))
