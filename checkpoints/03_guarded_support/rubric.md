# Guarded Support rubric

Score each area 0–2: missing, partial, complete. Aim for 8/10, with full marks for authorization and review integrity before proceeding.

| Area | Full marks |
|---|---|
| Authorization and policy | Identity comes from trusted context; ownership, delivery window, warehouse checks, exceptions and quantity are enforced in code. |
| Review integrity | Large refunds pause before the tool executes; reject writes nothing; approve still revalidates eligibility; model fields cannot grant approval. |
| Transaction reliability | Repeated and concurrent same-key requests write once; changed payloads conflict; a new key cannot return the same purchased unit again. |
| Bounded execution | Model/tool counts are bounded, graph-step allowance includes middleware overhead, and fallback/retry costs are explained. |
| Evidence and communication | All eight cases run; before-review and final write counts are reported; fixtures are never described as live model or injection-resistance accuracy. |

Acceptance tests check the central contracts, not a production authentication system. Review the actual tool traces and database records. A final assistant sentence claiming success is not proof of a write; a pending interrupt is not a completed request. A safe all-denied starter is incomplete because valid requests must also work.

Stretch: add a rejected warehouse exception and a changed-payload idempotency collision without weakening existing controls. Then demonstrate that a model-selected tool and a human-approved tool can both fail policy validation correctly.
