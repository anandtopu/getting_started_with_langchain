# Evaluation report

Measured 2026-10-28 using the actual reference solution with scripted models and network denial. This is interface and contract evidence, not live-model quality.

| Case | Complete contract |
|---|---|
| returns | Pass |
| shipping | Pass |
| unknown | Pass |

3/3 complete contracts. Reproduce with `uv run --extra apps python scripts/evaluate.py --offline`. Full answer/evidence payloads are written to the ignored runtime report.

The return-window case checks 30 days and page 2; shipping checks $5.95 and 3-5 business days on page 3; an unrelated query abstains with no citation. Both retrieval interfaces execute, but fake vectors do not measure semantic search quality. Three synthetic cases are a small baseline, not broad document coverage.
