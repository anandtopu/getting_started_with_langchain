# LCEL and Runnables: quiz

**What does the pipe operator connect?**

<details><summary>Answer</summary>

The output of one runnable to the input of the next.

</details>

**Do parallel branches consume one another's output?**

<details><summary>Answer</summary>

No. Each receives the same initial input.

</details>

**What input does assign require?**

<details><summary>Answer</summary>

A dictionary; it preserves existing fields and adds computed fields.

</details>

**What distinguishes retry from fallback?**

<details><summary>Answer</summary>

Retry repeats a path; fallback chooses another runnable after a failure.

</details>

**Where should tags and metadata go?**

<details><summary>Answer</summary>

Execution config, without secrets or sensitive prompt content.

</details>

**Is every astream_events item a token?**

<details><summary>Answer</summary>

No. Many events describe starts, ends or intermediate pipeline activity.

</details>

**When should you choose LangGraph?**

<details><summary>Answer</summary>

When explicit state, durable execution, loops or human interruptions require more than a fixed dataflow.

</details>
