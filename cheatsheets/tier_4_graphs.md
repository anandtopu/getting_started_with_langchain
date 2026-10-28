# 4 | Graphs and teams

## StateGraph

Define typed state, nodes returning updates, and edges from START to END. compile produces the executable graph. Conditional edges make routing explicit and testable.

## Reducers

A reducer defines how concurrent updates combine. operator.add concatenates lists; add_messages manages message identity. A missing reducer can cause conflicting concurrent updates.

## Durability

Checkpoint state under a stable, owned thread ID. interrupt pauses; resume continues. Keep side effects idempotent because replay can execute a node again. State history supports investigation and controlled forks.

## Workflow patterns

Use fixed chaining for known steps, a router for distinct paths, Send for dynamic fan-out, and an evaluator-optimizer loop for bounded revisions. Set both attempt and recursion limits.

## Multiple agents

Give each worker only relevant context and tools. Merge evidence explicitly. A handoff changes control; a subagent tool returns a result. More agents add cost and failure paths, not automatic intelligence.

## Research release

Planner -> readers -> writer -> critic. Require known source IDs and exact evidence even when the critic approves. Stop without a report when attempts are exhausted. Synthetic sources are not market forecasts.

## Try it

```text
uv sync --extra agents
uv run --no-sync python capstones/04_research_crew/solution.py --offline
uv run --no-sync pytest capstones/04_research_crew
```

[Print the one-page PDF](tier_4_graphs.pdf). Commands run from the repository root.
