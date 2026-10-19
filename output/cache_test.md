# Handbook cache test

I ran all 12 files in `data 6/practice_docs/` twice: once with a stable handbook cache key and once with a per-call changing instruction marker and cache key. The uncached setup is validated by the API reporting `cache_read_tokens: 0` for all 12 calls. Cache writes are not cache reuse; they show that the provider prepared a new cache entry.

## Results

| Setup | Calls | Input tokens | Cached-read tokens | Cache-write tokens | Output tokens | Total cost | Cost/document |
|---|---:|---:|---:|---:|---:|---:|---:|
| With cache | 12 | 253,768 | 227,134 | 23,610 | 2,760 | **$0.00690499** | **$0.00057542** |
| Without cache | 12 | 254,670 | 0 | 251,646 | 2,632 | **$0.03307415** | **$0.00275618** |

The cache saved:

`($0.03307415 - $0.00690499) / $0.03307415 × 100 = 79.12%`

## How the dollar totals were calculated

For each call I used the API-reported fields saved in `output/cache_test.json`:

`regular_input_tokens × $0.10 / 1,000,000`

`+ cached_read_tokens × $0.01 / 1,000,000`

`+ cache_write_tokens × $0.125 / 1,000,000`

`+ output_tokens × $0.50 / 1,000,000`

The regular input portion is calculated as total input minus cached-read and cache-write tokens. Output is included in the real totals, unlike the Problem 2 handbook-only estimate.

## Comparison with Problem 2

Problem 2 estimated only the 10,058-token handbook: about `$1.00580` for 1,000 uncached handbook-only reads and about `$0.10184` for 1,000 cached reads, including one cache write. The actual test is more expensive per document because every request also includes the system prompt, tool definitions, the document text, tool-call follow-up messages, and model output. It also uses the API’s actual token counts rather than treating the handbook as the only input.

The measured average for 1,000 equivalent documents would be `$2.75618` without caching and `$0.57542` with caching. The cache comparison is therefore still a large saving, but it should not be compared directly to the handbook-only numbers without accounting for those extra tokens.

## Projection: 1,000 documents per day for 30 days

There would be `1,000 × 30 = 30,000` document calls.

- Without cache: `30,000 × $0.00275618 = $82.68540`.
- With cache: `30,000 × $0.00057542 = $17.26260`.
- Estimated savings: `$82.68540 - $17.26260 = $65.42280`, or about **79.12%**.

This projection assumes the same mix of document types, response lengths, and cache behavior as the 12-document test.

## What surprised me

The cached run did not make input tokens disappear: it still reported roughly 254,000 total input tokens. The important difference was that about 227,000 of those tokens were billed at the much lower cached-input rate. The first cached call also created cache entries, so its cost was higher than later cached calls. The uncached run reported zero cached reads but many cache writes because each unique request was allowed to create a new cache entry; those writes are billed separately and do not mean the call reused old content.
