# Workflow patterns: quiz


1. What distinguishes a gate from a prompt instruction?

<details>
<summary>Answer</summary>

A gate runs code that can block the next step; a prompt merely requests behavior.

</details>

2. Why sort worker results?

<details>
<summary>Answer</summary>

Concurrent completion order need not be stable; sorting makes presentation deterministic.

</details>

3. What does Send carry?

<details>
<summary>Answer</summary>

The destination node and the input for one dynamically created worker task.

</details>

4. Should a planner be allowed to name arbitrary tools or categories?

<details>
<summary>Answer</summary>

No. Validate plans against a finite allowlist and a worker budget.

</details>

5. How many calls can six workers plus two draft/evaluate rounds make?

<details>
<summary>Answer</summary>

Ten logical model calls, before any provider retries.

</details>

6. Does a passing structural gate prove factual accuracy?

<details>
<summary>Answer</summary>

No. It verifies the chosen format conditions; semantic correctness needs separate evaluation.

</details>
