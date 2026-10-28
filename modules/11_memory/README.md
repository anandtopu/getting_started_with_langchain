Assistant version 7: Keep conversation state and customer preferences across sessions.

# Memory and state

**Outcome:** Keep conversation state and customer preferences across sessions.

**Time:** 150 minutes plus optional practice. **Level:** Intermediate; complete the earlier tiers first.

**Cost:** Offline fixtures cost $0 in API fees. Local models have no API fee but require hardware. Short hosted examples normally budget under $0.01; allow up to $0.10 for the full checkpoint. Model fallback, retries, summaries and tool selection can add calls. These are estimates for low-cost configured profiles, not spending guarantees. Synthetic ledger writes never send money.

## Prerequisites

Complete [Agents with create_agent](../10_agents/README.md). Commands below run from the repository root in Windows PowerShell, macOS and Linux:

```text
uv sync --locked --extra agents
uv run --extra agents python scripts/check_env.py --offline
```

Keep `--extra agents` on uv commands so optional dependencies remain installed. See the root [pip fallback](../../README.md) and [provider capabilities](../../docs/PROVIDER_CAPABILITIES.md). Omit `--offline` to use the configured real model; unsupported capabilities fail visibly. Offline mode blocks outbound networking and uses explicit scripted responses; actual local tool, database and protocol code still executes.

## Learning objectives

- Separate stateless calls, thread checkpoints and customer preference storage.
- Reopen SQLite checkpoints after the original process ends.
- Trim complete turns and summarize old history with explicit limits.
- Keep evolving task state separate from authenticated runtime context.

## The big idea

Conversation memory is a notebook assigned to one conversation. Long-term preferences are a customer filing cabinet shared across that customer's conversations. Neither is the model learning new weights. The application chooses what to save, who may read it, and how much to include in the next prompt. A summary is a shorter note written by another model call; it can omit or distort a detail, so important facts need an authoritative store.

## How it works

```mermaid
flowchart LR
    A["Authenticated customer and thread"] --> B["Load checkpoint"] --> C["Agent turn"] --> D["Save state and scoped preferences"]
```

### A thread is a storage address

A model invocation only sees the messages supplied to it. A **checkpointer** saves agent state between steps and turns. `InMemorySaver` retains it in the current process; `SqliteSaver` writes a local database. A `thread_id` selects which conversation to restore. It is an address, not a password. The host constructs it from trusted customer and conversation identifiers and must authorize access before invoking the agent. The helper's alphanumeric validation prevents ambiguous separators; it does not authenticate anyone.

Keep a `SqliteSaver.from_conn_string` context open for the whole agent operation and close it afterward. The persistence example closes the parent connection, starts a fresh Python process, and reads the checkpoint there. It uses a fixed argument list and bounded timeout; no customer text becomes executable code. SQLite suits local lessons and modest single-host applications; shared production deployment and PostgreSQL stores are introduced later.

### Keep history valid and small

**Trimming** removes older messages without another model call. A tool result must still have its matching assistant tool request. Our trim helper keeps complete recent turns, starts on a human message, ends on a human/tool boundary, retains the system instruction and disallows partial messages. It uses approximate token counts for planning, not billing. Reserve additional room for system instructions, tool schemas and model output; trimming one history list does not prove the full provider request fits.

**Summarization** makes another model call that replaces older context with a compact note. `SummarizationMiddleware` triggers at a message threshold and retains the newest messages. Inspect whether quantities, unresolved tasks, preferences and exceptions survive. The fixture's fixed summary only tests replacement and state flow. It does not establish that a real summarizer preserves every fact. Do not use summaries as an authoritative source of approvals or financial balances.

### State, context and stores

`AgentState` is a typed dictionary describing evolving graph data; the example adds an optional task note with `NotRequired`. Runtime context is a separate trusted record passed to the invocation. A model may influence a task note; it must not influence authenticated identity or database paths. The default message reducer accumulates messages by identity, which is why scripted tool loops need fresh message/call identities rather than recycling the same object indefinitely.

A **store namespace** groups records by application-defined scope, such as `("customers", "C001")`. The semantic InMemoryStore example indexes a preference's text and searches only that customer's namespace. Real embeddings may rank related meaning; fake embeddings test wiring and cannot establish semantic recall. InMemoryStore is not durable. A checkpointer stores workflow state, while a store holds records that can be reused across threads.

The [Preferences repository](../../common/memory.py) is deliberately a small application-specific SQLite table, not an implementation of LangGraph's BaseStore interface. It stores an allowlisted shipping preference under a customer key, rejects writes under committed data, and uses parameterized SQL. The application combines that durable table with SqliteSaver. It saves files in `.runtime/remembering-agent`, so re-running it preserves data. It initializes the default preference only if absent and never accepts customer identity from the model's tool arguments. Real applications additionally need retention, correction and deletion policies.

New terms are also collected in the [glossary](../../docs/GLOSSARY.md).

## Key APIs at a glance

