# Embeddings, vector stores and retrievers: quiz

**What does embedding dimension mean?**

<details><summary>Answer</summary>

The number of coordinates in each vector, not the number of documents.

</details>

**Can two 768-dimensional models share an index?**

<details><summary>Answer</summary>

Not safely: their coordinate spaces may be unrelated even though the lengths match.

</details>

**Is a cosine distance of 0.2 an 80% correctness probability?**

<details><summary>Answer</summary>

No. It is a geometric distance in that store's space.

</details>

**Why filter before ranking products?**

<details><summary>Answer</summary>

Similarity does not enforce business constraints such as exact capacity or a strict price ceiling.

</details>

**What does MMR trade off?**

<details><summary>Answer</summary>

Relevance to the query and redundancy relative to already selected documents.

</details>

**Why separate query and document cache keys?**

<details><summary>Answer</summary>

Some embedding models encode the two roles differently; identical text need not produce the same vector.

</details>
