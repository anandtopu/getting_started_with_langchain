# Verification notes

## Policy-answer correction (2026-10-28)

The former two support misses are fixed in common/rag.py: small grammatical normalization matches return/returned and take/takes; duration questions require a numeric time unit in relevant evidence. The live prompt also distinguishes the requested timeline from fees or unrelated services. The prompt change is not a measured live-model improvement. No evaluation labels, policy numbers or thresholds changed. Six support contracts and all 19 capstone contracts now pass; both strict release commands succeed offline. Changed-number/paraphrase and missing-evidence tests prevent hard-coded success. Missing facts and denied ownership still block the gate.

The shared RAG benchmark was regenerated: retrieval hit rate and keyword correctness remain unchanged (5/7 and 5/8 for each configuration). A duration question lacking retrieved timing evidence now abstains instead of quoting unrelated text. Older phase sections below retain their original results as historical evidence; they do not describe the corrected release.

Follow-up verification: 629 tests passed (two explicit live skips), all 141 smoke targets and all 21 notebooks passed. Both strict release commands returned success; the rebuilt non-root container returned the corrected 30-day answer through authenticated SSE and persisted its policy tool trace. Ruff, formatting, legacy scan, strict inventory and local links passed. The full CI workflow now requires both strict release commands rather than merely completing an evaluation.


## Phase 8 - final capstones and repository audit (2026-10-28)

All 43 PyPI package records were refreshed before the capstone implementation; verified stable versions remain unchanged. The project version is 1.0.0. [Machine-readable evidence](phase8-verification.json) records results; [the completion checklist](DEFINITION_OF_DONE.md) keeps outstanding evidence visible.

