# Production Release rubric

| Area | Points | Observable acceptance |
|---|---:|---|
| Identity and session isolation | 20 | Missing token 401; other customer 403; identity cannot be supplied in the body. |
| Streaming and cleanup | 15 | SSE framing, no tool-body leakage, completed history, cancellation releases slots. |
| Reviewed actions | 20 | Trusted warehouse facts; current interrupt; policy/amount recheck; rejection writes nothing. |
| Resource and privacy controls | 15 | Persistent reservations, bounded concurrency, scrub-before-log and public-only SQL. |
| Honest evaluation and release gate | 20 | Independent labels, failed cases retained, strict release exits nonzero on failures. |
| Deployment evidence and rationale | 10 | Non-root container, runtime secrets, health, persistence reopen check, explicit remaining gaps. |

Pass the learning checkpoint at 80/100 with all access and side-effect controls passing. Learning completion is not production approval: a customer release separately requires every configured quality contract and the deployment review. Never compensate for unauthorized access with a higher average quality score.
