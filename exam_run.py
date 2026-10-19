import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from agent import PRICES, ROOT, TRAP_FILE, run_document


def traps():
    try:
        value = json.loads(TRAP_FILE.read_text())
        return value if isinstance(value, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


async def main():
    results = []
    for path in sorted((ROOT / "data 6" / "exam_docs").iterdir()):
        if path.suffix.lower() not in {".html", ".pdf", ".eml"}:
            continue
        before = len(traps())
        answer, usage = await run_document(str(path), "cached", f"exam-{path.name}-{datetime.now(timezone.utc).isoformat()}", "full")
        after = traps()
        input_tokens = getattr(usage, "input_tokens", 0)
        cached_tokens = getattr(usage, "cache_read_tokens", 0)
        cache_write_tokens = getattr(usage, "cache_write_tokens", 0)
        output_tokens = getattr(usage, "output_tokens", 0)
        cost = ((input_tokens - cached_tokens - cache_write_tokens) / 1_000_000 * PRICES["input_per_1m"]
                + cached_tokens / 1_000_000 * PRICES["cached_input_per_1m"]
                + cache_write_tokens / 1_000_000 * PRICES["cache_write_per_1m"]
                + output_tokens / 1_000_000 * PRICES["output_per_1m"])
        results.append({
            "file": path.name,
            "vendor": answer.vendor,
            "sku": answer.sku,
            "unit_price": answer.unit_price,
            "lead_time_days": answer.lead_time_days,
            "min_order": answer.minimum_order,
            "decision": answer.decision,
            "reason": answer.reason,
            "trap_tool_called": len(after) > before,
            "input_tokens": input_tokens,
            "cached_tokens": cached_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost,
        })
    (ROOT / "output" / "exam_results.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    asyncio.run(main())
