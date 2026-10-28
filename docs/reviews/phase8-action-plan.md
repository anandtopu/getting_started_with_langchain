# Phase 8 review action plan

## Release gate

The educational repository can be published with transparent evidence and limitations. The customer-support application cannot be released to customers while the strict answer-quality gate fails. Infrastructure tests do not override that decision.

## Fix queue

| ID | Priority | Owner | Action | Acceptance check |
|---|---|---|---|---|
| R1 | P2 | Course maintainer | Disable Personal Ops raw tracing. Completed. | Agent invocation runs in tracing_context(enabled=False); server tracing is disabled. |
| R2 | P2 | Course maintainer | Validate exact MCP discovery fields. Completed. | Both memory and stdio capstone cases pass with reviewed schemas. |
| R3 | P3 | Course maintainer | Match actual citation evidence in API test. Completed. | Test resolves tool-result citations and checks each source appears in SSE answer. |
| R4 | P2 | Course maintainer | Record observed checks and explicit gaps. | Final checklist matches measured logs and remote CI evidence. |
| R5 | P1 before customer use | Application owner | Improve policy relevance without changing held-out facts. | All six cases pass, with separate live/human assessment and no ownership regression. |

## Follow-up backlog

- Run every applicable example on Ollama and at least one hosted provider; retain capability and failure records.
- Measure fresh-clone time to a real first model call on representative learner hardware.
- Before public app hosting: add production identity, resource isolation, coordinated admission, managed persistence and retention procedures.
- Expand independent evaluation sets beyond the small synthetic baselines; treat quote validation and semantic correctness as separate gates.
