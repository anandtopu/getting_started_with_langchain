# Evaluation report

Measured 2026-10-28 using the actual reference solution with scripted models and network denial. This is interface and contract evidence, not live-model quality.

| Case | Complete contract |
|---|---|
| trends | Pass |
| market | Pass |
| exhausted | Pass |

3/3 complete contracts. Reproduce with `uv run --extra apps python scripts/evaluate.py --offline`. Full answer/evidence payloads are written to the ignored runtime report.

Two accepted reports require two draft attempts; the one-attempt case correctly refuses publication. Exact quotations and bounded calls are checked. The scripted critic does not establish editorial quality.
