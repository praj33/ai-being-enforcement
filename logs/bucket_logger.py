"""
BUCKET LOGGER
-------------
Canonical, deterministic enforcement logging.

Properties:
- JSON ARRAY ONLY (no JSONL)
- Replay-safe
- Deterministic serialization
- Append-with-rewrite (single-node safe)
- NEVER breaks enforcement
"""

from pathlib import Path
import json
from typing import List, Any, Dict

from __version__ import ENGINE_VERSION

# -------------------------------------------------
# PATH RESOLUTION (ABSOLUTE, STABLE)
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "replayable_traces.json"


# -------------------------------------------------
# INTERNAL NORMALIZATION
# -------------------------------------------------

def _normalize_input_snapshot(input_snapshot: Any) -> Dict[str, Any]:
    """
    Convert EnforcementInput (or dict) into a deterministic dict.
    """
    if isinstance(input_snapshot, dict):
        return {
            "intent": input_snapshot.get("intent"),
            "emotional_output": input_snapshot.get("emotional_output", {}),
            "age_gate_status": input_snapshot.get("age_gate_status"),
            "region_policy": input_snapshot.get("region_policy"),
            "platform_policy": input_snapshot.get("platform_policy"),
            "karma_score": input_snapshot.get("karma_score", 0.0),
            "risk_flags": input_snapshot.get("risk_flags", []),
        }

    # Assume Pydantic / object
    return {
        "intent": input_snapshot.intent,
        "emotional_output": input_snapshot.emotional_output,
        "age_gate_status": input_snapshot.age_gate_status,
        "region_policy": input_snapshot.region_policy,
        "platform_policy": input_snapshot.platform_policy,
        "karma_score": input_snapshot.karma_score,
        "risk_flags": input_snapshot.risk_flags,
    }


# -------------------------------------------------
# PUBLIC LOGGER
# -------------------------------------------------

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

    ABSOLUTE RULE:
    - MUST NEVER throw
    """

    try:
        record = {
            "trace_id": trace_id,
            "engine_version": ENGINE_VERSION,
            "input_snapshot": _normalize_input_snapshot(input_snapshot),
            "akanksha_verdict": {
                "decision": akanksha_verdict.get("decision"),
                "risk_category": akanksha_verdict.get("risk_category"),
                "confidence": akanksha_verdict.get("confidence"),
            },
            "raj_evaluators": sorted(
                [
                    {
                        "name": r.name,
                        "action": r.action,
                        "triggered": r.triggered,
                    }
                    for r in evaluator_results
                ],
                key=lambda x: x["name"],
            ),
            "final_decision": final_decision,
        }

        # -------------------------------
        # ENSURE DIRECTORY EXISTS
        # -------------------------------
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        # -------------------------------
        # LOAD EXISTING LOG (ARRAY)
        # -------------------------------
        if LOG_FILE.exists():
            try:
                with LOG_FILE.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except Exception:
                data = []
        else:
            data = []

        # -------------------------------
        # APPEND RECORD
        # -------------------------------
        data.append(record)

        # -------------------------------
        # WRITE BACK CANONICAL JSON
        # -------------------------------
        with LOG_FILE.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                sort_keys=True,
                ensure_ascii=True,
            )

    except Exception:
        # LOGGING MUST NEVER BLOCK ENFORCEMENT
        pass
