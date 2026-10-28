# 5 | Apps, evaluation and release

## Streaming

FastAPI SSE carries progress, text and a final done/error event. Partial text is not successful completion. Handle disconnects, deadlines and admission cleanup. Streamlit keeps session state per browser session.

## Authentication

Authenticate first, derive the principal on the server, then authorize the thread or review. Never accept customer identity from tool arguments. Give reviewers separate credentials.

## Evaluation

Run the actual application path on held-out cases. Score tool trajectory, ownership, quote support, factual correctness and tone separately. Fakes test contracts; live and human review measure real quality.

## Budgets and traces

Reserve a conservative call allowance before execution, including nested calls. Unknown token usage is not zero cost. Redact logs and avoid raw sensitive spans; tracing can upload prompts.

## Deployment

Build from the repository root, inject secrets at runtime, run as non-root and keep source read-only. SQLite plus local admission uses one worker. A Postgres saver probe does not prove full horizontal scalability.

## Release decision

The scripted Support Copilot passes 4/6 complete contracts. Return and shipping facts still fail, so customer release stays blocked. Publishing a teaching repository is not customer deployment readiness.

## Try it

```text
uv sync --extra apps
uv run --no-sync python scripts/evaluate.py --offline
uv run --no-sync python scripts/evaluate.py --offline --release
```

[Print the one-page PDF](tier_5_production.pdf). Commands run from the repository root.
