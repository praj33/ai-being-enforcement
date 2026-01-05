import json
import sys
from datetime import datetime
from typing import Dict, Any


def log_enforcement_event(event: Dict[str, Any]) -> None:
    """
    Production-safe structured logger.

    This simulates Bucket ingestion.
    In production, this would POST to a log sink.
    """

    log_record = {
        "timestamp": datetime.utcnow().isoformat(),
        **event,
    }

    # stdout logging (Render / container friendly)
    sys.stdout.write(json.dumps(log_record) + "\n")
    sys.stdout.flush()
