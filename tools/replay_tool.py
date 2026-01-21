"""
REPLAY TOOL
===========
Deterministically replays enforcement decisions
from stored traces (JSON ARRAY).
"""

import json
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from enforcement_engine import enforce
from models.enforcement_input import EnforcementInput
from utils.deterministic_trace import generate_trace_id


def replay_trace(trace: dict) -> bool:
    input_snapshot = trace["input_snapshot"]
    expected_trace_id = trace["trace_id"]
    expected_decision = trace["final_decision"]

    enforcement_input = EnforcementInput(
        intent=input_snapshot["intent"],
        emotional_output=input_snapshot["emotional_output"],
        age_gate_status=input_snapshot["age_gate_status"],
        region_policy=input_snapshot["region_policy"],
        platform_policy=input_snapshot["platform_policy"],
        karma_score=input_snapshot.get("karma_score", 0.0),
        risk_flags=input_snapshot.get("risk_flags", []),
    )

    decision = enforce(enforcement_input)

    recomputed_trace_id = generate_trace_id(
        input_payload=input_snapshot,
        enforcement_category=expected_decision,
    )

    trace_match = recomputed_trace_id == expected_trace_id
    decision_match = decision.decision == expected_decision

    print("—" * 60)
    print(f"Trace ID match     : {'✅' if trace_match else '❌'}")
    print(f"Decision match     : {'✅' if decision_match else '❌'}")
    print(f"Expected decision  : {expected_decision}")
    print(f"Replayed decision  : {decision.decision}")
    print(f"Trace ID           : {expected_trace_id}")

    return trace_match and decision_match


def main(trace_file: str):
    with open(trace_file, "r", encoding="utf-8") as f:
        traces = json.load(f)

    print(f"\nLoaded {len(traces)} trace(s)\n")

    all_passed = True
    for trace in traces:
        if not replay_trace(trace):
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("REPLAY VERIFIED ✅ — SYSTEM IS DETERMINISTIC")
    else:
        print("REPLAY FAILED ❌ — NON-DETERMINISM DETECTED")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/replay_tool.py <trace_file>")
        sys.exit(1)

    main(sys.argv[1])
