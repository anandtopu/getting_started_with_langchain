"""Explicit graph: Build a StateGraph that increments attempts once and returns the compiled graph.

Run: uv run --extra agents python modules/14_langgraph/exercises/02_apply.py --offline
Expected: Runnable baseline; complete YOUR CODE HERE to pass target tests.
Cost: No model calls. Requires: agents
"""

from typing import TypedDict

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


class State(TypedDict):
    attempts: int


def build() -> object:
    # YOUR CODE HERE: Build a StateGraph that increments attempts once and returns the compiled
    # graph.
    return lambda state: state


def main() -> None:
    lesson_settings()
    graph = build()
    print_text(
        str(graph.invoke({"attempts": 0}) if hasattr(graph, "invoke") else graph({"attempts": 0}))
    )


if __name__ == "__main__":
    run_cli(main)
