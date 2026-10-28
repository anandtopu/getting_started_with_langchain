"""Route validated intent with a visible fallback.

Run: uv run --extra agents python modules/15_workflows/examples/02_route.py --offline
Expected: Shipping selects logistics; an unknown request selects manual review.
Cost: No model calls; intent labels are explicit inputs. Offline fixtures incur no API fee.
Requires: agents
"""

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


class State(TypedDict):
    intent: str
    queue: str


def route(state: State) -> Literal["logistics", "billing", "fallback"]:
    return {"shipping": "logistics", "refund": "billing"}.get(state["intent"], "fallback")


def main() -> None:
    lesson_settings()
    graph = StateGraph(State)
    graph.add_node("logistics", lambda state: {"queue": "delivery desk"})
    graph.add_node("billing", lambda state: {"queue": "refund review"})
    graph.add_node("fallback", lambda state: {"queue": "manual clarification"})
    # KEY IDEA: an unknown label is not permission to pick a privileged branch.
    graph.add_conditional_edges(START, route)
    for node in ("logistics", "billing", "fallback"):
        graph.add_edge(node, END)
    workflow = graph.compile()
    for intent in ("shipping", "unknown"):
        print_text(str(workflow.invoke({"intent": intent, "queue": ""})))


if __name__ == "__main__":
    run_cli(main)
