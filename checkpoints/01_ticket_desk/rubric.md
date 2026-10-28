# Smart Ticket Desk rubric

Score each item 0 (absent), 1 (partial), or 2 (complete with evidence). A passing implementation earns at least 10/12 and must earn 2 on ownership and limits. A live answer-quality claim needs separate live evidence.

| Criterion | Evidence for 2 points |
|---|---|
| Structured extraction | All five fields validated, nullable missing IDs, labels excluded from prompts |
| Manual tool protocol | Assistant requests preserved, allowlist dispatch, matching IDs and final reply |
| Ownership | Both order and shipment tools reject another customer's order, with no record disclosure |
| Limits and errors | Turn/call bounds, invalid-argument errors, unknown-tool rejection, no unbounded retries |
| Draft and audit | Unsent draft plus triage/tool results; seed database unchanged |
| Honest evaluation | Six fixture cases checked; quality and live security limits explicitly documented |

Review prompts:

- Change the customer from C001 to C002 while keeping BW1001. Explain why both reads are denied.
- Return repeated tool calls from the fake model. Show the bounded error and count executed calls.
- Supply no order ID. Explain why an invented identifier must not enter a query.
- Show one field-level error in an extraction and how it affects exact-match accuracy.
- Explain why a valid JSON request for a shell command still must not execute.
- Compare a real provider's draft to the verified results before attributing model quality.
