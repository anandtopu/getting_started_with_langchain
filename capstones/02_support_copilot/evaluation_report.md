# Evaluation report

Measured 2026-10-28 using the actual reference solution with scripted models and network denial. This is interface and contract evidence, not live-model quality.

| Case | Complete contract |
|---|---|
| order-known | Pass |
| order-denied | Pass |
| returns | Fail |
| shipping | Fail |
| clarify | Pass |
| hostile-order | Pass |

4/6 complete contracts. Reproduce with `uv run --extra apps python scripts/evaluate.py --offline`. Full answer/evidence payloads are written to the ignored runtime report.

Return and shipping answers miss expected facts despite exact source support. All six HTTP paths complete, with correct tool trajectory and ownership. The strict customer release gate remains false. The separate API tests verify manager review, rejection and idempotency.
