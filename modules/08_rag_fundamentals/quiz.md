# RAG fundamentals: quiz

**Does indexing train the chat model?**

<details><summary>Answer</summary>

No. It prepares searchable evidence that is supplied at request time.

</details>

**Where should source/page values come from?**

<details><summary>Answer</summary>

Application-controlled metadata of the retrieved Documents, not model-invented values.

</details>

**What can an exact-quote check prove?**

<details><summary>Answer</summary>

That the quote occurs in retrieved evidence. It cannot prove every answer claim is supported.

</details>

**Should evaluation answers be included in the index?**

<details><summary>Answer</summary>

No. Keep labels outside retrieval and generation, using them only in scoring.

</details>

**Why inspect retrieval before changing the prompt?**

<details><summary>Answer</summary>

Generation cannot reliably recover a missing fact that was never retrieved.

</details>

**When is the fixed chain easier to debug?**

<details><summary>Answer</summary>

When every question needs retrieval: fixed steps make the evidence and number of calls predictable.

</details>
