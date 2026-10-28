# Operations Desk design rationale

The router has a narrow job: select zero to three allowed roles with confidence. Its structured result is validated before `Send` creates workers. Zero roles lead to clarification. A separate worker function runs the selected specialist, and a final node drafts the combined answer. This makes the sequence visible and prevents an open-ended delegation loop.

Customer identity comes from the host, outside the model-visible schema. Billing and logistics each receive one scoped SQL tool. Product receives a retrieval tool over the public synthetic catalogue. A specialist sees an order or SKU and a narrow task, rather than the complete customer history. Only its final draft and evidence return to the parent; its private conversation stays inside the child invocation. This limits context exposure but is not an authentication system: the host must authenticate the customer and authorize access to any persisted thread.

The report list has an append reducer because several workers may finish in the same graph step. The combining node sorts results by role so scheduling does not change presentation. `max_concurrency=2` limits simultaneous workers. Each child permits at most one tool call and three model calls; the router and synthesizer each make one call. Product RAG can add one generation call. The resulting ceiling is twelve logical model calls for a three-role case, before provider retries. There are no recursive worker capabilities.

The final answer is a draft, not a permission decision. SQL and citation checks determine whether evidence is usable. Tool denials remain in the report even when a model writes misleading prose. No specialist can issue a refund or notify a customer. A later integration can hand off to the separate reviewed return graph, with explicit host authorization and state mapping.

The additional routing and synthesis are useful when team-specific prompts or permissions must be maintained independently. For a single shipment lookup, they add latency, tokens and failure points. Module 16 measures the same read with one agent and with delegation. Offline timings measure local program overhead and fake-model work; they do not predict hosted latency or answer quality.

The acceptance cases deliberately test mechanisms: ownership denial, public/private separation, confidence fallback and role selection. They do not claim an eight-case model-quality score. Real-provider evaluation, remote CI and the production host's identity controls remain separate evidence requirements.
