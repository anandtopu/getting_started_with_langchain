# Provider profiles and limits

All examples obtain models from `common.models`. Configuration precedence is: explicit helper settings, process environment, `.env`, then `.env.example`. Provider model names are read from the profile file; none are embedded in the factory. An explicit `LLM_MODEL` or `EMBEDDINGS_MODEL` overrides the profile and remains your responsibility to choose compatibly.

| Provider setting | Key | Chat profile | Embeddings | Notes |
|---|---|---|---|---|
| `openai` | `OPENAI_API_KEY` | `gpt-6-luna` | `text-embedding-3-small` | Responses API, reasoning effort `none` in the starter |
| `anthropic` | `ANTHROPIC_API_KEY` | `claude-haiku-5-5` | Select OpenAI, Gemini or Ollama independently | Temperature omitted for the current profile |
| `google_genai` | `GOOGLE_API_KEY` | `gemini-3.5-flash-lite` | `gemini-embedding-001` | Set `EMBEDDINGS_PROVIDER=google_genai` to avoid a second hosted key |
| `ollama` | None | `qwen3:4b` | `embeddinggemma` | Server and models must already be installed |

With `EMBEDDINGS_PROVIDER=auto`, Ollama chat uses Ollama embeddings; other chat providers use OpenAI embeddings. Selecting Anthropic chat therefore does not mean Anthropic embeddings exist. Use `EMBEDDINGS_PROVIDER=ollama` for local embeddings with any chat provider. Rebuild a vector store after changing embedding models or dimensions.

## Capabilities must be tested, not assumed

The provider constructors and parameter names have been checked with installed packages. No paid model or local Ollama generation has yet been run for this phase. Tool calling, image input and structured-output methods depend on the selected model as well as the integration package. The current local image profile is `qwen3-vl:4b`; it needs a separate download and Ollama 0.12.7 or newer according to its registry entry.

OpenAI's selected profile supports temperature only with reasoning disabled. The factory drops temperature if a non-`none` reasoning effort is selected. Haiku 5.5 requires temperature to be omitted. Other model overrides may need the capability flags in `.env` changed. Model comparisons use temperature zero where accepted; temperature zero is not a guarantee of identical live text.

Hosted adapters use their supported retry settings. Ollama receives a request timeout through client options; it has no identical `max_retries` constructor setting. Explicit runnable retries will be taught later. API errors are not converted into fake success.

## Cost accounting

`.env.example` records the current standard uncached OpenAI profile rates, and `common.pretty` uses `usage_metadata` to estimate cost. An unknown model or absent usage yields **unknown**, never a false zero. The estimate does not yet account for cache-write pricing, provider discounts or paid tool fees. Later budget enforcement will bound the full application run. Ollama inference has no API fee; hardware and initial downloads still cost resources.

## Offline mode

`COURSE_OFFLINE=true`, `--offline` on the starter, or an explicit helper argument selects `GenericFakeChatModel` and `DeterministicFakeEmbedding`. Fake vectors are repeatable random numbers, not semantic embeddings. Scripted fake messages can contain a tool-call payload but do not implement tool binding or structured-output generation. Those test adapters will arrive with the relevant lessons. Offline tests disable tracing and block service connections; Windows' internal async socket pair is the sole narrow local exception.

Sources and checked release versions are in [verification notes](VERIFICATION_NOTES.md).
