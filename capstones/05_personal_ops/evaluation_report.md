# Evaluation report

Measured 2026-10-28 using the actual reference solution with scripted models and network denial. This is interface and contract evidence, not live-model quality.

| Case | Complete contract |
|---|---|
| approved | Pass |
| denied | Pass |
| stdio | Pass |

3/3 complete contracts. Reproduce with `uv run --extra apps python scripts/evaluate.py --offline`. Full answer/evidence payloads are written to the ignored runtime report.

Approved memory/stdio runs write one note and one task; denial writes neither. This includes real protocol exchanges with two local SDK servers. Ownership, altered approvals and replay behavior have separate adversarial tests.
