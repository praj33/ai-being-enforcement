import json
from pathlib import Path

LOG_FILE = Path("logs/replayable_traces.json")

with LOG_FILE.open("rb") as f:
    raw = f.read()

# Strip BOM and invisible unicode
clean = raw.decode("utf-8-sig").strip()

data = json.loads(clean)

with LOG_FILE.open("w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, sort_keys=True)

print("✅ Trace file repaired and normalized")
