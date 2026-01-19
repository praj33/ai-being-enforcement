import hashlib
import json
from typing import Any, Dict

from __version__ import ENGINE_VERSION


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


def generate_trace_id(
    input_payload: Dict[str, Any],
    enforcement_category: str,
) -> str:
    """
    Deterministic trace identity.

    IMPORTANT:
    - enforcement_category MUST be a string
    """

    if not isinstance(enforcement_category, str):
        # Fail-closed normalization
        enforcement_category = str(enforcement_category)

    normalized = normalize_input(input_payload)
    raw = f"{normalized}|{enforcement_category.lower()}|{ENGINE_VERSION}"

    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
