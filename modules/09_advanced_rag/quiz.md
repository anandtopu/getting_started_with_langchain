# Advanced RAG and evaluation: quiz

**Why retain the original query?**

<details><summary>Answer</summary>

A rewrite may drop or distort a constraint; the original provides another retrieval path.

</details>

**Why not add a BM25 score to a cosine distance?**

<details><summary>Answer</summary>

They use incompatible scales and opposite conventions; RRF combines ranked positions instead.

</details>

**Does exact compression guarantee no loss of meaning?**

<details><summary>Answer</summary>

No. Removing context can drop exceptions or change the interpretation of a copied sentence.

</details>

**What is the cost of parent retrieval?**

<details><summary>Answer</summary>

More context tokens and possible noise, traded for restored surrounding evidence.

</details>

**Should unknown questions enter the source-hit denominator?**

<details><summary>Answer</summary>

No source is expected for them. Evaluate abstention separately.

</details>

**What if the candidate has the same quality score?**

<details><summary>Answer</summary>

Report the tie, other measured tradeoffs and per-case failures. Do not claim an accuracy improvement.

</details>
