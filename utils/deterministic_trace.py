import hashlib
import json
from typing import Any, Dict


ENGINE_VERSION = "3.0.0"


def normalize_input(payload: Dict[str, Any]) -> str:
    """
    Normalize enforcement input deterministically.
    """
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).lower()


def compute_trace_id(
    input_payload: Dict[str, Any],
    enforcement_category: str,
) -> str:
    """
    Deterministic trace identity.
    """
    normalized = normalize_input(input_payload)
    raw = f"{normalized}|{enforcement_category}|{ENGINE_VERSION}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# -------------------------------------------------
# PUBLIC API (Contract v3 expects this name)
# -------------------------------------------------
def generate_trace_id(
    input_payload: Dict[str, Any],
    enforcement_category: str,
) -> str:
    """
    Alias for compute_trace_id.
    This is the ONLY function enforcement_engine should call.
    """
    return compute_trace_id(input_payload, enforcement_category)
