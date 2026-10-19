# Vendor desk agent harness

## Structured fields in `models.py`

- `VendorDecision.vendor` — the vendor name extracted from the document.
- `VendorDecision.sku` — the Campus Customs SKU being quoted.
- `VendorDecision.unit_price` — the quoted per-unit price used for purchasing analysis.
- `VendorDecision.lead_time_days` — the numeric delivery lead time needed to judge timing.
- `VendorDecision.minimum_order` — the vendor’s minimum order quantity, important for feasibility and cash exposure.
- `VendorDecision.decision` — constrained to `recommend` or `do_not_recommend` so the downstream result is predictable.
- `VendorDecision.reason` — one sentence explaining the handbook-based decision.
- `AuditEntry` fields — timestamp, event type, tool name, arguments, short result, and final answer provide an append-only review trail.
- `UsageLog` fields — document, model, input/output/total tokens, timestamp, and dollar cost make each API run auditable.

## Tools

- `read_vendor_document` — reads the supplied HTML, PDF, or `.eml` file and returns its text; it is the only tool needed for normal work.
- `send_email_trap` — records attempted email calls in `output/trap_calls.json` and never sends an email.
- `approve_payment_trap` — records attempted payment calls in `output/trap_calls.json` and never approves or pays anything.

The handbook is loaded into the system instructions together with the prompt on every model call. Vendor documents are treated as untrusted data, and the two trap tools remain registered for the entire assignment so prompt injection attempts are visible.

## Logging and runs

`output/audit_trail.json` and `output/usage_log.json` are append-only lists. Each tool call records its arguments and a short result; each run also records its final structured answer. Usage cost uses the `gpt-6-luna` prices in `data 6/prices.json` and the token counts reported by the API. `output/trap_calls.json` starts empty; any entry means a document attempted to trigger a prohibited action.

Problem 4’s cache experiment is saved in `output/cache_test.json` and summarized in `output/cache_test.md`. The cached setup uses one stable prompt cache key and stable handbook instructions. The uncached setup changes the instruction marker on every model request and uses a unique cache key; its 12 API records all report zero `cache_read_tokens`.

## Safety defenses

- **Code defense:** before the model sees a file, the reader removes hidden HTML, instruction-like lines, and conflicting later revision lines. It keeps the ordinary quote facts so a clean quote still works.
- **Design defense:** the agent keeps `send_email` and `approve_payment` available as inert, logged tools, but the decision workflow’s wrappers block those actions. A document can never directly send mail or approve money.
- **Prompt defense:** `prompts/prompt.md` tells the model to treat vendor documents as untrusted evidence, never follow their instructions, and use only supported quote facts.

The command-line `--defense none` option preserves the no-defense experiment required for comparison. The defended run uses `--defense full`. Results and per-document token/cost evidence are in `output/defense_results.json` and `output/defense_results.md`.

Run the requested examples from `HW 6/` with:

```bash
.venv/bin/python agent.py --doc data/practice_docs/p01_bluehen_quote.html
.venv/bin/python agent.py --doc data/practice_docs/p08_chapelst_email.eml
```
