# Course glossary

This glossary grows with the course. These terms cover modules 00–13; later phases add orchestration and production terminology.

| Term | Plain-English meaning | First lesson |
|---|---|---|
| LLM | A large language model that predicts token sequences from context | 00 |
| Inference | Running an already trained model to produce an answer | 00 |
| Token | A tokenizer-defined piece of text; not necessarily a word | 00 |
| Tokenizer | The model-specific conversion between text and token IDs | 00 |
| Context window | The token capacity available to a model request | 00 |
| Temperature | A sampling setting controlling randomness, not truth | 00 |
| Hallucination | A plausible claim unsupported by available evidence | 00 |
| Provider | The service or local runtime executing a model | 00 |
| Adapter | Code translating the common model interface into a provider protocol | 00 |
| Fixture | Predetermined test data, not an intelligent prediction | 00 |
| Trace | A record of steps, inputs, outputs and timing from an execution | 00 |
| Message | A piece of conversation carrying a role and content | 01 |
| System message | Application instructions sent as a distinct conversation role | 01 |
| Human message | Customer-supplied request or other user input | 01 |
| AIMessage | LangChain's representation of a model reply or tool request | 01 |
| ToolMessage | A program result associated with a model's tool-call ID | 01 |
| Content block | A typed content piece such as text or an image | 01 |
| Streaming | Consuming partial output before the full response is complete | 01 |
| Batch | Processing a collection of independent inputs | 01 |
| Async | Execution that can yield while waiting for input/output | 01 |
| Coroutine | An awaitable computation created by an async function | 01 |
| Event loop | The scheduler that advances asynchronous work | 01 |
| Concurrency | Overlapping work, often while requests wait for responses | 01 |
| Rate limit | A bound on request starts or resource use per time interval | 01 |
| Usage metadata | Provider-reported input/output token accounting | 01 |
| Prompt template | Instructions with named blanks filled from input variables | 02 |
| Partial variable | A prompt variable bound before the remaining inputs arrive | 02 |
| Few-shot prompting | Including example input/output pairs in the current context | 02 |
| Delimiter | A marker separating source data from other prompt content | 02 |
| Structured output | An answer represented according to a defined data contract | 03 |
| Schema | A description of fields, types and permitted values | 03 |
| Pydantic | A Python library validating data against typed model classes | 03 |
| Enum | A finite set of allowed values | 03 |
| Nullable | A field whose value may be null; not necessarily omissible | 03 |
| TypedDict | Type hints describing dictionary keys; not runtime validation | 03 |
| Parser | Code transforming generated output into a consumable representation | 03 |
| Exact-match accuracy | Fraction of labelled records with every evaluated field correct | 03 |
| Runnable | A composable component with invoke, batch and related interfaces | 04 |
| LCEL | LangChain Expression Language for composing runnable dataflow | 04 |
| Fan-out | Sending the same input to several branches | 04 |
| Passthrough | Returning an input unchanged so it can be retained or enriched | 04 |
| Retry | Repeating a failed operation within an explicit bound | 04 |
| Fallback | An alternative runnable attempted after specified failures | 04 |
| Tool | A callable application function exposed through an input schema | 05 |
| Tool call | A model-written request naming a tool, arguments and an ID | 05 |
| Dispatcher | Application code resolving an allowed tool name and executing it | 05 |
| Agent | A model plus tools and a loop that uses results to decide what comes next | 05 |
| Runtime context | Trusted per-run information injected by the application | 05 |
| State | Data that evolves during a workflow, such as message history | 05 |
| Parameterized SQL | SQL whose values are bound separately from query syntax | 05 |
| Authorization | Code-enforced permission to access a particular resource | 05 |
| Prompt injection | Untrusted content attempting to redirect the model's instructions | 05 |
| Document | Text plus metadata, with an optional identifier | 06 |
| Metadata | Labels such as source file, page, price or category attached to a record | 06 |
| Provenance | Information showing where evidence came from and how it was transformed | 06 |
| Lazy loading | Yielding records as they are requested instead of first collecting every result | 06 |
| OCR | Optical character recognition: converting images of letters into machine-readable text | 06 |
| Chunk | A bounded piece of a larger source document | 06 |
| Chunk overlap | Text shared between neighbouring chunks to reduce loss at boundaries | 06 |
| Parent ID | A reference linking a chunk to its original page or section | 06 |
| Embedding | A model-produced list of numbers representing text in a learned coordinate space | 07 |
| Dimension | The number of coordinates in a vector | 07 |
| Cosine similarity | A measure comparing vector directions using their normalized dot product | 07 |
| SVD | Singular value decomposition: a matrix method that can project vectors onto fewer axes | 07 |
| Vector store | An index storing vectors with document IDs, text and metadata | 07 |
| Collection | A named group of records in a vector store | 07 |
| Retriever | A component that takes a query and returns relevant Documents | 07 |
| MMR | Maximal marginal relevance: balancing query relevance against repeated information | 07 |
| Cache namespace | Part of a cache identity that keeps incompatible values separate | 07 |
| Index manifest | A record of model, dimensions and corpus identity used to validate a stored index | 07 |
| RAG | Retrieval-augmented generation: supplying retrieved evidence to a model when answering | 08 |
| BM25 | A lexical scoring method based on matching words, their rarity and document length | 08 |
| Grounding | Connecting an answer to evidence supplied for that request | 08 |
| Citation | A reference to evidence, ideally resolved and validated by application code | 08 |
| Entailment | A relationship in which the evidence logically supports an answer's claim | 08 |
| Abstention | Explicitly declining to answer when available evidence is insufficient | 08 |
| Query rewriting | Rephrasing a search request, optionally resolving references using supplied history | 09 |
| Hybrid search | Combining lexical and semantic search results | 09 |
| RRF | Reciprocal-rank fusion: combining ranked lists using inverse rank contributions | 09 |
| Reranking | Reordering an initial shortlist using a second relevance assessment | 09 |
| Contextual compression | Keeping the parts of retrieved evidence most useful for the current question | 09 |
| Parent retrieval | Searching small chunks, then returning their larger source sections | 09 |
| Retrieval hit rate | Fraction of answerable questions whose expected evidence appears in the shortlist | 09 |
| Evaluation proxy | An easily measured signal that approximates, but does not prove, a target quality | 09 |
| Held-out set | Examples kept separate from tuning so they can test generalisation | 09 |
| LLM judge | A model asked to assess another answer using an explicit rubric | 09 |
| Transaction | A set of database operations that commit together or roll back together | 10 |
| Idempotency key | An identifier used to recognize retries of the same logical operation | 10 |
| Dataclass | A Python record type that declares named fields | 10 |
| Structured response | Parsed agent output that conforms to a declared schema | 10 |
| Recursion limit | A cap on graph execution steps, not a direct count of model calls | 10 |
| Checkpointer | A component that saves workflow state between steps and turns | 11 |
| Thread ID | A storage address selecting one conversation's saved state | 11 |
| Short-term memory | State retained within one conversation thread | 11 |
| Long-term memory | Scoped records reusable across separate conversations | 11 |
| Namespace | An application-defined grouping of records, often by customer or tenant | 11 |
| Message reducer | Logic that combines new messages with existing state using their identities | 11 |
| Summarization | Replacing older text with a shorter model-written account that may lose details | 11 |
| Middleware | Code attached around agent, model or tool lifecycle operations | 12 |
| Hook | A function called at a defined lifecycle boundary | 12 |
| Handler | The callable a wrapper invokes to continue the underlying operation | 12 |
| Interrupt | A saved workflow pause that requires a later input before continuing | 12 |
| Resume command | A graph input carrying a decision for paused work | 12 |
| PII | Personally identifying information, whose detection depends on the chosen rules | 12 |
| Tool selector | A component that narrows available tool schemas based on a request | 12 |
| MCP | Model Context Protocol: a standard for discovering and calling service capabilities | 13 |
| Transport | The channel carrying protocol messages, such as pipes or HTTP | 13 |
| Stdio | A process's standard input/output streams, used here for protocol communication | 13 |
| Streamable HTTP | MCP's HTTP transport for requests and optionally streamed server events | 13 |
| ASGI | The Python interface between an asynchronous web application and its server | 13 |
| Discovery | Asking a service which capabilities and schemas it advertises | 13 |
| Allowlist | An explicit set of accepted names, values or endpoints | 13 |

Return to the [learning path](../LEARNING_PATH.md).
