"""Inspect history, replay a checkpoint, and fork a read-only workflow.

Run: uv run --extra agents python modules/14_langgraph/examples/07_time_travel.py --offline
Expected: Original standard quote stays available; fork uses expedited.
Cost: No model calls. Offline fixtures incur no API fee.
Requires: agents
"""

from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from common.errors import run_cli
from common.lesson import lesson_settings
from common.memory import thread_config
from common.pretty import print_text


class State(TypedDict):
    shipping: str
    quote: str


def quote(state: State) -> dict:
    return {
        "quote": "3-5 business days" if state["shipping"] == "standard" else "1-2 business days"
    }


def main() -> None:
    lesson_settings()
    builder = StateGraph(State)
    builder.add_node("quote", quote)
    builder.add_edge(START, "quote")
    builder.add_edge("quote", END)
    graph = builder.compile(checkpointer=InMemorySaver())
    config = thread_config("C001", "shipping")
    graph.invoke({"shipping": "standard", "quote": ""}, config)
    history = list(graph.get_state_history(config))
    before = next(snapshot for snapshot in history if snapshot.next == ("quote",))
    replay = graph.invoke(None, before.config)
    # KEY IDEA: update_state returns the fork config; it does not rewrite historical snapshots.
    fork = graph.update_state(before.config, {"shipping": "expedited"}, as_node="__start__")
    changed = graph.invoke(None, fork)
    print_text(
        str(
            {
                "replay": replay,
                "fork": changed,
                "original": graph.get_state(history[0].config).values,
            }
        )
    )


if __name__ == "__main__":
    run_cli(main)
