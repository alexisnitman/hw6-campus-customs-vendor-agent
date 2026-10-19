# HW6 — Campus Customs vendor desk

This repository contains the complete HW6 vendor-document agent, its safety experiments, the 10-document exam run, and the full `data 6/` course data pack. The two files in `data 6/my_attacks/` are the original red-team attack documents.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put a real `PORTKEY_API_KEY` in the local `.env`. The real `.env` is ignored by Git and is not included in this repository.

## Run the agent

From this folder, run one vendor document with the final defended path:

```bash
python agent.py --doc "data 6/exam_docs/e01_quote.html" --defense full
```

The agent also supports HTML, PDF, and `.eml` documents. The no-defense comparison path is available for testing:

```bash
python agent.py --doc "data 6/practice_docs/p01_bluehen_quote.html" --defense none
```

Each run appends usage information to `output/usage_log.json` and audit information to `output/audit_trail.json`. Trap tools remain installed, but they never send email or approve payment; attempted calls are recorded in `output/trap_calls.json`.

## Included results

- `output/hw6_report.html` — self-contained offline manager report.
- `output/exam_results.json` — final defended results for all 10 exam documents.
- `output/cache_test.*`, `output/attack_results.*`, `output/defense_results.*`, and `output/red_team.md` — experiment evidence.
- `data 6/shop_handbook.md`, `prices.json`, `practice_key.json`, practice documents, exam documents, and the two files in `my_attacks/`.

The expected top-level agent files are `agent.py`, `tools.py`, `models.py`, and `prompts/prompt.md`.
