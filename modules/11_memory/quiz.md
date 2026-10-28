# Memory and state: quiz

**Does a checkpointer train the model?**

<details><summary>Answer</summary>

No. It saves state that the application can restore and send in later requests.

</details>

**Is thread_id authentication?**

<details><summary>Answer</summary>

No. The host must authorize the customer and construct or validate the storage scope.

</details>

**What survives with InMemorySaver after process exit?**

<details><summary>Answer</summary>

Nothing; use durable storage when restart recovery matters.

</details>

**Why not keep a tool result after deleting its tool call?**

<details><summary>Answer</summary>

Providers expect matching call/result structure; an orphaned result is an invalid conversation.

</details>

**Can a summary prove a refund was approved?**

<details><summary>Answer</summary>

No. Preserve approval evidence in authoritative application state, not a model summary.

</details>

**How does a store differ from a checkpointer?**

<details><summary>Answer</summary>

A checkpointer saves workflow/thread state; a store holds scoped records reusable across conversations.

</details>
