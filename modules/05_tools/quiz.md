# Tools and tool calling: quiz

**Who runs a requested tool?**

<details><summary>Answer</summary>

The application dispatcher, not the model.

</details>

**Where must customer identity come from?**

<details><summary>Answer</summary>

Trusted application context or authentication, never the model-authored arguments.

</details>

**Does parameterized SQL guarantee authorization?**

<details><summary>Answer</summary>

No. It handles values safely, but a separate ownership predicate is required.

</details>

**Why preserve call IDs?**

<details><summary>Answer</summary>

They match each result to the exact pending request, including parallel calls.

</details>

**Should independent reads and refund writes use the same parallel strategy?**

<details><summary>Answer</summary>

No. Writes and dependencies need different controls; this lesson only parallelizes independent reads.

</details>

**What happens after the turn budget is exhausted?**

<details><summary>Answer</summary>

Raise a bounded failure and request human review, rather than continue indefinitely.

</details>

**Does ToolRuntime implement authentication?**

<details><summary>Answer</summary>

No. It transports context supplied by the application; the identity source must already be trusted.

</details>
