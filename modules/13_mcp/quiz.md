# Model Context Protocol: quiz

**Does MCP make a server trustworthy?**

<details><summary>Answer</summary>

No. Protocol compatibility says nothing about permission, accuracy or side effects.

</details>

**Why keep stdout clean in a stdio server?**

<details><summary>Answer</summary>

It carries protocol messages; ordinary diagnostic text can corrupt communication.

</details>

**What does the in-process HTTP test verify?**

<details><summary>Answer</summary>

Actual HTTP/MCP handler behaviour and lifecycle, not deployed network security or availability.

</details>

**Can the model choose a subprocess command here?**

<details><summary>Answer</summary>

No. The executable and script arguments are fixed by reviewed application code.

</details>

**Why validate the returned SKU?**

<details><summary>Answer</summary>

A well-shaped response for another product must not be treated as the requested evidence.

</details>

**Why await the agent inside the adapter context?**

<details><summary>Answer</summary>

Its tool calls need the live session, and the context guarantees cleanup when the operation ends.

</details>
