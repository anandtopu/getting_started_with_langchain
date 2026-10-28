# Setup and orientation: quiz

**Are tokens always words?**

<details><summary>Answer</summary>

No. A tokenizer can split words, punctuation and whitespace differently.

</details>

**Why reserve output space?**

<details><summary>Answer</summary>

Input, evidence and history consume the context budget; the answer also needs room.

</details>

**Does temperature zero prevent hallucinations?**

<details><summary>Answer</summary>

No. Sampling settings do not verify factual claims.

</details>

**Which package translates provider requests?**

<details><summary>Answer</summary>

A provider adapter; langchain-core defines the common interface.

</details>

**What does a passing offline setup check prove?**

<details><summary>Answer</summary>

The local installation and fixture interfaces work. It does not prove key validity, local model availability or answer quality.

</details>

**When is LangSmith required?**

<details><summary>Answer</summary>

It is optional throughout this course; tracing is useful but the application runs without it.

</details>
