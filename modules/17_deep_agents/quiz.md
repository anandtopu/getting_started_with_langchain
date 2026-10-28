# Deep Agents (optional): quiz


1. Does a todo entry run the task it describes?

<details>
<summary>Answer</summary>

No. The application or agent must execute the necessary tools and record their results.

</details>

2. Can VirtualFiles read the host .env file?

<details>
<summary>Answer</summary>

No. Model paths are never mapped to the host filesystem, and unknown virtual paths are rejected.

</details>

3. What does StateBackend store?

<details>
<summary>Answer</summary>

Files in graph state. It is distinct from a backend with access to the host filesystem or a shell.

</details>

4. Why explicitly bound the general-purpose SDK child?

<details>
<summary>Answer</summary>

The SDK can add one automatically; explicit configuration makes its model and budget reviewable.

</details>

5. What does citation validation prove here?

<details>
<summary>Answer</summary>

That allowed sources exist and the draft identifies synthetic evidence. It does not prove entailment.

</details>

6. When does the search example contact Tavily?

<details>
<summary>Answer</summary>

Only with --web in a live configuration, with the search extra and key; offline mode rejects it.

</details>
