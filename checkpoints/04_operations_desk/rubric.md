# Operations Desk rubric

Score each area 0 (missing), 1 (partially demonstrated) or 2 (implemented with evidence), for ten possible points.

| Area | Evidence for two points |
|---|---|
| Routing | Validated role allowlist, confidence fallback and deterministic aggregation |
| Tool permissions | Customer-scoped SQL; public-only product retrieval; no write or shell tools |
| Context boundaries | Worker projection excludes unrelated conversation and identity fields |
| Budgets and failure handling | Bounded worker count, per-agent calls and preserved denials |
| Evaluation and explanation | Reproducible report, actual graph diagram and candid written tradeoffs |

A perfect offline score demonstrates these program contracts. It does not establish live model accuracy, production security or deployed authentication.
