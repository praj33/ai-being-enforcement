"""
BUCKET LOGGER
-------------
Append-only deterministic enforcement logging.
Single source of truth for replay & audit.
"""

import json
from pathlib import Path
from typing import List

from __version__ import ENGINE_VERSION


LOG_FILE = Path("logs/replayable_traces.json")


def log_enforcement(
    *,
    trace_id: str,
    input_snapshot,
    akanksha_verdict: dict,
    evaluator_results: List,
    final_decision: str,
):
    """
    Append a deterministic enforcement record.
    Must NEVER throw.
    """

    try:
        record = {
            "trace_id": trace_id,
            "engine_version": ENGINE_VERSION,
            "input_snapshot": {
                "intent": input_snapshot.intent,
                "emotional_output": input_snapshot.emotional_output,
                "age_gate_status": input_snapshot.age_gate_status,
                "region_policy": input_snapshot.region_policy,
                "platform_policy": input_snapshot.platform_policy,
                "karma_score": input_snapshot.karma_score,
                "risk_flags": input_snapshot.risk_flags,
            },
            "akanksha_verdict": {
                "decision": akanksha_verdict["decision"],
                "risk_category": akanksha_verdict["risk_category"],
                "confidence": akanksha_verdict["confidence"],
            },
            "raj_evaluators": [
                {
                    "name": r.name,
                    "action": r.action,
                    "triggered": r.triggered,
                }
                for r in evaluator_results
            ],
            "final_decision": final_decision,
        }

        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")

    except Exception:
        # Logging must never break enforcement
        pass
