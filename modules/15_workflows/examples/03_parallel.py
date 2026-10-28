"""Join two independent review analyses before producing a summary.

Run: uv run --extra agents python modules/15_workflows/examples/03_parallel.py --offline
Expected: One deterministic report contains both worker outputs.
Cost: No model calls. Offline fixtures incur no API fee.
Requires: agents
"""

import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.workflows import category_facts, review_groups


class State(TypedDict):
    facts: Annotated[list[dict], operator.add]
    report: str


def ratings(state: State) -> dict:
    groups = review_groups()
    category = next(iter(groups))
    return {"facts": [{"kind": "ratings", "value": category_facts(category, groups[category])}]}


def sample(state: State) -> dict:
    return {"facts": [{"kind": "scope", "value": "Synthetic reviews, not market research."}]}


def merge(state: State) -> dict:
    return {"report": str(sorted(state["facts"], key=lambda row: row["kind"]))}


def main() -> None:
    lesson_settings()
    graph = StateGraph(State)
    for name, node in [("ratings", ratings), ("sample", sample), ("merge", merge)]:
        graph.add_node(name, node)
    graph.add_edge(START, "ratings")
    graph.add_edge(START, "sample")
    # KEY IDEA: a list edge waits for both producers; the reducer accepts their writes.
    graph.add_edge(["ratings", "sample"], "merge")
    graph.add_edge("merge", END)
    print_text(str(graph.compile().invoke({"facts": [], "report": ""})))


if __name__ == "__main__":
    run_cli(main)
