# Evaluation report

Measured 2026-10-28 using the actual reference solution with scripted models and network denial. This is interface and contract evidence, not live-model quality.

| Case | Complete contract |
|---|---|
| status | Pass |
| category | Pass |
| revenue | Pass |
| exhausted | Pass |

4/4 complete contracts. Reproduce with `uv run --extra apps python scripts/evaluate.py --offline`. Full answer/evidence payloads are written to the ignored runtime report.

Independent totals: 200 orders, 470 units by category, 7,978,950 revenue cents. The exhaustion case passes by refusing to produce an accepted chart. Summary prose is not independently graded for business relevance.
