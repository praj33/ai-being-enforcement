"""
ENFORCEMENT → EXECUTION AUTHORIZER
Phase C — Execution Authorization Spine

ABSOLUTE RULE:
No execution token is ever produced unless execution is explicitly allowed.
FAIL-CLOSED. DETERMINISTIC. NON-BYPASSABLE.
"""

import hashlib
from typing import Dict

ENGINE_VERSION = "EXECUTION_AUTH_v1.0_LOCKED"


class ExecutionAuthorizer:
    """
    Converts enforcement decisions into execution authorization.
    """

    def authorize(
        self,
        *,
        enforcement_result: Dict,
        execution_scope: Dict,
    ) -> Dict:
        """
        enforcement_result:
          - decision: EXECUTE | REWRITE | BLOCK

        execution_scope:
          - action_type
          - platform
          - target
        """

        # 🔒 FAIL-CLOSED DEFAULT
        if enforcement_result.get("decision") != "EXECUTE":
            return {
                "execution_allowed": False,
                "execution_token": None,
                "reason": "NOT_AUTHORIZED",
            }

        token = self._deterministic_execution_token(
            enforcement_result,
            execution_scope,
        )

        return {
            "execution_allowed": True,
            "execution_scope": execution_scope,
            "execution_token": token,
        }

    def _deterministic_execution_token(
        self,
        enforcement_result: Dict,
        execution_scope: Dict,
    ) -> str:
        """
        Deterministic token.
        Same input → same token.
        """

        hash_input = (
            f"{enforcement_result}"
            f"{execution_scope}"
            f"{ENGINE_VERSION}"
        )

        return hashlib.sha256(hash_input.encode()).hexdigest()
