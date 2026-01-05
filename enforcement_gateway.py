from datetime import datetime
from typing import Dict, Any

from enforcement_engine import enforce
from enforcement_logging.bucket_logger import log_enforcement


def enforce_gateway(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Live Enforcement Gateway.
    This is the final authority before user exposure.
    """

    trace_id = payload.get("trace_id")

    # -------- Hard Input Validation --------
    required_fields = [
        "trace_id",
        "text",
        "meta",
        "age_state",
        "region_state",
        "platform_policy",
        "karma_signal",
    ]

    for field in required_fields:
        if field not in payload:
            result = _block(
                trace_id,
                "missing_required_field",
                f"{field}_missing",
            )
            log_enforcement(payload, result)
            return result

    try:
        decision = enforce(payload)

    except Exception as e:
        result = _block(
            trace_id,
            "enforcement_crash",
            str(e),
        )
        log_enforcement(payload, result)
        return result

    # -------- Mandatory Logging --------
    log_enforcement(payload, decision)

    return {
        "enforcement_id": decision["enforcement_id"],
        "trace_id": trace_id,
        "decision": decision["final_decision"],
        "reason": decision["reason"],
    }


def _block(trace_id: str, reason: str, detail: str) -> Dict[str, Any]:
    return {
        "enforcement_id": f"block-{trace_id}",
        "trace_id": trace_id,
        "final_decision": "BLOCK",
        "reason": reason,
        "detail": detail,
        "timestamp": datetime.utcnow().isoformat(),
        "evaluator_results": [],
    }
