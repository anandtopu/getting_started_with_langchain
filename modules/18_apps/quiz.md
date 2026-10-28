# Quiz


1. Does async def make blocking code concurrent?

<details>
<summary>Answer</summary>

No. It needs an actual await point or worker offloading.

</details>

2. Can the chat payload choose customer_id?

<details>
<summary>Answer</summary>

No. Extra fields are rejected; identity comes from the host.

</details>

3. Does a step event mean the request is complete?

<details>
<summary>Answer</summary>

No. Only done confirms completed chat history was saved.

</details>

4. Why buffer tokens before redacting?

<details>
<summary>Answer</summary>

Sensitive patterns can span chunks; full-line buffering protects the narrow patterns at some latency cost.

</details>

5. Can approval override absent inspection?

<details>
<summary>Answer</summary>

No. Trusted facts are rechecked before the write.

</details>

6. Does reset delete earlier conversations?

<details>
<summary>Answer</summary>

No. It changes the active thread; deletion is a separate policy.

</details>
