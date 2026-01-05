import json
import sys
from datetime import datetime
from typing import Dict, Any


def log_enforcement_event(event: Dict[str, Any]) -> None:
    """
    Structured Enforcement Logger (Bucket-compatible)

    Guarantees:
    - Always emits valid JSON
    - Always includes trace_id
    - Never raises exceptions
    - Deterministic structure
    - stdout-based (Render / container friendly)

    This simulates Bucket ingestion.
    In production, stdout can be replaced with HTTP POST.
    """

    try:
        log_record = {
            "type": "ENFORCEMENT_EVENT",
            "timestamp": datetime.utcnow().isoformat(),
            "trace_id": event.get("trace_id", "UNKNOWN_TRACE"),
            "event": event,
        }

        # Write to stdout (safe for containers & Render)
        sys.stdout.write(json.dumps(log_record, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    except Exception:
        # HARD FAIL SAFE: logging must NEVER crash enforcement
        fallback = {
            "type": "ENFORCEMENT_LOGGER_FAILURE",
            "timestamp": datetime.utcnow().isoformat(),
            "trace_id": "UNKNOWN_TRACE",
            "event": "logger_exception",
        }
        sys.stdout.write(json.dumps(fallback) + "\n")
        sys.stdout.flush()
