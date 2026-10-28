# Troubleshooting

## Orchestration lesson errors

| Error or symptom | Why it happens | Fix |
|---|---|---|
| `InvalidUpdateError` on a parallel field | Several nodes wrote one unreduced channel | Use a reducer for collections and merge into a scalar in one node |
| `GraphRecursionError` | A cycle did not terminate within the step ceiling | Inspect routing and enforce an attempt budget; a larger limit alone is not a fix |
| Missing configurable keys when checkpointing | No thread ID selected the persisted run | Supply the same authorized thread ID and saver when resuming |
| `Refund amount changed; start a new policy review.` | The database quote differs from the amount presented to the reviewer | Start a fresh review; do not reuse approval for a changed amount |
| A return exists but its notice is absent | The process failed between two separate commits | Resume the saved run; the idempotent outbox inserts once using the return ID |
| `Choose one to six unique categories.` | The report dispatcher received empty or duplicate work | Validate the finite plan before creating workers |
| `Virtual paths must be canonical` | A path used traversal or alternate separators | Use the exact allowlisted virtual path, never a host path |
| `Web search needs an explicit live run.` | `--web` was combined with offline configuration | Keep local search for tests, or deliberately opt into live search and its costs |
| Windows CLI help raises `UnicodeEncodeError` | The terminal encoding cannot print the upstream CLI's emoji | In PowerShell set `$env:PYTHONIOENCODING="utf-8"`, then retry |

`langgraph dev --no-browser --host 127.0.0.1` is a persistent local service; stop it with Ctrl+C. The read-only lesson graph and root configuration were exercised through the HTTP API. A Studio link printed by the CLI is not evidence that the Studio browser was tested. Use Mermaid output without an account.

Start with `uv run python scripts/check_env.py --offline`. If that succeeds, the Python installation and fake interfaces work. Run it without `--offline` to check selected keys or the local Ollama server. This does not spend tokens validating a hosted key.

| Symptom | Meaning | Fix |
|---|---|---|
| `Set OPENAI_API_KEY in .env for openai.` | The selected hosted provider has no key | Run `scripts/configure.py`, edit `.env`, or select Ollama |
| `Invalid configuration for: MODEL_TIMEOUT.` | A setting cannot be parsed or violates its bounds | Compare `.env.example`; timeout must be positive and at most 300 seconds |
| `Ollama is unavailable; start it and check OLLAMA_BASE_URL.` | No reachable server at the configured endpoint | Start Ollama and rerun the environment check |
| `An Ollama profile is not installed; pull the models in .env.` | Server is up, but a selected model is absent | Pull both the chat and embedding profiles; image models are separate |
| `The operation failed (AuthenticationError).` | The provider rejected credentials | Replace the key in `.env`; do not paste it into an issue |
| `The operation failed (RateLimitError).` | Request rate or account quota was exceeded | Inspect the provider account; reduce concurrency and use bounded retries |
| `Network disabled in offline mode; use an explicit live run.` | An offline code path tried to reach a service | Keep fixtures offline; use `--live` only when intentionally testing a real provider |
| `Writable databases must be outside committed data/.` | A write target could alter the seed corpus | Use `.runtime/orders.db` or a test temporary directory |
| `FileExistsError` when copying orders | A learner database already exists | Choose a new runtime filename; copies intentionally never overwrite |
| `attempt to write a readonly database` | Seed access is intentionally read-only | Create a writable copy for a write lesson |
| `ModuleNotFoundError` for an integration | The dependency extra or editable install is missing | Run `uv sync` with the required extra, from the checkout root |

The CLI intentionally suppresses raw SDK exception bodies because they can contain request data. Unit tests call functions directly so programming errors still show tracebacks. Record the command, package versions and exception class when filing an issue; omit keys and personal information.

## Windows paths and environments

Use the repository-root commands exactly as shown. Python uses `pathlib` for data paths, so spaces in your checkout path work. The pip fallback invokes `.venv\Scripts\python.exe` directly and does not require PowerShell activation. If your user cache is not writable, set `UV_CACHE_DIR` to a writable folder for that terminal session. This is a machine permission issue, not a reason to change provider code.

## Agent, memory and MCP errors

