# Handbook Q&A rubric

Score each area from 0 to 2: 0 missing, 1 partial, 2 complete. Aim for 8/10 or better, with full marks for citation integrity and offline behaviour before proceeding.

| Area | Full marks |
|---|---|
| Ingestion and retrieval | Loads the handbook only, preserves one-based pages, returns relevant chunks, and keeps evaluation labels outside the index and generation prompts. |
| Citation integrity | Resolves IDs against retrieved evidence, checks exact quote membership, derives page/source in code, and rejects unsupported citations. |
| Abstention and boundaries | Unknown facts abstain with no citations; empty/oversized input is rejected; refund approval is described as strictly over $100. |
| Offline behaviour | Runs with no keys or network, labels fixtures, uses central factories, and makes no semantic-quality claims from fake outputs. |
| Evaluation and explanation | Runs all six cases, reports page hits separately from answer quality, inspects errors, and explains the limitations of exact-quote validation. |

The acceptance tests automate provenance, expected-page retrieval and unknown-case abstention. They do not award full semantic-correctness marks automatically. Manually read each answer and its source, especially numerical boundaries and exceptions. A working starter that always abstains is safe but incomplete.

Stretch: add a new answerable question and a new unsupported question without changing retrieval to recognise their wording. Re-run the existing cases to check for regressions, then explain whether the new cases remain a useful independent challenge after you have tuned against them.
