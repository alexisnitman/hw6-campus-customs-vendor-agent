import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from agent import TRAP_FILE, run_document, usage_record

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "red_team_results.json"


def trap_snapshot():
    try:
        value = json.loads(TRAP_FILE.read_text())
        return value if isinstance(value, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


async def one(path: Path, defense: str):
    before = trap_snapshot()
    answer, usage = await run_document(str(path), "uncached", f"red-team-{path.stem}-{defense}-{datetime.now(timezone.utc).isoformat()}", defense)
    after = trap_snapshot()
    return {
        "document": str(path.relative_to(ROOT)),
        "defense": defense,
        "answer": answer.model_dump(mode="json"),
        "trap_called": len(after) > len(before),
        "new_trap_calls": after[len(before):],
        "usage": usage_record(usage, str(path), "uncached"),
    }


async def main():
    rows = []
    for path in sorted((ROOT / "data" / "my_attacks").iterdir()):
        if path.suffix.lower() in {".html", ".eml", ".pdf"}:
            for defense in ("none", "full"):
                print(f"Running {path.name} ({defense})")
                rows.append(await one(path, defense))
    OUT.write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    asyncio.run(main())
