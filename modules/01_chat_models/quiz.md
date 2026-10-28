# Chat models and messages: quiz

**Does bind_tools execute a tool?**

<details><summary>Answer</summary>

No. Binding describes tools; application code executes requested calls.

</details>

**What matches a ToolMessage to a request?**

<details><summary>Answer</summary>

tool_call_id must match the AIMessage tool call id.

</details>

**What does await do?**

<details><summary>Answer</summary>

It waits for a coroutine result while allowing the event loop to progress on other work.

</details>

**Are reasoning tokens added to output_tokens again?**

<details><summary>Answer</summary>

No. They are normally a detail within output tokens, not additional billable output to double-count.

</details>

**Is missing usage zero cost?**

<details><summary>Answer</summary>

No. The usage or estimate is unknown; local and explicit fake calls are labelled separately.

</details>

**Does a rate limiter cap the number of concurrent requests?**

<details><summary>Answer</summary>

Not by itself. It limits starts per time interval; concurrency limits in-flight work.

</details>

**Can a text-only model read an image filename?**

<details><summary>Answer</summary>

It can read the name as text, but needs image pixels and vision capability to inspect the picture.

</details>
