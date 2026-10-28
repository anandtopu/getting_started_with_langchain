# Evaluation report

The corrected offline HTTP path passes **6/6 complete contracts**, up from 4/6. The evaluation questions, expected facts, tool trajectories and release thresholds are unchanged. This is deterministic contract evidence, not live-model quality.

| Case | Complete contract |
|---|---|
| order-known | Pass |
| order-denied | Pass |
| returns | Pass |
| shipping | Pass |
| clarify | Pass |
| hostile-order | Pass |

The return-window answer now quotes 30 calendar days after delivery; standard shipping quotes 3 to 5 business days after dispatch. Grammatical normalization matches return/returned, and time-window questions require a duration in relevant evidence. No expected answer or policy number is embedded in the selector. Tests use changed durations (45 days and 8-12 days), paraphrases and missing evidence.

All six HTTP requests complete with correct ownership and tool trajectories. Citations retain exact source quotes. The separate API tests cover manager approval, rejection and idempotency. Removing a required fact still causes the strict gate to fail.

Reproduce all 19 capstone cases with `uv run --extra apps python scripts/evaluate.py --offline --release`. Run the engineering/quality rehearsal with `uv run --extra apps python checkpoints/05_production_release/solution.py --offline --release`. Both now succeed offline. Live-provider behavior and customer deployment remain unverified.