| API or concept | Example | What to inspect |
|---|---|---|
| Stateless models; InMemorySaver; thread_id and conversation isolation | [01_stateless_threads.py](examples/01_stateless_threads.py) | A shared saver accumulates messages for one thread while another thread starts fresh. |
| SqliteSaver lifecycle; resume in a fresh process | [02_sqlite_checkpoint.py](examples/02_sqlite_checkpoint.py) | SqliteSaver writes state; a new Python process reads it after the first connection closes. |
| trim_messages; token budget; preserve matching tool-call/result pairs | [03_trim.py](examples/03_trim.py) | trim_messages keeps the current human/tool turn and excludes older complete turns. |
| SummarizationMiddleware; summarize older history without losing current task | [04_summarize.py](examples/04_summarize.py) | SummarizationMiddleware replaces older messages and retains the newest ones. |
| Custom AgentState; separate state from runtime context | [05_custom_state.py](examples/05_custom_state.py) | Custom AgentState carries task_note; SupportContext carries trusted identity. |
| Store namespaces; InMemoryStore; semantic search of preferences across threads | [06_long_term_store.py](examples/06_long_term_store.py) | InMemoryStore applies namespace scope before returning preference matches. |
| SQLite-backed preference tool for no-service persistence; preview PostgresStore in module 20 | [07_durable_preferences.py](examples/07_durable_preferences.py) | Preferences writes an allowlisted value, closes the connection and reads it through a new repository instance. |

## Walkthrough

Read each script, predict its tool/state changes, run it, then change one input. A scripted answer may stay fixed; inspect the real program behaviour around it.

### 1. Stateless threads

**Analogy:** Compare loose conversations with labelled notebooks. **Under the hood:** A shared saver accumulates messages for one thread while another thread starts fresh.

```mermaid
flowchart LR
    A["Thread ID"] --> B["Checkpoint lookup"] --> C["Isolated history"]
```

```text
uv run --extra agents python modules/11_memory/examples/01_stateless_threads.py --offline
```

**Expected:** Same-thread history grows; another thread starts fresh. Inspect [the source](examples/01_stateless_threads.py) and its `KEY IDEA` comment. Live model decisions and wording may differ.

### 2. Sqlite checkpoint

**Analogy:** Close a notebook and reopen it in another room. **Under the hood:** SqliteSaver writes state; a new Python process reads it after the first connection closes.

```mermaid
flowchart LR
    A["Agent state"] --> B["SQLite file"] --> C["Fresh process read"]
```

```text
uv run --extra agents python modules/11_memory/examples/02_sqlite_checkpoint.py --offline
```

**Expected:** A child process sees persisted messages without making a model call. Inspect [the source](examples/02_sqlite_checkpoint.py) and its `KEY IDEA` comment. Live model decisions and wording may differ.

### 3. Trim

**Analogy:** Remove old conversation pages without tearing a question from its answer. **Under the hood:** trim_messages keeps the current human/tool turn and excludes older complete turns.

```mermaid
flowchart LR
    A["Message list"] --> B["Budget and turn boundaries"] --> C["Valid recent history"]
```

```text
uv run --extra agents python modules/11_memory/examples/03_trim.py --offline
```

**Expected:** Latest complete turn remains within an approximate token budget. Inspect [the source](examples/03_trim.py) and its `KEY IDEA` comment. Live model decisions and wording may differ.

### 4. Summarize

**Analogy:** Write a shorter handover note but keep the current request intact. **Under the hood:** SummarizationMiddleware replaces older messages and retains the newest ones.

```mermaid
flowchart LR
    A["Old history"] --> B["Summary model"] --> C["Summary plus latest messages"]
```

```text
uv run --extra agents python modules/11_memory/examples/04_summarize.py --offline
```

**Expected:** A summary marker replaces older turns; the latest user request survives. Inspect [the source](examples/04_summarize.py) and its `KEY IDEA` comment. Live model decisions and wording may differ.

### 5. Custom state

**Analogy:** Keep the task checklist separate from the authenticated badge. **Under the hood:** Custom AgentState carries task_note; SupportContext carries trusted identity.

```mermaid
flowchart LR
    A["Input state and context"] --> B["Agent"] --> C["Updated task state"]
```

```text
uv run --extra agents python modules/11_memory/examples/05_custom_state.py --offline
```

**Expected:** The result retains a typed task note; identity stays in runtime context. Inspect [the source](examples/05_custom_state.py) and its `KEY IDEA` comment. Live model decisions and wording may differ.

### 6. Long term store

**Analogy:** Search only the right customer filing drawer. **Under the hood:** InMemoryStore applies namespace scope before returning preference matches.

```mermaid
flowchart LR
    A["Namespace and query"] --> B["Scoped vector search"] --> C["Preference records"]
```

```text
uv run --extra agents python modules/11_memory/examples/06_long_term_store.py --offline
```

**Expected:** Only C001 namespace results appear; fake-vector scores are not semantic evidence. Inspect [the source](examples/06_long_term_store.py) and its `KEY IDEA` comment. Live model decisions and wording may differ.