| Symptom | Meaning | Fix |
|---|---|---|
| `Refund over $100 requires manager approval` | The ordinary writer rejected a large refund before insertion | Use the guarded review path; model-provided approval text is not authorization |
| `Purchased quantity already has a return record` | The item has already been returned, even if the new request has another key | Inspect existing returns; never bypass the quantity check |
| `Warehouse eligibility checks have not passed` | Trusted inspection/proof fields are absent | Supply actual host-verified evidence, or explicitly simulated evidence for this course |
| Checkpointer requires configurable thread fields | A saved conversation has no address | Supply host-authorized `thread_id` through `thread_config` |
| `GraphRecursionError` | The graph ran out of steps; middleware also consumes steps | Inspect the loop and retain model/tool limits; do not treat more graph steps as a cost control |
| Reusing a scripted AIMessage corrupts a repeated loop | The state reducer merges messages by identity | Generate a fresh message and tool-call ID for each simulated model turn |
| `LangChainBetaWarning` for MCP | The verified current adapter is explicitly beta | Keep the warning and pinned integration boundary visible; do not substitute an archived adapter silently |
| MCP hangs or emits malformed messages | Protocol stdout may contain ordinary prose, or the session lifetime is wrong | Keep stdout for protocol data, await the run inside the adapter context, and use finite transport timeouts |
| `No module named fastmcp` or SQLite saver import fails | The agents extra is absent | Run commands with `uv run --extra agents ...` |

The HTTP MCP example uses actual handlers through an in-process ASGI transport. It needs no listening port and does not verify remote authentication, TLS or proxies. An interrupt similarly proves a workflow pause, not reviewer identity; authentication belongs in the application that accepts resume decisions.

## Retrieval lesson errors

| Error or symptom | Why it happens | Fix |
|---|---|---|
| `No module named langchain_chroma` or `rank_bm25` | The retrieval extra is absent, possibly removed by an ordinary uv run | Use `uv run --extra rag ...` consistently, or install with `uv sync --extra rag` and use `--no-sync` deliberately |
| `Stale index: embedding identity or corpus changed.` | Stored vectors no longer match the selected model, dimensions or corpus | Use a fresh index name and rebuild; do not edit the manifest to bypass the check |
| `Index has data without a manifest` | An earlier build stopped before its identity was recorded | Inspect the partial build and choose a new index name; old data is never deleted automatically |
| Empty extracted PDF text | The page may contain a scanned image | Inspect the page and add an OCR stage if needed; pypdf extraction is not OCR |
| `Require size > 0 and 0 <= overlap < size.` | Chunk settings cannot advance through the text | Keep overlap strictly smaller than chunk size |
| `Compression must be an exact extract from its source.` | A generated excerpt changed or invented text | Reject it; request a verbatim excerpt or retain the original evidence |
| A valid citation accompanies a wrong answer | Exact-quote validation proves provenance, not logical support | Compare every claim against the evidence; add human-reviewed semantic evaluation |

Chroma persistence is automatic with `persist_directory`; keep the collection and its manifest together. Fake embeddings demonstrate storage mechanics but cannot verify semantic similarity. A changed model requires a rebuilt index even when dimensions match. The small SQLite embedding cache similarly separates provider/model/dimension and query/document operations.

## Foundation lesson errors

| Error excerpt | Why it happens | Fix |
|---|---|---|
| `variable history should be a list of base messages` | A history placeholder received text | Supply a message list, or `[]` for no history |
| `Input to PromptTemplate is missing variables` | A required blank was omitted or literal braces were interpreted as a variable | Supply the named variable; double literal template braces |
| `Invalid json output` | Generated text was not the expected JSON | Use native structured output when supported, otherwise bounded schema repair |
| `The input to RunnablePassthrough.assign() must be a dict.` | A string reached dictionary enrichment | Pass a dictionary and inspect the previous stage's output shape |
| `Function must have a docstring if description not provided.` | A tool has no description | Add a meaningful docstring before applying `@tool` |
| `Turn budget exhausted; ask a human to review the ticket.` | The model kept requesting tools | Inspect the transcript and bounded failure; do not remove the cap |
| `'tool_call_id'` | A ToolMessage was created without its request ID | Copy the ID from the corresponding assistant tool request |

In notebooks, the event loop already exists. Use `await` for async functions instead of starting a second loop in that thread. Our mirrored script cells use `await asyncio.to_thread(main)` so scripts that create their own loop can run unchanged. The notebook fixture wrapper blocks network; run the scripts without `--offline` for real-model experiments.

For local multimodal input, pull the vision profile and check capabilities. A model that can generate text may lack vision or tool calling. Model-requested tools also need an application dispatcher: binding tool schemas alone performs no database query.

## Old tutorials and future lessons

Do not copy imports from older framework tutorials without checking the current official reference. Use the model factory and `invoke` interface shown in this checkout. Chroma persistence diagnostics and graph recursion-limit examples are available in the current tiers. The complete migration guide and release audit arrive in Phase 8.
