# 3 | Agents, memory and MCP

## The loop

create_agent combines a model, tools and repeated decisions. Bind the authenticated identity in host context. Tools must check ownership independently of model obedience.

## State and memory

A checkpointer saves a conversation under thread_id. A Store holds cross-thread data in explicit namespaces. Authorize the owner before loading either. Summaries save tokens but can omit facts.

## Middleware

Hooks surround agent, model and tool execution. Use limits for bounds, retries for transient errors and fallback for defined provider failures. Count retries and nested model calls in budgets.

## Human review

An interrupt pauses an action; Command(resume=...) supplies a decision. Review the exact quote and inputs. Revalidate trusted facts after resume. Rejection means no write; replay needs an idempotency key.

## MCP trust

MCP transports tool schemas and results; it does not make a server trustworthy. Review program/endpoint, tool names, fields and permissions. The pinned current adapter is beta. Keep approvals outside model tools.

## Failure to check

Cross-owner access, guessed approval receipts, changed action payloads, duplicate writes, runaway tools and raw sensitive tracing all need host-level tests.

## Try it

```text
uv sync --extra agents
uv run --no-sync python capstones/05_personal_ops/solution.py --offline
uv run --no-sync pytest tests/test_security.py
```

[Print the one-page PDF](tier_3_agents.pdf). Commands run from the repository root.
