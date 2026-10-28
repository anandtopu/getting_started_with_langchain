# Verification notes

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
3. **Advanced retrieval:** implement fusion, parent lookup, rewriting, compression and embedding caching with current Runnable/Document/Embeddings primitives. Do not import retired convenience chains. `langchain-community` is restricted to loaders and may itself install `langchain-classic` transitively; the course does not use those legacy chain APIs.
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
