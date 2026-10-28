# Document loaders and text splitters: quiz

**Does a Document automatically know its PDF page?**

<details><summary>Answer</summary>

No. The loader must supply the page in metadata; splitting must preserve it.

</details>

**Why keep parent_id?**

<details><summary>Answer</summary>

It links a small searchable child back to the original page or section for context expansion.

</details>

**Does lazy_load prove constant-memory PDF processing?**

<details><summary>Answer</summary>

No. It yields incrementally, but PdfReader may retain the PDF structure internally.

</details>

**Does a 450-character chunk contain 450 model tokens?**

<details><summary>Answer</summary>

No. Token counts depend on the tokenizer and text.

</details>

**Why keep gold evaluation files out of ingestion?**

<details><summary>Answer</summary>

Otherwise the index could retrieve the answer key and make evaluation misleading.

</details>

**Does removing HTML comments prevent every injection?**

<details><summary>Answer</summary>

No. Malicious instructions can be visible text too; application permissions must remain separate.

</details>
