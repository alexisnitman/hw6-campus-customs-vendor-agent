# Shop handbook token and cost estimate

## Token count

File measured: `data 6/shop_handbook.md`

The handbook contains 28,903 characters and 6,127 whitespace-separated words. I counted tokens with `tiktoken` using the `o200k_base` GPT-style encoding, which produced **10,058 tokens**. The assignment’s `gpt-6-luna` price list does not specify a tokenizer name, so this is a reproducible estimate rather than a claim about a private tokenizer used by that model.

## Price used

From `data 6/prices.json` for `gpt-6-luna`:

- Regular input: `$0.10` per 1,000,000 tokens
- Cached input: `$0.01` per 1,000,000 tokens
- Cache write: `$0.125` per 1,000,000 tokens

These calculations cover the handbook input only. They do not include output tokens or any other prompt content.

## Math

### One call without caching

`10,058 / 1,000,000 × $0.10 = $0.0010058`

So, one call costs approximately **$0.00101** for the handbook input.

### 1,000 calls without caching

`1,000 × $0.0010058 = $1.0058`

So, 1,000 uncached calls cost approximately **$1.00580**.

### One call using a cached handbook

After the handbook has been written to the cache, the cached read costs:

`10,058 / 1,000,000 × $0.01 = $0.00010058`

So, one cached call costs approximately **$0.00010** for the handbook read. The first call also has a cache-write charge:

`10,058 / 1,000,000 × $0.125 = $0.00125725`

If the first call’s cache write and regular input are both counted, the initial setup call costs `$0.0010058 + $0.00125725 = $0.00226305`; later calls use the cached-read amount.

### 1,000 calls with caching

For the simple comparison of 1,000 cached reads after setup:

`1,000 × $0.00010058 = $0.10058`

Adding one cache-write charge gives:

`$0.10058 + $0.00125725 = $0.10183725`

So, 1,000 calls with caching cost approximately **$0.10184**, assuming the cache is written once and then reused. If the first call is also counted as a regular uncached read, the total is `$0.10274247`.