### 7. Durable preferences

**Analogy:** Store a small preference in a real database. **Under the hood:** Preferences writes an allowlisted value, closes the connection and reads it through a new repository instance.

```mermaid
flowchart LR
    A["Customer preference"] --> B["SQLite commit"] --> C["Reopened value"]
```

```text
uv run --extra agents python modules/11_memory/examples/07_durable_preferences.py --offline
```

**Expected:** C001 shipping survives reopening; C002 has no preference. Inspect [the source](examples/07_durable_preferences.py) and its `KEY IDEA` comment. Live model decisions and wording may differ.

## Real-world use case

**Sample input:** Two separate conversations ask for C001's shipping preference.

```text
uv run --extra agents python modules/11_memory/use_case/remembering_agent.py --offline
```

**Sample output:** Both receive standard from the preference tool while conversation histories remain distinct.

**Business application:** A support application can reuse a saved preference without sharing another customer's history. The runtime files survive another program run. Inspect [the application](use_case/remembering_agent.py). The source labels simulated data and decisions explicitly.

## Common mistakes

These cases are exercised in the examples, exercise checks or [agent contracts](../../tests/test_agent_contracts.py). Exception-only entries name the stable class rather than promising provider-specific wording. The CLI prints a shorter troubleshooting hint.

### Missing thread address

```text
ValueError
```

**Fix:** A checkpointed invocation needs configurable.thread_id; use the host-side thread_config helper.

### Invalid thread component

```text
ValueError: Thread components must be nonempty alphanumeric identifiers.
```

**Fix:** Use unambiguous trusted IDs; do not paste arbitrary user text into the storage key.

### Invalid preference

```text
ValueError: Choose standard or expedited for a known customer.
```

**Fix:** Validate the allowed shipping values before writing.

### Zero token budget

```text
ValueError: Token budget must be positive.
```

**Fix:** Choose a positive history budget and reserve space for the rest of the request.

## Exercises

Starters run as baseline behaviour. Complete `YOUR CODE HERE`, then use the learner-target checks before inspecting the solution.

1. **Customer thread scope.** Return a config whose thread_id combines nonempty alphanumeric customer and conversation IDs. [Starter](exercises/01_practice.py) · [Solution](solutions/01_practice.py).

2. **Whole-turn trimming.** Keep recent complete turns using approximate tokens without orphaning tool results. [Starter](exercises/02_apply.py) · [Solution](solutions/02_apply.py).

3. **Durable preference.** Write a customer preference, reopen the SQLite repository, and return only that customer value. [Starter](exercises/03_stretch.py) · [Solution](solutions/03_stretch.py).

```text
uv run --extra agents python modules/11_memory/exercises/01_practice.py --offline
uv run --extra agents pytest modules/11_memory/tests/test_exercises.py --exercise-target exercises
uv run --extra agents pytest modules/11_memory/tests
```

The middle command intentionally fails until you complete the starters. The last command checks supplied solutions, every script and the use case. The [notebook](notebook.ipynb) mirrors actual example/application source with cleared outputs. Install notebook tools with `uv sync --extra agents --group authoring`, then use `uv run --extra agents --group authoring jupyter lab`.

## Quiz

**Does a checkpointer train the model?**

<details><summary>Answer</summary>

No. It saves state that the application can restore and send in later requests.

</details>

**Is thread_id authentication?**

<details><summary>Answer</summary>

No. The host must authorize the customer and construct or validate the storage scope.

</details>

**What survives with InMemorySaver after process exit?**

<details><summary>Answer</summary>

Nothing; use durable storage when restart recovery matters.

</details>

**Why not keep a tool result after deleting its tool call?**

<details><summary>Answer</summary>

Providers expect matching call/result structure; an orphaned result is an invalid conversation.

</details>

**Can a summary prove a refund was approved?**

<details><summary>Answer</summary>

No. Preserve approval evidence in authoritative application state, not a model summary.

</details>

**How does a store differ from a checkpointer?**

<details><summary>Answer</summary>

A checkpointer saves workflow/thread state; a store holds scoped records reusable across conversations.

</details>

## Key takeaways

- Separate stateless calls, thread checkpoints and customer preference storage.
- Reopen SQLite checkpoints after the original process ends.
- Trim complete turns and summarize old history with explicit limits.
- Keep evolving task state separate from authenticated runtime context.
- Keep scripted control tests distinct from live model quality and deployment guarantees.

## Go deeper

- [Official short-term-memory reference](https://docs.langchain.com/oss/python/langchain/short-term-memory)
- [Official built-in reference](https://docs.langchain.com/oss/python/langchain/middleware/built-in)
- [Official long-term-memory reference](https://docs.langchain.com/oss/python/langchain/long-term-memory)
- [Verified versions, substitutions and limits](../../docs/VERIFICATION_NOTES.md)

## Next: Middleware and guardrails

Continue to [Middleware and guardrails](../12_middleware/README.md). Re-run shared contract tests if you change the helper code.
