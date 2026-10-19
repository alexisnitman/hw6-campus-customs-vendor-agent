import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from agent import run_document, usage_record


ROOT = Path(__file__).resolve().parent
DOCS = sorted((ROOT / "data 6" / "practice_docs").iterdir())
OUT = ROOT / "output" / "cache_test.json"


async def main() -> None:
    records: list[dict] = []
    for setup in ("cached", "uncached"):
        for doc in DOCS:
            relative = "data/" + str(doc.relative_to(ROOT / "data 6"))
            answer, usage = await run_document(relative, setup, f"{setup}-{doc.name}-{datetime.now(timezone.utc).isoformat()}")
            records.append({
                "setup": setup,
                "document": relative,
                "usage": usage_record(usage, relative, setup),
                "answer": answer.model_dump(mode="json"),
            })
    OUT.write_text(json.dumps(records, indent=2) + "\n")
    print(f"Wrote {len(records)} records to {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
