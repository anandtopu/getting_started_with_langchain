# Migrating from older tutorials

This is the only course file that deliberately shows legacy APIs. These are comparison fragments, not executable lessons. Legacy chains now live in `langchain-classic`; installing that compatibility package does not turn an old tutorial into the current main path. Use the pinned versions in pyproject.toml and the executable examples linked below.

| Old tutorial fragment | Current replacement | Why |
|---|---|---|
| `from langchain.llms import OpenAI` | `from common.models import get_chat_model` | Central provider configuration and the chat interface. |
| `from langchain.chat_models import ChatOpenAI` | `from langchain.chat_models import init_chat_model` through the shared factory | Provider adapters are separate packages; avoid provider-specific construction in lessons. |
| `LLMChain(llm=model, prompt=prompt)` | `prompt \| model \| StrOutputParser()` | A visible Runnable pipeline with explicit inputs and outputs. |
| `ConversationChain(llm=model)` | `create_agent(model=model, tools=[], checkpointer=saver)` | Conversation state is explicit and scoped by thread. |
| `SequentialChain(chains=steps)` | `step_one \| step_two` or ordinary Python | Use a fixed pipeline for known steps. Use StateGraph when routing or durable state is necessary. |
| `RetrievalQA.from_chain_type(llm=model, retriever=retriever)` | Retrieve documents, format evidence, call the model and validate citations | See the complete current RAG pipeline instead of relying on a hidden chain contract. |
| `initialize_agent(tools, model)` | `create_agent(model=model, tools=tools)` | Current LangChain agent factory. |
| `AgentExecutor(agent=agent, tools=tools)` | `agent = create_agent(model, tools)` followed by `agent.invoke({"messages": messages})` | The current agent already manages the tool loop. |
| `ConversationBufferMemory()` | `InMemorySaver()` for a process, `SqliteSaver` for a local persistent thread | Explicit checkpointers replace implicit history containers. |
| `ConversationSummaryMemory(llm=model)` | `SummarizationMiddleware(model=model, trigger=("tokens", 2000), keep=("messages", 4))` | Manage model context separately from durable stored history. |
| `ConversationBufferWindowMemory(k=4)` | Bound model-facing messages or use summarization middleware | A window is context management, not authorization or persistence. |
| `chain.run(question)` | `chain.invoke({"question": question})` | Supply the actual input shape; inspect the returned type. |
| `model.predict(text)` | `model.invoke(text)` and then `message.content` | Chat models return messages with metadata, not only strings. |
| `from langgraph.prebuilt import create_react_agent` | `from langchain.agents import create_agent` | The LangChain factory is the current primary agent API. |
| `from langchain_mcp_adapters.client import MultiServerMCPClient` | `from langchain.mcp import MCPAdapter`, with a reviewed FastMCP Client | The earlier adapter is archived in this verified package baseline; current replacement is beta. |

The one-line replacements show the direction, not a promise of identical semantics. Prompts, output types, stream formats, persistence and error handling must be retested. Never copy a public tutorial's model name or outdated constructor arguments without checking the selected provider.

## Run current equivalents

- [Models and messages](../modules/01_chat_models/README.md): provider factory, invoke, stream, batch and async.
- [Runnable pipelines](../modules/04_lcel_runnables/README.md): composition, dictionary shapes and bounded retries.
- [RAG](../modules/08_rag_fundamentals/README.md): explicit evidence and validated citations.
- [Agents](../modules/10_agents/README.md) and [memory](../modules/11_memory/README.md): current factory, owned thread IDs and checkpoint lifecycle.
- [Middleware](../modules/12_middleware/README.md): actual installed summarization and human-review signatures.
- [MCP](../modules/13_mcp/README.md): SDK server, real transports, beta adapter and trust checks.

## Migration checklist

1. Start in a new virtual environment using the committed lockfile.
2. Map the old example's input, output and side effects before changing imports.
3. Replace one boundary at a time and use synthetic inputs with no network first.
4. Test message/tool-call IDs, resume behavior, denied permissions and duplicate actions.
5. Run a separately labelled live evaluation; fake-model success does not prove provider capability or answer quality.

Official references: [LangChain v1 migration](https://docs.langchain.com/oss/python/migrate/langchain-v1), [current agents](https://docs.langchain.com/oss/python/langchain/agents), [short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory), and [MCP](https://docs.langchain.com/oss/python/langchain/mcp).
