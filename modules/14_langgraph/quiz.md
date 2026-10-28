# LangGraph fundamentals: quiz


1. Does TypedDict validate untrusted amounts at runtime?

<details>
<summary>Answer</summary>

No. Validate untrusted inputs explicitly, for example with Pydantic, before using them.

</details>

2. Why does a parallel report list need a reducer?

<details>
<summary>Answer</summary>

Several workers update the same field in one step; the reducer defines how to combine those writes.

</details>

3. What executes again when an interrupted node resumes?

<details>
<summary>Answer</summary>

The node starts from its beginning. Completed task results can be replayed in the Functional API, but arbitrary effects still need idempotency.

</details>

4. Can approval override the warehouse checks?

<details>
<summary>Answer</summary>

No. The writer rechecks eligibility, ownership and quantity even after approval.

</details>

5. Is a thread ID authentication?

<details>
<summary>Answer</summary>

No. The host must authorize access to the selected thread and its persisted state.

</details>

6. Does queueing a notification mean the customer received it?

<details>
<summary>Answer</summary>

No. This outbox is local pending work; an actual delivery worker and delivery evidence are separate.

</details>
