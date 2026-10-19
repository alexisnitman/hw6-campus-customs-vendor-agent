import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from agent import run_document, usage_record

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "layer_usage.json"


async def main():
    rows = []
    for defense in ("none", "code", "design", "prompt"):
        for doc in sorted((ROOT / "data 6" / "practice_docs").iterdir()):
            path = "data/" + str(doc.relative_to(ROOT / "data 6"))
            _, usage = await run_document(path, "uncached", f"layer-{defense}-{doc.name}-{datetime.now(timezone.utc).timestamp()}", defense)
            rows.append({"defense": defense, "document": doc.name, **usage_record(usage, path, defense)})
    OUT.write_text(json.dumps(rows, indent=2) + "\n")
    print(f"Wrote {len(rows)} layer measurements")


if __name__ == "__main__":
    asyncio.run(main())
