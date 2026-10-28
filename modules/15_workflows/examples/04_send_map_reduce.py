"""Create a dynamic worker per review category with Send.

Run: uv run --extra agents python modules/15_workflows/examples/04_send_map_reduce.py --offline
Expected: Six category groups are reduced in sorted order.
Cost: No model calls. Offline fixtures incur no API fee.
Requires: agents
"""

import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.workflows import category_facts, review_groups


class State(TypedDict):
    categories: list[str]
    facts: Annotated[list[dict], operator.add]
    report: str


class Work(TypedDict):
    category: str


def dispatch(state: State) -> list[Send]:
    if not state["categories"] or len(set(state["categories"])) != len(state["categories"]):
        raise ValueError("Use nonempty unique categories.")
    return [Send("analyze", {"category": category}) for category in state["categories"]]


def analyze(state: Work) -> dict:
    return {"facts": [category_facts(state["category"], review_groups()[state["category"]])]}


def main() -> None:
    lesson_settings()
    graph = StateGraph(State)
    graph.add_node("analyze", analyze)
    graph.add_node(
        "merge",
        lambda state: {"report": str(sorted(state["facts"], key=lambda row: row["category"]))},
    )
    # KEY IDEA: each Send contains only the worker's input; results enter a shared reducer.
    graph.add_conditional_edges(START, dispatch, ["analyze"])
    graph.add_edge("analyze", "merge")
    graph.add_edge("merge", END)
    print_text(
        str(
            graph.compile().invoke({"categories": list(review_groups()), "facts": [], "report": ""})
        )
    )


if __name__ == "__main__":
    run_cli(main)
