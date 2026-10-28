# 1 | Foundations

## Choose the smallest useful piece

One call for one answer. A chain for a fixed sequence. A tool loop when the model must choose which permitted operation happens next.

## Models and messages

get_chat_model() centralizes provider setup. invoke returns one message; stream yields chunks; batch handles several inputs; ainvoke can be awaited. System sets behavior, human asks, AI responds, tool returns an executed result.

## Prompt and schema

ChatPromptTemplate formats named fields. MessagesPlaceholder inserts message lists. with_structured_output(Model) validates a Pydantic schema, not the truth of a claim. Use bounded repair for validation errors.

## Runnables

a | b pipes the first output into the second input. RunnableParallel shares an input across branches. RunnablePassthrough.assign adds fields to a dictionary. Keep input/output shapes visible.

## Tool calling

@tool turns a typed function and docstring into a schema. The model requests JSON; your host validates and dispatches it. A ToolMessage must retain its matching tool_call_id. Tool schemas do not grant permission.

## Failure to check

Missing template variable: provide the named field. Wrong ToolMessage ID: copy the AI tool-call ID. Endless loop: impose model/tool limits. Never infer live accuracy from scripted fake output.

## Try it

```text
uv sync
uv run python scripts/first_call.py --offline
uv run python modules/05_tools/examples/01_tool_schema.py --offline
```

[Print the one-page PDF](tier_1_foundations.pdf). Commands run from the repository root.
