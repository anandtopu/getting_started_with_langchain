# Agents with create_agent: quiz

**When is an agent unnecessary?**

<details><summary>Answer</summary>

When the sequence is known in advance, such as one fixed retrieval-and-answer path.

</details>

**Does a tool description grant permission?**

<details><summary>Answer</summary>

No. Application code must enforce ownership, eligibility and allowed side effects.

</details>

**Where does a structured final answer appear?**

<details><summary>Answer</summary>

At structured_response; the message trace remains separate.

</details>

**Why keep customer_id out of tool arguments?**

<details><summary>Answer</summary>

The model must not choose which authenticated customer it represents.

</details>

**Why are integer cents useful?**

<details><summary>Answer</summary>

They make the exact $100 boundary unambiguous and avoid floating-point currency comparisons.

</details>

**Why check quantity as well as an idempotency key?**

<details><summary>Answer</summary>

A caller could use a new key for the same purchased unit; the quantity check prevents another return.

</details>
