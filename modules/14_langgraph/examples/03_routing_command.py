"""Route once with a conditional edge, then update and route with Command.

Run: uv run --extra agents python modules/14_langgraph/examples/03_routing_command.py --offline
Expected: The refund takes the review path; status is review requested.
Cost: No model calls. Offline fixtures incur no API fee.
Requires: agents
"""

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


class State(TypedDict):
    cents: int
    status: str


def route(state: State) -> Literal["review", "finish"]:
    return "review" if state["cents"] > 10000 else "finish"


def review(state: State) -> Command[Literal["finish"]]:
    return Command(update={"status": "review requested"}, goto="finish")


def main() -> None:
    lesson_settings()
    graph = StateGraph(State)
    graph.add_node("review", review)
    graph.add_node("finish", lambda state: {})
    graph.add_conditional_edges(START, route)
    # KEY IDEA: Command is the review node's only outgoing route; no duplicate edge.
    graph.add_edge("finish", END)
    print_text(str(graph.compile().invoke({"cents": 12195, "status": "received"})))


if __name__ == "__main__":
    run_cli(main)
