import json
import sys
from pathlib import Path

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from enforcement_engine import enforce

from models.enforcement_input import EnforcementInput

LOG_FILE = Path("logs/replayable_traces.json")


def replay(trace_id: str):
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if record["trace_id"] == trace_id:
                return record
    raise ValueError("Trace ID not found")


def rebuild_input(snapshot: dict) -> EnforcementInput:
    return EnforcementInput(
        intent=snapshot["intent"],
        emotional_output=snapshot["emotional_output"],
        age_gate_status=snapshot["age_gate_status"],
        region_policy=snapshot["region_policy"],
        platform_policy=snapshot["platform_policy"],
        karma_score=snapshot["karma_score"],
        risk_flags=snapshot["risk_flags"],
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python replay/replay_enforcement.py <trace_id>")
        sys.exit(1)

    trace_id = sys.argv[1]
    record = replay(trace_id)

    enforcement_input = rebuild_input(record["input_snapshot"])
    decision = enforce(enforcement_input)

    result = {
        "trace_id": trace_id,
        "original_decision": record["final_decision"],
        "replayed_decision": decision.decision,
        "match": record["final_decision"] == decision.decision,
    }

    print(json.dumps(result, indent=2))
