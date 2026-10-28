"""Explicit graph: Build a StateGraph that increments attempts once and returns the compiled graph.

Run: uv run --extra agents python modules/14_langgraph/solutions/02_apply.py --offline
Expected: Runnable reference result.
Cost: No model calls. Requires: agents
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


class State(TypedDict):
    attempts: int


def build() -> object:
    graph = StateGraph(State)
    graph.add_node("count", lambda state: {"attempts": state["attempts"] + 1})
    graph.add_edge(START, "count")
    graph.add_edge("count", END)
    return graph.compile()


def main() -> None:
    lesson_settings()
    graph = build()
    print_text(
        str(graph.invoke({"attempts": 0}) if hasattr(graph, "invoke") else graph({"attempts": 0}))
    )


if __name__ == "__main__":
    run_cli(main)
