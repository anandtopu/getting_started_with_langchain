"""Merge concurrent evidence and replace a corrected message by ID.

Run: uv run --extra agents python modules/14_langgraph/examples/02_reducers.py --offline
Expected: Two evidence records; one corrected message.
Cost: No model calls. Offline fixtures incur no API fee.
Requires: agents
"""

import operator
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.errors import InvalidUpdateError
from langgraph.graph import END, START, StateGraph, add_messages

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


class State(TypedDict):
    evidence: Annotated[list[str], operator.add]
    messages: Annotated[list[AnyMessage], add_messages]


class Unreduced(TypedDict):
    evidence: list[str]


def stock(state: State) -> dict:
    return {"evidence": ["BW-001 stock requires a fresh lookup"]}


def policy(state: State) -> dict:
    return {"evidence": ["Unused returns have a 30-day window"]}


def main() -> None:
    lesson_settings()
    broken = StateGraph(Unreduced)
    for name, node in [("stock", stock), ("policy", policy)]:
        broken.add_node(name, node, input_schema=Unreduced)
        broken.add_edge(START, name)
        broken.add_edge(name, END)
    try:
        broken.compile().invoke({"evidence": []})
    except InvalidUpdateError:
        print_text("Expected InvalidUpdateError: parallel evidence needs a reducer.")
    else:
        raise AssertionError("The unreduced parallel graph should reject concurrent writes.")
    graph = StateGraph(State)
    for name, node in [("stock", stock), ("policy", policy)]:
        graph.add_node(name, node)
        graph.add_edge(START, name)
        graph.add_edge(name, END)
    # KEY IDEA: list reducers collect parallel updates; sort when order matters.
    result = graph.compile().invoke({"evidence": [], "messages": []})
    messages = add_messages(
        [HumanMessage("Wrong order", id="request")], [HumanMessage("Order BW1001", id="request")]
    )
    print_text(str({"evidence": sorted(result["evidence"]), "messages": messages}))


if __name__ == "__main__":
    run_cli(main)