Official API references checked include [SQL agents](https://docs.langchain.com/oss/python/langchain/sql-agent), [MCPAdapter and its beta status](https://docs.langchain.com/oss/python/langchain/mcp), [workflow patterns](https://docs.langchain.com/oss/python/langgraph/workflows-agents), [Streamlit PDF uploads](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader) and [v1 migration](https://docs.langchain.com/oss/python/migrate/langchain-v1). Installed signatures and executable tests confirm SDK server methods, adapter discovery, file_uploader max_upload_size and graph Send/reducers. Tests use the current MCP SDK input_schema field, avoiding its deprecated alias.

The five capstones exercise actual PDF extraction/retrieval/UI, authenticated HTTP chat and refund review, engine-authorized SQL repair/charting, planner/researcher/writer/critic orchestration, and two real MCP servers. The 19-case suite passes 17 complete contracts; the same two policy relevance misses remain visible in the flagship's actual HTTP path. Its five-call reservation covers three outer calls plus two policy tool calls with one model call each, with SDK retries disabled. A dedicated test checks this nested path. Other capstone logical-call limits do not include provider retry attempts.

The final review fixed raw Personal Ops tracing and added strict discovered MCP field checks. PDF limits do not isolate a malicious parser; private document consent and session-local indexes do not constitute a public identity system. SQL analytics are staff-only, while the customer copilot's SQL remains owner scoped. No model can issue its own approval receipt. See the [per-file report](reviews/phase8-per-file.md), [integration report](reviews/phase8-integration.md) and [action plan](reviews/phase8-action-plan.md).

Five one-page cheatsheets were generated with deterministic PDF metadata, rendered with Poppler and visually inspected for clipping and readability. Their Markdown companions remain editable. The legacy guide is the only deliberate old-API comparison surface. Full and minimal checks, all notebook executions, container evidence and publication outcomes are recorded in the final checklist rather than inferred from implementation.


## Phase 7 — apps, evaluation and production (2026-10-28)

Refreshed all 43 package records on PyPI before implementation; stable versions match Phase 6. Project version advances to 0.7.0 without dependency upgrades. [Machine-readable evidence](phase7-verification.json) records actual results and explicitly untested paths.

Official sources and installed signatures checked: [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/), [Streamlit chat](https://docs.streamlit.io/develop/api-reference/chat), [AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest), [LangSmith evaluate](https://docs.langchain.com/langsmith/evaluate-llm-application), [tracing](https://docs.langchain.com/langsmith/observability-quickstart), [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence), [streaming](https://docs.langchain.com/oss/python/langchain/streaming), [uv Docker](https://docs.astral.sh/uv/guides/integration/docker/) and [current deployment naming](https://docs.langchain.com/langsmith/deployment). The globals API-reference page failed in the web reader; current installed `get_llm_cache`, `set_llm_cache`, `InMemoryCache` and `InMemoryRateLimiter` signatures were inspected and executable examples tested instead. No unconfirmed import was substituted from a tutorial.

### Implementation adjustments discovered by execution

The installed GenericFakeChatModel's stream implementation does not retain modern empty-content `AIMessage.tool_calls`. The common scripted subclass now emits real AIMessageChunk tool_call_chunks, tested in synchronous and asynchronous streams; ordinary replies retain the upstream implementation. This is a visible fixture adapter, not a production model implementation. The UI stream filters ToolMessage bodies so internal SQL payloads are not rendered as assistant text.

Direct standalone ToolNode invocation in this pinned release requires runtime config supplied by a graph. The injection lesson therefore executes ToolNode inside a real compiled MessagesState graph. It deliberately assumes a compromised model and proves that an unregistered export tool is denied; no model injection resistance is claimed.

The real LangSmith evaluate runner passes with in-memory Examples and `upload_results=False` under network denial. The SDK labels this flag beta and emits upstream AST deprecation warnings on Python 3.12. Cloud dataset creation uses verified Client.create_dataset/create_examples signatures and is guarded by an explicit cloud argument plus live credentials; that service path was not executed. The optional structured judge fixture explicitly says no semantic assessment occurred.

### Environment and tooling corrections

Direct execution revealed that the generic Jupyter dispatcher selected an unrelated system installation on this Windows host. The notebook checker now invokes nbconvert with the current Python and writes a temporary kernel spec naming that exact interpreter. All 21 notebooks then passed against the locked environment. The legacy scanner now recognizes only an explicitly imported current Streamlit AppTest runner; ordinary model legacy invocations remain prohibited and regression-tested. Cost notes count up to 30 logical calls for six live cases (three agent calls plus two nested retrieval calls per case); provider retries can add attempts.

### Application contracts

Tests exercise actual FastAPI handlers and Streamlit AppTest controls: credential prompts, chat, reset, identity changes, approve and reject. Ownership is enforced server-side; customer fields cannot be injected into requests; stale or duplicate interrupt IDs fail. Trusted warehouse changes and changed refund quotes are rejected after review without a write. A direct ASGI disconnect test closes the source and releases admission; timeouts and failures expose only a generic SSE error and safe correlation ID. Modern tool-call streaming and no-tool-body leakage have regression tests.

Calls are conservatively reserved in SQLite before each chat and survive process reopen. Concurrent reservations cannot exceed the ceiling. Admission is explicitly one-process-only; the image uses one worker. Input/history limits and model/tool call limits are separate from the illustrative post-call dollar accounting, which treats unknown usage as unknown. Public-only SQL uses a read-only connection, authorizer, instruction limit and output cap. Configured secrets, synthetic emails and card-like patterns are scrubbed before local storage/log export; this narrow filter is not general DLP.

### Container and database evidence

Built the locked image and ran it as UID 10001 with read-only source and writable disposable runtime. Actual health, authenticated thread creation and SSE completion passed. The local Podman 6.0.2 Docker-compatible engine's bridge networking failed with netavark/nftables; the successful check used the explicit context, direct builder and host networking limited to VM loopback. Normal bridge networking is not claimed verified on this host. The inspection records the image ID. No registry push occurred.

A separate PostgreSQL 16-alpine container passed PostgresSaver checkpoint recovery after reconnect, PostgresStore recovery after reconnect and namespace isolation. Probe credentials were generated in memory, never logged; containers were stopped in finally blocks. The installed checkpoint/store packages were used directly. The FastAPI app remains SQLite; the probe does not imply that the entire application has migrated to Postgres or supports horizontal scaling.

### Quality and release semantics

The independent six-case support set yields 4/6 complete offline contracts. All tool-trajectory and ownership contracts pass. Returns and shipping fail keyword correctness despite literal citation support, demonstrating that faithful quotation alone does not answer the question. The answer-producing function receives no expected labels; a regression test changes labels without changing answers. Both prompt versions receive identical fixture scores, so no prompt-quality improvement is claimed.

The default strict quality gate is false. Tone and applicable exact-evidence support are mandatory alongside correctness, ownership and tool trajectories; regressions in either independently block release. The checkpoint's ordinary rehearsal can pass engineering checks while reporting this block; `--release` exits nonzero, and CI tests that exit code. [The saved report](../checkpoints/05_production_release/evaluation_report.json) retains failures. Hosted models, Ollama inference, cloud LangSmith, Studio browser, public app deployment, payment/email services and remote CI remain unverified. Final checks: 558 tests passed, two opted-in live tests skipped; all 141 smoke targets and 21 notebooks passed. Minimal install: 230 tests passed with 305 explicit skips, 38 smoke targets passed with 103 missing-extra skips. All nine runnable exercise baselines intentionally fail their completion targets. Ruff, legacy scan and coverage passed. Internal and external links had zero failures; five future-capstone links remain deferred. No remote CI run is claimed.



## Phase 6 execution record — 2026-10-28

Modules **14–17** add 28 examples, four applications, twelve exercise starters and solutions, four quizzes and four notebooks. **Operations Desk** adds eight contract cases, a committed evaluation report, a graph export and a written design rationale. Eighteen modules and four checkpoints are implemented; three modules and the capstones remain planned.

### Versions and API checks

The [43-package refresh](phase6-verification.json) found no release changes from Phase 5. Core versions remain LangChain 1.4.7, LangGraph 1.2.18 and Deep Agents 0.7.32. The latter is pre-1.0 and stays optional. Package version 0.6.0 identifies this course phase. The lockfile remains the reproducible installation reference.

Official references checked: [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api), [persistence](https://docs.langchain.com/oss/python/langgraph/persistence), [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts), [Functional API](https://docs.langchain.com/oss/python/langgraph/functional-api), [workflow patterns](https://docs.langchain.com/oss/python/langgraph/workflows-agents), [multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent), [Deep Agents customization](https://docs.langchain.com/oss/python/deepagents/customization), [backends](https://docs.langchain.com/oss/python/deepagents/backends), [local development](https://docs.langchain.com/langsmith/local-dev-testing) and [Tavily](https://docs.langchain.com/oss/python/integrations/tools/tavily_search).

Installed signatures and executable examples verified StateGraph schemas and routing, reducers, ToolNode, runtime context, Command, Send, interrupt, SQLite saving, history/forks, subgraphs, all four requested stream modes, get_stream_writer, entrypoint/task and sync/async execution. The manual agent uses the current ToolNode with the central model factory. The deliberately broken parallel example reproduces InvalidUpdateError; the repaired graph uses a list reducer. A bounded loop reproduces GraphRecursionError.

The optional SDK example executes planning, task delegation and virtual writing through actual create_deep_agent tools. It explicitly supplies StateBackend, TodoListMiddleware, a bounded researcher and a bounded general-purpose child; no provider default or shell backend is selected. Models are still created through common.models. The SDK's state files do not have the same narrow path allowlist as the separate manual VirtualFiles helper. Neither demonstration grants host filesystem tools.

TavilySearch construction was checked with its installed API wrapper and a synthetic key. A mocked response verifies opt-in dispatch, result limits and URL provenance without contacting Tavily. The wrapper import is isolated in common/research.py because the provider package exposes it under `_utilities`; that internal path may require adjustment on a future upgrade. Real search, real model decisions and Studio browser behavior remain unverified.

### Local server and recovery evidence

The current `langgraph dev` command was verified from its help. The root langgraph.json registers a read-only, model-free graph. A temporary loopback server passed `/ok`, exposed `/runs/wait` in its OpenAPI schema, and returned `Review required` for an actual HTTP graph invocation. The process and its children were stopped afterward. No browser or public tunnel was opened. Installed server components were langgraph-api 0.16.8 and langgraph-runtime-inmem 0.36.8. The stateless request emitted the upstream warning that durability has no effect without a checkpointer; durable SQLite behavior is tested separately. Windows CLI help needed UTF-8 output to print its upstream emoji.

Return inspection is now shared between a read-only preflight and the transactional writer. Tests verify no preapproval write, rejection with no write, resumed eligibility changes, changed-amount rejection, ownership, idempotency and one outbox row per return. An injected failure after the return commit leaves one return and zero notices; resuming repairs it to one of each. This is recoverable at-least-once work across separate transactions, not an atomic distributed transaction or evidence of email delivery. The local outbox rechecks ownership and reads the recorded refund amount itself.

Report tests verify all 300 reviews across six categories, deterministic aggregation, a two-attempt ceiling, rejection of duplicate/unknown work and prevention of negative initial counters. The normal fixture uses ten logical model calls; an exhausted single-attempt run remains unaccepted. These are structural and budget checks, not factuality scores. Specialist tests preserve SQL denials, validate public product citations, restrict role labels and project minimum inputs. Virtual-file tests reject traversal, source overwrites, oversized writes and unknown citations. The [Operations Desk report](../checkpoints/04_operations_desk/evaluation_report.json) records 8/8 scripted routing/access cases; no live routing-accuracy claim is made.

### Execution results and limits

The first full run passed 468 tests with one opt-in live skip and the expected MCP beta warning. All 18 notebooks and 121 standalone targets passed. The expanded reducer demonstration initially exposed a schema conflict: its typed nodes contributed their reduced schema to the intentionally unreduced graph. Explicit input_schema=Unreduced fixes that demonstration; it now produces the intended InvalidUpdateError and then runs the repaired graph. The changed graph notebook and both expanded standalone examples were re-executed successfully. Final suite counts and basic-installation results are recorded in [Phase 6 metadata](phase6-verification.json).

The final full suite passed **469 tests**, with one opt-in live skip and the expected MCP beta warning.

The basic `uv sync --locked` environment passed 216 tests, with 249 explicit optional-extra/live skips. Its standalone run passed 38/38 targets and skipped 83 missing-extra examples. The full environment was then restored. Notebook execution preserved cleared committed outputs; the upstream local-kernel transport warning remains visible rather than suppressed.

All 56 teaching scripts have typed functions and are at most 96 lines. Twelve runnable exercise baselines intentionally fail their twelve target checks until completed; the supplied solutions pass. Local lint, format, legacy and coverage checks pass. Seventy links still point to explicitly planned future files. Actual hosted/Ollama quality, real Tavily search, Studio browser, production host authentication and remote cross-platform CI remain unverified.

## Phase 5 execution record — 2026-10-28

Modules **10–13** and **Guarded Support** add 28 examples, four applications plus an inventory server, 12 exercise starters and solutions, four quizzes and four notebooks. Fourteen modules and three checkpoints are now implemented. Windows/Python 3.12 checks remain local; actual hosted/Ollama model decisions and remote CI are not claimed.

| Local check | Result |
|---|---|
| Full agents/authoring installation | 366 tests passed; one opt-in live test skipped |
| Basic `uv sync` installation | 195 tests passed; 167 optional-extra/live checks skipped |
| Standalone examples | Full: 93/93 passed; basic: 38/38 passed, 55 optional-extra skips |
| Executed notebooks | 14/14 passed, including the repaired MCP notebook |
| Ruff lint and formatting | Passed; 369 Python/notebook files formatted |
| Legacy API and feature checks | Zero violations; seven future modules remain deferred |
| Local and external links | Zero failures; 160 explicitly planned links deferred |

The 57 new teaching scripts have typed functions and are at most 84 lines each. Supporting shared modules and tests are longer where the control logic requires it.

The initial 42-package refresh found **pypdf 6.21.4**, replacing 6.21.3 in the lower bound and lock. The current MCP stack uses `httpx2`; its **2.16.0** release was checked separately and added as an explicit agents-extra dependency because the HTTP example imports it directly. Other top-level versions remain unchanged. See the [43-package record](phase5-verification.json), installed ranges and lockfile.

### Current agent and memory interfaces

Official references checked: [agents](https://docs.langchain.com/oss/python/langchain/agents), [structured output](https://docs.langchain.com/oss/python/langchain/structured-output), [short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory), [long-term memory](https://docs.langchain.com/oss/python/langchain/long-term-memory), [custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom) and [built-in middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in). Installed signatures and real offline execution verified create_agent, ToolStrategy/ProviderStrategy, context_schema/ToolRuntime, AgentState, message trimming, InMemorySaver/SqliteSaver, InMemoryStore and every middleware named in the feature map.

The fake native-schema example parses an explicitly supplied JSON response through the actual agent parser; it does not emulate provider-side enforcement. Tool selection, planning and summaries likewise use declared fixtures. The durable preference repository is an application-specific SQLite table, not an implementation of LangGraph BaseStore. The remembering application persists under `.runtime/remembering-agent`; checkpoint reopening is also checked in a fresh Python process.

The tested guard factory combines input bounds, email/card-fixture redaction, human review, fallback and logical model/tool limits. Both model instances use the same configured profile for portability, so fallback proves control flow rather than independent-provider availability. Fallback and SDK retries can add physical calls beyond the logical model counter. Middleware adds graph steps; the host's 60-step backstop is intentionally separate from the five-model/six-tool limits. The repeated-message demonstration now creates fresh message/call identities because reusing the same AIMessage object caused reducer/routing errors during implementation.

### MCP verification and substitution

The [current MCP guide](https://docs.langchain.com/oss/python/langchain/mcp) documents `langchain.mcp.MCPAdapter` and `list_tools`; the namespace remains beta and its warning is preserved. The [official Python SDK](https://github.com/modelcontextprotocol/python-sdk) 2.3.0 supplies `mcp.server.mcpserver.MCPServer`, including typed tool registration and asynchronous stdio/HTTP serving. The separate FastMCP 4.1.4 client transport accepts this high-level official server; attempting to infer transport directly from the low-level Server failed, so the lesson uses the verified high-level class. No retired adapter package was installed.

Real protocol handshake, discovery and calls passed over in-process memory, managed stdio subprocesses, and Streamable HTTP through the SDK's ASGI app and `httpx2.ASGITransport`. HTTP is exercised without a listening socket; this is not evidence of deployed authentication, TLS or proxy behaviour. Client endpoints, tool names, request fields, response bounds and returned SKU are checked. Descriptions and read-only annotations are not treated as permission grants.

The first MCP notebook run exposed Jupyter stderr's missing file descriptor. The adapter now gives the child a real managed temporary diagnostic file. A regression test replaces stderr with a stream lacking fileno, and the affected notebook was re-executed successfully. All other notebooks passed on the initial run; the 14th passed after this repair. The Windows notebook runtime also emits its upstream event-loop/kernel-transport notices; these are not silently suppressed or presented as a remote deployment check.

### Measured controls and remaining limits

The [eight-case report](../checkpoints/03_guarded_support/evaluation_report.json) records ordinary success, approved/rejected high-value requests, wrong-customer denial, repeated requests, missing warehouse checks, hostile approval text and ordinary-writer bypass attempts. Its model trajectories and reviewer decisions are explicitly scripted. It measures controls and write counts, not autonomous-agent accuracy or general injection resistance.

Tests also verify exact 10,000-cent boundaries, concurrent retries, key/payload conflicts, already-returned quantity, source-database protection, trusted exception verification, hidden context fields, invalid review decisions and reopening a paused SQLite workflow. Eligibility runs again after approval. These are synthetic ledger records; no payment API or manager-authentication UI is implemented. Final execution counts, basic-installation skips and link checks are in [Phase 5 metadata](phase5-verification.json). Seven modules and later projects remain planned.

## Phase 4 execution record — 2026-10-28

Modules **06–09** and **Handbook Q&A** add 27 examples, four applications, 12 runnable exercise starters and solutions, four quizzes and four notebooks. The implemented course now contains ten modules and two checkpoints. Local validation uses Windows and Python 3.12; remote CI and actual hosted/Ollama generation remain unverified.

The 42-package PyPI refresh found the same latest versions as the Phase 3 refresh. The [Phase 4 record](phase4-verification.json) records those versions, source URLs, inspected interfaces and final checks. The lock resolves 286 packages across all optional groups. The installed retrieval tier uses langchain 1.4.7, langchain-core 1.7.1, langchain-text-splitters 1.1.3, langchain-chroma 1.1.0 and pypdf 6.21.3.

| Check | Result |
|---|---|
| Retrieval plus authoring installation | 268 passed, one opt-in live test skipped. |
| Minimal locked installation | 179 passed, 85 explicit skips for missing retrieval/PDF dependencies and the live test. The checkpoint module skips during collection, so collected test totals differ by installation. |
| Standalone smoke | Retrieval installation: 65/65 passed. Minimal installation: 38/38 passed, 27 missing-extra skips. |
| Notebooks | 10/10 execute offline; source hashes and cleared outputs checked. |
| Lint and format | Both pass across 278 Python/notebook files. |
| Legacy scan and coverage | Zero violations; ten implemented modules, eleven future modules. |
| Local and external links | Zero failures; 249 references explicitly deferred to planned files. |
| Teaching scope | All 55 new example/application/exercise/solution scripts have typed functions and run; longest is 53 lines. |

### Loader substitution and API verification

The upstream [community sunset notice](https://github.com/langchain-ai/langchain-community/issues/674) states that the package was sunset in May 2026 and the repository archived in June. The Phase 1 loader proposal is therefore superseded: remove `langchain-community` from the retrieval extra and use `langchain_core.document_loaders.BaseLoader` with small visible pypdf/standard-library adapters. The lock consequently drops its retired chain dependency too. Learners still practice `load`, `lazy_load`, PDF pages, CSV/JSON records, text/Markdown and explicit directory ingestion. No broad directory sweep imports evaluation answers or poisoned fixtures.

Official sources checked: [document loaders](https://docs.langchain.com/oss/python/integrations/document_loaders), [splitters](https://docs.langchain.com/oss/python/integrations/splitters), [embeddings](https://docs.langchain.com/oss/python/integrations/embeddings/), [Chroma](https://docs.langchain.com/oss/python/integrations/vectorstores/chroma), [retrieval](https://docs.langchain.com/oss/python/langchain/retrieval), and [evaluation](https://docs.langchain.com/langsmith/evaluate-llm-application). The retrieval URL currently redirects to a Deep Agents retrieval page; using that general explanation does not add a Deep Agents dependency. Specific old PDF integration links returned 404, so guides link to the current loader overview and implementation instead.

Installed signatures and runtime behaviour were checked for Document, BaseLoader, RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter, TokenTextSplitter, Tokenizer/split_text_on_tokens, language-aware splitting, InMemoryVectorStore, Chroma persistence/update/delete/filter/MMR, Embeddings, and BM25Okapi. Current Chroma persistence is automatic. Embedding models always come from the central factory, with explicit telemetry-disabled local Chroma settings; no default embedding download is used. The offline token example uses an explicitly labelled ASCII byte fixture because a real tokenizer may download its vocabulary on first use.

### Measured evidence and boundaries

The committed [before/after report](../modules/09_advanced_rag/results/README.md) reproduces exactly under an offline test. The candidate reduces chunks from **138 to 44 (68.1%)**, while source/page hit rate remains **5/7** and the keyword correctness proxy remains **5/8**. Exact-extract support is 1.0 for non-abstained answers, which merely reflects copying source text. This is neither a live-model score nor proof of relevance or entailment. The eight-case set is developer-visible, not blind; labels are excluded from indexing and generation. Live mode uses actual vector ranking and generation and constitutes a separate experiment.

The checkpoint's [six-case report](../checkpoints/02_handbook_qa/evaluation_report.json) records five expected-page retrieval hits and an unknown-fact abstention. Approval appears on more than one handbook page: page 8 is retrieved, while a valid quote may come from page 2. Citation validation derives page/source from retrieved metadata and checks exact quoted text. It cannot establish that every answer claim follows from that quote.

Tests cover provenance-sensitive identities, chunk bounds, cache reopen/hits and query/document namespaces, incompatible embedding/corpus manifests, product eligibility, invalid citations, invented compression, parent lookup and evaluation denominators. Default tests and smoke runs block network; missing retrieval extras are explicitly skipped in a basic installation. Notebooks mirror actual scripts and keep committed outputs cleared. Both generated teaching plots were visually inspected. Final executed counts are recorded in [Phase 4 metadata](phase4-verification.json).

No paid model calls, public deployment or remote CI runs were performed. Eleven modules, later checkpoints and capstones remain planned. The final-release link and coverage gates intentionally remain incomplete until those phases are built.

## Phase 3 execution record — 2026-10-28

Modules **00–05** and **Smart Ticket Desk** are implemented. Local checks used **Windows / CPython 3.12.13 / uv 0.12.18**. The tier contains 36 examples (longest: 95 lines), six applications, 18 runnable exercise starters and solutions, six quizzes and six notebooks. Future tiers remain deferred.

| Check | Result |
|---|---|
| Refresh 42 PyPI packages | Complete; [metadata](phase3-verification.json). Langchain-core advanced to **1.7.1**; lower bound/lock updated. Pydantic-settings 2.16.2 was already adopted in Phase 2. |
| Minimal `uv sync --locked` then pytest | **179 passed, 3 skipped**: two optional PDF/authoring checks and the opt-in live test. |
| Authoring install and pytest | **181 passed, 1 skipped**: only the live test. |
| Standalone smoke | **38/38 targets passed**: 36 lessons plus setup/first-call scripts. The updated HTTP lesson was additionally checked with both provider mock formats and its notebook. |
| Notebooks | **6/6 executed top to bottom**; chat notebook re-executed after the HTTP update. Committed outputs/execution counts remain empty. Tests verify source-hash and body parity for every example/use case. |
| Lint/format | Both pass, including notebooks. Notebook-only exceptions permit repeated imports/main definitions and imports after setup cells; script source is linted independently. |
| Legacy scan/coverage | Zero violations; six complete implemented modules, 15 deferred. Strict final-release coverage remains incomplete. |
| Local/external links | Zero failures; **335 explicitly planned references** remain deferred. |
| Exercises | All 18 baselines and 18 solutions run offline; default target checks validate solutions. `--exercise-target exercises` checks learner edits and deliberately fails on incomplete baselines. |
| Checkpoint | Six acceptance cases check IDs, missing orders/identifiers, ownership denial, hostile text with scoped reads, unsent drafts and unchanged seed DB. |
| Failure behavior | Schema repair exhaustion, invalid arguments, unknown tools, turn/call limits, actual review-pipeline fallback after a synthetic timeout, and offline suppression of ambient tracing. |
| Dataset | Deterministic SVG/PNG tent diagrams added; 21 generated files now have checksums. Count/integrity and fresh-build repeatability checks pass. |

### Phase 3 API checks and choices

Installed signatures were checked for prompt classes, message placeholders, few-shot templates, sequences, parallel/branch/passthrough/lambda runnables, `chain`, retries/fallbacks, `astream_events`, output parsers, `InMemoryRateLimiter`, `tool`, and `ToolRuntime`. Tests construct both `json_schema` and `function_calling` bindings for all four real provider adapters with networking denied. Construction verifies local imports/arguments, not remote capabilities.

Official references checked: [models](https://docs.langchain.com/oss/python/langchain/models), [messages](https://docs.langchain.com/oss/python/langchain/messages), [tools/runtime](https://docs.langchain.com/oss/python/langchain/tools), [structured output](https://docs.langchain.com/oss/python/langchain/structured-output), [prompts](https://reference.langchain.com/python/langchain_core/prompts/), [runnables](https://reference.langchain.com/python/langchain_core/runnables/), [parsers](https://reference.langchain.com/python/langchain_core/output_parsers/), and [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/). API reference Markdown that the browser extractor could not display was fetched directly and compared with installed signatures.

The HTTP exercise implements OpenAI Responses and Ollama chat with explicit status checks and different response-envelope parsing. It uses mocked transport offline. Sources: [OpenAI text generation](https://developers.openai.com/api/docs/guides/text), [reasoning/output limits](https://developers.openai.com/api/docs/guides/reasoning), [Ollama chat](https://docs.ollama.com/api/chat), [Ollama model-information API](https://github.com/ollama/ollama/blob/main/docs/api.md), and [HTTPX transports](https://www.python-httpx.org/advanced/transports/). Anthropic/Gemini users select OpenAI or Ollama for this one wire-protocol comparison; remaining model lessons use the central factory.

`GenericFakeChatModel` lacks tool binding. `ScriptedChatModel` subclasses it to record schemas and consume explicit `AIMessage` fixtures. LangChain's inherited tool-output parser performs actual local validation. This fake neither chooses tools nor enforces provider-native JSON constraints; both output-method demos use the tool parser offline. Guides and metric labels explicitly distinguish fixture plumbing from model quality.

The runtime example supplies `ToolRuntime` through a small injection harness; its public schema excludes that argument. Full agent-managed injection belongs to module 10. Order tools use trusted closure identity, parameterized SQL and read-only connections. Fallback selects the configured low-cost profile and is cheaper only if the primary is a more expensive override; it does not solve provider-wide outages. The synthetic triage rules are fixtures, never an automatic fallback for a real-provider failure.

No paid calls were made. Actual hosted/local generation, native schema enforcement, live tool selection, model accuracy, live injection resistance, LangSmith uploads, remote CI, other operating systems and Python versions remain **unverified**. Offline CLIs disable tracing and block service sockets. Notebook execution retains normal local Jupyter kernel communication without contacting a model service. Publication remains scheduled for Phase 8.

## Phase 2 execution record — 2026-10-28

The foundation is implemented and verified locally on **Windows / CPython 3.12.13**. The older Phase 1 research below is preserved as history; the committed `uv.lock` is now the authoritative resolved dependency graph.

| Check | Result |
|---|---|
| Refresh all 42 inspected PyPI packages | Complete; [Phase 2 metadata](pypi-verification-phase2.json). Only pydantic-settings changed, from 2.16.1 to 2.16.2; the project lower bound was updated. |
| `uv sync` and `uv run pytest -q` | **42 passed, 3 skipped**. Skips: two authoring/PDF checks absent from the minimal install, plus the explicitly opt-in live test. |
| `uv sync --all-extras --group authoring` | Successful installation of all proposed extras on Windows, including Chroma, MCP, apps, Deep Agents and deployment packages. This is installation evidence, not runtime evidence for future lessons. |
| `uv run --group authoring pytest -q` | **44 passed, 1 skipped**. The sole skip is the live-provider test. Test sockets deny service connections, including localhost; only Python's internal async socket-pair creation is allowed. |
| `uv run ruff check .` | Passed. |
| `uv run ruff format --check .` | Passed. |
| `uv run python scripts/run_all_examples.py` | **2/2 implemented foundation targets passed** with fakes and networking disabled. All 139 planned module examples remain explicitly deferred. |
| Legacy/API scan | Zero violations; regression tests verify detection and standard-library exceptions. |
| Local and external link checks | Zero failures. **448 references** to explicitly planned future files remain deferred. Strict release-mode links still fail until the course is built. |
| Dataset validation | Exact requested counts; SHA-256 checks; foreign-key integrity; order arithmetic; matching CSV/database prices and stock; read-only seed access; isolated writes. |
| Repeatability | Two fresh builds in the same locked environment produced identical file bytes, including SQLite and PDF. |
| Handbook | Ten pages; extracted text/page labels checked; all ten rendered page images visually inspected for clipping, overlap and legibility. |
| Coverage gate | Zero violations for the current phase; all 21 teaching modules reported as unimplemented. Final-release mode deliberately fails. |

No paid model calls were made. Live OpenAI/Anthropic/Gemini behavior, actual Ollama generation, LangSmith uploads, Docker execution, other operating systems/Python versions and remote GitHub Actions remain **unverified**. The CI matrix is configured for Ubuntu/Windows Python 3.12–3.14 and a macOS 3.12 smoke job. GitHub publication remains scheduled for the final phase.

### Installed API checks

The actual installed functions/classes were inspected and the four chat-provider constructors plus all three embedding-provider constructors were exercised under network denial. Construction verifies imports and accepted parameters; it does not prove the remote service will accept a request.

| Import/API | Checked use |
|---|---|
| `langchain.chat_models.init_chat_model` | `model`, `model_provider`, provider-specific keyword arguments |
| `langchain.embeddings.init_embeddings` | `model`, `provider`, integration-specific options; installed registry includes `google_genai` even though an embedded docstring list omits it |
| `langchain_core.language_models.fake_chat_models.GenericFakeChatModel` | Scripted string/AIMessage iterator; invoke, batch, stream and async invocation |
| `langchain_core.embeddings.DeterministicFakeEmbedding` | `size`, embed_query and embed_documents; NumPy is required, so it is a base dependency for key-free tests |
| `langchain_core.messages` | SystemMessage, HumanMessage, AIMessage and tool-call message payloads |
| OpenAI chat integration | `api_key`, `timeout`, `max_retries`, `max_tokens`, `use_responses_api`, `reasoning_effort`; omit temperature when reasoning is enabled |
| Anthropic chat integration | `api_key`, `timeout`, `max_retries`, `max_tokens`; no temperature for the selected profile |
| Google chat/embedding integration | Chat timeout/token aliases; embeddings `api_key` and `request_options` |
| Ollama chat/embedding integration | `base_url`, `client_kwargs` timeout; chat `num_predict` and temperature |
| `langsmith.Client`, `tracing_context` | Client lifecycle methods exist; disabled tracing path runs offline. Enabled uploads are not tested. |
| Pydantic Settings | Dotenv precedence, SecretStr redaction, validation bounds and safe errors |

Sources: [model guide](https://docs.langchain.com/oss/python/langchain/models), [embedding initializer](https://reference.langchain.com/python/langchain/embeddings/base/init_embeddings), [Pydantic settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/), and the provider reference links already listed below. Model profiles were rechecked against the current official [OpenAI](https://developers.openai.com/api/docs/models/gpt-6-luna), [Anthropic](https://platform.claude.com/docs/en/models/haiku-5-5/overview) and [Gemini](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite) documentation.

CI action releases were checked using the official [checkout v7.0.1 release](https://github.com/actions/checkout/releases/tag/v7.0.1), [setup-uv v10.3.2 release](https://github.com/astral-sh/setup-uv/releases/tag/v10.3.2), and [uv integration guide](https://docs.astral.sh/uv/guides/integration/github/). CI selects uv 0.13.6; local verification used installed uv 0.12.18. Both the installed dependency graph and commands are recorded here without claiming a remote CI run.

### Foundation-specific decisions

- Python's Windows async loop uses an internal loopback socket pair. Blanket socket blocking initially prevented the test loop from starting. A narrowly scoped socket-pair allowance fixed the harness; a test still proves that ordinary connections to Ollama's localhost port are blocked.
- Bare `uv sync` intentionally omits PDF regeneration, notebooks and optional services. Install the authoring group to run both PDF tests. The initial full dependency installation and the default minimal installation were tested separately.
- The repository is a clone-based course with an editable `common` package, not a standalone data-bearing PyPI wheel. If importing it outside the checkout, set the process-level `BRIGHTWAVE_ROOT` to the clone. A value written only inside `.env` cannot relocate a configuration file that has not yet been found.
- `common.pretty` buffers streamed text by line before redacting configured credentials. Later token-streaming lessons must preserve that safety boundary or apply redaction before display.
- The generated data deliberately uses fixed historical dates. Production clock handling is separate. Golden sets are small teaching cases and do not establish statistical production quality.

## Phase 1 research record

**Checked: 2026-10-27, America/Chicago.** The raw PyPI metadata preserves upload timestamps in UTC, which can show October 28 while the local date is still October 27. Versions below were retrieved directly from the public PyPI JSON API; they are not inferred from search snippets.

## Verification levels

- **Release metadata checked:** latest published version, Requires-Python and direct dependency requirements for every proposed direct package. See [raw snapshot](pypi-verification.json).
- **Dependency resolution checked:** uv 0.12.18 successfully resolved the combined proposed course extras using Python 3.12 with universal platform resolution. See [candidate ranges](dependency-candidates.in) and [resolver output](dependency-resolution.txt). This is not uv.lock, an installation test or evidence that native wheels work on every OS.
- **Documentation checked:** the core official guides and API reference endpoints listed below were read. Reference HTML is sometimes poorly exposed by the browser reader; endpoints were also fetched directly. Individual signatures still require inspection against installed pinned packages before implementation.
- **Not yet checked:** import execution, exercise behavior, pytest, linting, notebook execution, Ollama/hosted calls, Docker, real Windows/Linux/macOS installation and GitHub CI. Those belong to the implementation phases.

## Versions and proposed bounds

Use a latest-verified lower bound and the next minor as the upper bound to limit API drift. The eventual uv.lock freezes the exact resolved graph. Recheck releases at the start of Phase 2; any change needs another resolution and validation pass. Python support is deliberately bounded to `>=3.12,<3.15`; NumPy 2.5.4 requires 3.12+, and the full chosen stack is the limiting factor, not LangChain alone.

| Package | Latest verified | Proposed range / decision | Requires Python | Source |
|---|---:|---|---|---|
| langchain | 1.4.7 | `>=1.4.7,<1.5.0` | `<4.0.0,>=3.10.0` | [PyPI](https://pypi.org/project/langchain/1.4.7/) |
| langchain-core | 1.7.0 | `>=1.7.0,<1.8.0` | `<4.0.0,>=3.10.0` | [PyPI](https://pypi.org/project/langchain-core/1.7.0/) |
| langgraph | 1.2.18 | `>=1.2.18,<1.3.0` | `>=3.10` | [PyPI](https://pypi.org/project/langgraph/1.2.18/) |
| langchain-text-splitters | 1.1.3 | `>=1.1.3,<1.2.0` | `<4.0.0,>=3.10.0` | [PyPI](https://pypi.org/project/langchain-text-splitters/1.1.3/) |
| langchain-openai | 1.7.3 | `>=1.7.3,<1.8.0` | `<4.0.0,>=3.10.0` | [PyPI](https://pypi.org/project/langchain-openai/1.7.3/) |
| langchain-anthropic | 1.7.7 | `>=1.7.7,<1.8.0` | `<4.0.0,>=3.10.0` | [PyPI](https://pypi.org/project/langchain-anthropic/1.7.7/) |
| langchain-google-genai | 4.4.2 | `>=4.4.2,<4.5.0` | `<4.0.0,>=3.10.0` | [PyPI](https://pypi.org/project/langchain-google-genai/4.4.2/) |
| langchain-ollama | 1.1.0 | `>=1.1.0,<1.2.0` | `<4.0.0,>=3.10.0` | [PyPI](https://pypi.org/project/langchain-ollama/1.1.0/) |
| langchain-community | 0.4.2 | `>=0.4.2,<0.5.0` | `<4.0.0,>=3.10.0` | [PyPI](https://pypi.org/project/langchain-community/0.4.2/) |
| langchain-chroma | 1.1.0 | `>=1.1.0,<1.2.0` | `<4.0.0,>=3.10.0` | [PyPI](https://pypi.org/project/langchain-chroma/1.1.0/) |
| pypdf | 6.21.3 | `>=6.21.3,<6.22.0` | `>=3.9` | [PyPI](https://pypi.org/project/pypdf/6.21.3/) |
| rank-bm25 | 0.2.2 | `>=0.2.2,<0.3.0` | `Not declared` | [PyPI](https://pypi.org/project/rank-bm25/0.2.2/) |
| langgraph-checkpoint-sqlite | 3.1.2 | `>=3.1.2,<3.2.0` | `>=3.10` | [PyPI](https://pypi.org/project/langgraph-checkpoint-sqlite/3.1.2/) |
| langchain-mcp-adapters | 0.3.2 | `Excluded from current install; archived; mcp<2 required` | `>=3.10` | [PyPI](https://pypi.org/project/langchain-mcp-adapters/0.3.2/) |
| mcp | 2.3.0 | `>=2.3.0,<2.4.0` | `>=3.10` | [PyPI](https://pypi.org/project/mcp/2.3.0/) |
| deepagents | 0.7.32 | `>=0.7.32,<0.8.0` | `<4.0,>=3.11` | [PyPI](https://pypi.org/project/deepagents/0.7.32/) |
| langsmith | 0.14.14 | `>=0.14.14,<0.15.0` | `>=3.10` | [PyPI](https://pypi.org/project/langsmith/0.14.14/) |
| fastapi | 0.162.0 | `>=0.162.0,<0.163.0` | `>=3.10` | [PyPI](https://pypi.org/project/fastapi/0.162.0/) |
| uvicorn | 0.54.0 | `>=0.54.0,<0.55.0` | `>=3.10` | [PyPI](https://pypi.org/project/uvicorn/0.54.0/) |
| streamlit | 1.66.1 | `>=1.66.1,<1.67.0` | `>=3.11` | [PyPI](https://pypi.org/project/streamlit/1.66.1/) |
| pytest | 9.2.0 | `>=9.2.0,<9.3.0` | `>=3.10` | [PyPI](https://pypi.org/project/pytest/9.2.0/) |
| pytest-asyncio | 1.4.1 | `>=1.4.1,<1.5.0` | `>=3.10` | [PyPI](https://pypi.org/project/pytest-asyncio/1.4.1/) |
| ruff | 0.17.3 | `>=0.17.3,<0.18.0` | `>=3.7` | [PyPI](https://pypi.org/project/ruff/0.17.3/) |
| pre-commit | 4.7.0 | `>=4.7.0,<4.8.0` | `>=3.11` | [PyPI](https://pypi.org/project/pre-commit/4.7.0/) |
| nbstripout | 0.9.1 | `>=0.9.1,<0.10.0` | `>=3.10` | [PyPI](https://pypi.org/project/nbstripout/0.9.1/) |
| jupyter | 1.1.1 | `>=1.1.1,<1.2.0` | `Not declared` | [PyPI](https://pypi.org/project/jupyter/1.1.1/) |
| rich | 15.0.0 | `>=15.0.0,<15.1.0` | `>=3.9.0` | [PyPI](https://pypi.org/project/rich/15.0.0/) |
| pydantic | 2.14.1 | `>=2.14.1,<2.15.0` | `>=3.10` | [PyPI](https://pypi.org/project/pydantic/2.14.1/) |
| pydantic-settings | 2.16.1 | `>=2.16.1,<2.17.0` | `>=3.11` | [PyPI](https://pypi.org/project/pydantic-settings/2.16.1/) |
| python-dotenv | 1.2.4 | `>=1.2.4,<1.3.0` | `>=3.10` | [PyPI](https://pypi.org/project/python-dotenv/1.2.4/) |
| httpx | 0.28.1 | `>=0.28.1,<0.29.0` | `>=3.8` | [PyPI](https://pypi.org/project/httpx/0.28.1/) |
| numpy | 2.5.4 | `>=2.5.4,<2.6.0` | `>=3.12` | [PyPI](https://pypi.org/project/numpy/2.5.4/) |
| matplotlib | 3.11.2 | `>=3.11.2,<3.12.0` | `>=3.11` | [PyPI](https://pypi.org/project/matplotlib/3.11.2/) |
| reportlab | 5.1.0 | `>=5.1.0,<5.2.0` | `<4,>=3.9` | [PyPI](https://pypi.org/project/reportlab/5.1.0/) |
| langgraph-cli | 0.4.40 | `>=0.4.40,<0.5.0` | `>=3.10` | [PyPI](https://pypi.org/project/langgraph-cli/0.4.40/) |
| langgraph-checkpoint-postgres | 3.2.0 | `>=3.2.0,<3.3.0` | `>=3.10` | [PyPI](https://pypi.org/project/langgraph-checkpoint-postgres/3.2.0/) |
| langchain-tavily | 0.2.18 | `>=0.2.18,<0.3.0` | `<4.0,>=3.10` | [PyPI](https://pypi.org/project/langchain-tavily/0.2.18/) |
| uv | 0.13.6 | `Bootstrap tool; tested resolver is installed 0.12.18` | `>=3.8` | [PyPI](https://pypi.org/project/uv/0.13.6/) |
| hatchling | 1.33.0 | `>=1.33.0,<1.34.0` | `>=3.10` | [PyPI](https://pypi.org/project/hatchling/1.33.0/) |
| fastmcp | 4.1.4 | `>=4.1.4,<4.2.0` | `>=3.10` | [PyPI](https://pypi.org/project/fastmcp/4.1.4/) |
| fastmcp-slim | 4.1.4 | `Transitive check; exact version selected by fastmcp` | `>=3.10` | [PyPI](https://pypi.org/project/fastmcp-slim/4.1.4/) |
| psycopg | 3.3.6 | `>=3.3.6,<3.4.0` | `>=3.10` | [PyPI](https://pypi.org/project/psycopg/3.3.6/) |

## Confirmed core documentation

| Area | Official sources read | Implementation verification still required |
|---|---|---|
| Chat initialization and model interface | [Guide](https://docs.langchain.com/oss/python/langchain/models), [init_chat_model reference](https://reference.langchain.com/python/langchain/chat_models/base/init_chat_model) | Provider-specific kwargs and capability tests |
| Embeddings | [Guide](https://docs.langchain.com/oss/python/integrations/embeddings/), [init_embeddings reference](https://reference.langchain.com/python/langchain/embeddings/base/init_embeddings) | Provider names, dimensions and fake-model imports |
| Agents and ToolRuntime | [Agents](https://docs.langchain.com/oss/python/langchain/agents), [tools](https://docs.langchain.com/oss/python/langchain/tools), [factory reference](https://reference.langchain.com/python/langchain/agents/factory/create_agent) | Import/signature tests with the locked release |
| Structured output | [Official guide](https://docs.langchain.com/oss/python/langchain/structured-output) | Pydantic/TypedDict/JSON Schema parity; provider method differences |
| Middleware | [Built-ins](https://docs.langchain.com/oss/python/langchain/middleware/built-in), [reference](https://reference.langchain.com/python/langchain/agents/middleware) | All requested classes plus hook signatures and sync/async behavior |
| Memory | [Short-term](https://docs.langchain.com/oss/python/langchain/short-term-memory), [long-term](https://docs.langchain.com/oss/python/langchain/long-term-memory) | Saver/store lifecycle and process restart tests |
| Graphs | [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api), [Functional API](https://docs.langchain.com/oss/python/langgraph/functional-api), [workflows](https://docs.langchain.com/oss/python/langgraph/workflows-agents) | Node signatures, checkpoint resume, Send and stream tests |
| Chroma | [Integration](https://docs.langchain.com/oss/python/integrations/vectorstores/chroma) | Persistent CRUD, filtering and dimension checks |
| Testing and evaluation | [Tests](https://docs.langchain.com/oss/python/langchain/test), [evaluate](https://docs.langchain.com/langsmith/evaluate-llm-application) | Fakes with tool support, offline judge fixtures, live opt-in path |
| Deep Agents | [Overview](https://docs.langchain.com/oss/python/deepagents/overview) | Optional package is pre-1.0; verify factory and backends in the locked version |
| Deployment | [Local development](https://docs.langchain.com/langsmith/local-dev-testing) | Current names: LangGraph CLI, Agent Server, Studio, LangSmith Deployment |

## Required adjustments and explicit limits

1. **MCP migration:** the [old adapter repository](https://github.com/langchain-ai/langchain-mcp-adapters) was archived on September 17, 2026. PyPI 0.3.2 requires `mcp>=1.24.0,<2.0.0`, conflicting with current SDK 2.3.0. The [official migration guide](https://docs.langchain.com/oss/python/migrate/langchain-mcp-adapters) replaces MultiServerMCPClient with `langchain.mcp.MCPAdapter` and `list_tools()`. Proposed main path: `langchain[mcp]`, FastMCP 4.1.4 and official MCP SDK 2.3.0; explain the old client only in the migration guide. **MCPAdapter is explicitly beta** even though LangChain 1.4.7 is stable. Keep it behind `common/mcp.py`, pin its minor range and test both transports. If its locked behavior is unsuitable, use the official SDK client with narrowly typed LangChain inventory tools; do not silently fall back to the archived dependency. This is a visible proposed adjustment to the original client requirement.
2. **Deep Agents:** 0.7.32 exists but is pre-1.0. The required lesson first implements planning, confined virtual files and subagents with create_agent and TodoListMiddleware. The package-specific demonstration is optional, with its exact tested APIs recorded later.
3. **Advanced retrieval:** implement fusion, parent lookup, rewriting, compression and embedding caching with current Runnable/Document/Embeddings primitives. Do not import retired convenience chains. The original community-loader proposal was superseded in Phase 4 by core BaseLoader adapters after verifying the upstream sunset; the retired package is no longer installed.
4. **Fake-model limits:** GenericFakeChatModel can supply scripted messages but is not automatically a full tool-binding/structured-output provider. Test `bind_tools` and structured-output behavior explicitly and provide a small scripted adapter in common/testing.py where required. Random fake embeddings are not evidence of semantic retrieval quality.
5. **Parameter portability:** `temperature=0` is used for comparisons when the model accepts it. The [Haiku 5.5 specification](https://platform.claude.com/docs/en/models/haiku-5-5/overview) says to omit temperature/top_p/top_k. Document and test this exception; deterministic CI uses fakes and live evaluations use tolerances. Do not send unsupported parameters for the sake of a generic interface.
6. **One-line provider switching:** read per-provider model defaults from .env.example, leaving LLM_MODEL blank unless explicitly overridden. With EMBEDDINGS_PROVIDER=auto, selecting Ollama also selects local embeddings; hosted chat defaults to OpenAI embeddings unless overridden. Anthropic chat is supported without inventing an Anthropic embedding model.
7. **Local versus account-free:** local LangGraph execution and generated Mermaid diagrams work without LangSmith. The current Studio/local Agent Server setup documents a LangSmith key, so that service demonstration is optional and cannot block module completion.
8. **Installation versus offline tests:** a fresh uv sync downloads packages. The no-network guarantee applies to pytest and smoke examples after dependencies are installed, or to uv sync with a populated cache. External link checks run in a separate network-enabled CI step; local-link checks and all default tests stay offline.
9. **Security and evaluation:** parameterized tools read immutable seed data; write tools use disposable runtime copies. Refund approval is enforced in code, writes are idempotent, and notifications are a local outbox. No claim of production security comes from a prompt alone. Quality improvements must be measured, never invented.

## Model profile candidates

These are documentation-verified candidates, not successful live-call claims. All identifiers and per-token price assumptions will live in .env.example; helper modules will not embed changing model names. Verify availability again before Phase 2 and record actual live results when credentials/local models are available.

| Profile | Candidate | Evidence / constraint |
|---|---|---|
| OpenAI chat default | `gpt-6-luna` | [Current model entry](https://developers.openai.com/api/docs/models/gpt-6-luna); standard input/output rates $0.10/$0.50 per million tokens; use reasoning effort none for introductory temperature=0 examples and Chat Completions tools |
| Anthropic chat | `claude-haiku-5-5` | [Model specification](https://platform.claude.com/docs/en/models/haiku-5-5/overview); omit temperature |
| Gemini chat | `gemini-3.5-flash-lite` | [Stable model specification](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite); avoid 2.5 defaults restricted for new projects |
| Ollama text/tools | `qwen3:4b` | [Registry](https://ollama.com/library/qwen3:4b); small tools-capable model; quality still needs live checks |
| OpenAI embeddings | `text-embedding-3-small` | [Model entry](https://developers.openai.com/api/docs/models/text-embedding-3-small); $0.02 per million input tokens |
| Ollama embeddings | `embeddinggemma` | [Registry](https://ollama.com/library/embeddinggemma); 300M parameters; respect its 2K context limit |

| Ollama vision | `qwen3-vl:4b` | [Registry](https://ollama.com/library/qwen3-vl:4b); vision and tools; documented Ollama minimum 0.12.7 |
| Gemini text embeddings | `gemini-embedding-001` | [Official embeddings guide](https://ai.google.dev/gemini-api/docs/embeddings); still available for text-only use |

A bounded OpenAI example using 4,000 uncached input tokens and 1,000 output tokens would cost approximately $0.0009 at these standard rates, before extra calls, cache writes or paid tools. Module-level estimates will budget the complete loop and retry ceiling. Local inference has no API fee but needs suitable hardware and initial downloads.

The inspected GPT-4.1 mini and GPT-5.4 nano entries are marked deprecated, so they are excluded as defaults. [Current parameter guidance](https://developers.openai.com/api/docs/guides/latest-model) permits temperature only with reasoning disabled for this model family. For reasoning/tool lessons use Responses and omit incompatible sampling parameters. Per-provider parameter sets, prices for other providers and live capabilities remain Phase 2 verification tasks. No paid model calls were made in Phase 1.
