"""
EXECUTOR RUNTIME — AUTHORIZATION LOCKED

ABSOLUTE RULE:
No action executes without valid authorization.
"""

import hashlib

ENGINE_VERSION = "EXECUTOR_v1.0_LOCKED"


class ExecutorRuntime:
    def execute(self, *, authorization: dict) -> dict:
        # 1️⃣ Must explicitly allow execution
        if authorization.get("execution_allowed") is not True:
            return self._refuse("EXECUTION_NOT_ALLOWED")

        # 2️⃣ Token must exist
        token = authorization.get("execution_token")
        if not token:
            return self._refuse("MISSING_EXECUTION_TOKEN")

        # 3️⃣ Scope must exist
        scope = authorization.get("execution_scope")
        if not scope:
            return self._refuse("MISSING_EXECUTION_SCOPE")

        # ✅ Execution permitted (stub)
        return {
            "status": "EXECUTED",
            "execution_token": token,
        }

    def _refuse(self, reason: str) -> dict:
        return {
            "status": "REFUSED",
            "reason": reason,
        }
