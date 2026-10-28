# Quiz


1. Is unknown token usage free?

<details>
<summary>Answer</summary>

No. Treat it as unknown and conservatively refuse further cost authorization.

</details>

2. Should private replies use the public global cache?

<details>
<summary>Answer</summary>

No. Scope caches by verified identity and lifecycle.

</details>

3. Does a system prompt stop all injection?

<details>
<summary>Answer</summary>

No. Permissions and validation must be enforced in host code.

</details>

4. Does a Postgres namespace authenticate its owner?

<details>
<summary>Answer</summary>

No. The host must authorize access to that namespace.

</details>

5. Does this API automatically use Postgres?

<details>
<summary>Answer</summary>

No. It uses SQLite; the Postgres probe is a separate integration example.

</details>

6. Why does a healthy container and passing offline gate not prove customer readiness?

<details>
<summary>Answer</summary>

Engineering and scripted quality contracts pass; live-model behavior and customer readiness remain unverified.

</details>
