# Structured output: quiz

**What does Pydantic validate?**

<details><summary>Answer</summary>

Types and declared constraints; not whether the extracted facts match the source.

</details>

**Does str | None make a field omissible?**

<details><summary>Answer</summary>

Not by itself. The value may be null; a default is needed if the key may be omitted.

</details>

**Does TypedDict validate at runtime?**

<details><summary>Answer</summary>

No. Add explicit validation when consuming dictionary outputs.

</details>

**How does repair differ from a transport retry?**

<details><summary>Answer</summary>

Repair adds feedback about invalid output; transport retry repeats a request after an infrastructure failure.

</details>

**Why exclude unlabelled tickets from accuracy?**

<details><summary>Answer</summary>

There is no known answer to compare them against.

</details>

**Does a perfect fixture score establish model quality?**

<details><summary>Answer</summary>

No. It checks parsing/scoring plumbing for scripted outputs, not model understanding.

</details>
