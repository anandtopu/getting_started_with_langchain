# Foundation glossary

This glossary grows with the course. These terms cover modules 00–05; the final phase expands it to at least 60 terms.

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

Return to the [learning path](../LEARNING_PATH.md).
