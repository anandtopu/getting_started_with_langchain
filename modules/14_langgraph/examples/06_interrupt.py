"""Pause before a side effect and resume a human decision.

Run: uv run --extra agents python modules/14_langgraph/examples/06_interrupt.py --offline
Expected: Approve and reject take different branches; neither writes before review.
Cost: No model calls. Offline fixtures incur no API fee.
Requires: agents
"""

from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from common.errors import run_cli
from common.lesson import lesson_settings
from common.memory import thread_config
from common.pretty import print_text


class State(TypedDict):
    request: str
    decision: str


def review(state: State) -> dict:
    answer = interrupt({"request": state["request"], "choices": ["approve", "reject"]})
    if answer not in ("approve", "reject"):
        raise ValueError("Invalid review decision")
    return {"decision": answer}


def main() -> None:
    lesson_settings()
    builder = StateGraph(State)
    builder.add_node("review", review)
    builder.add_edge(START, "review")
    builder.add_edge("review", END)
    graph = builder.compile(checkpointer=InMemorySaver())
    for decision in ("approve", "reject"):
        config = thread_config("C001", decision)
        pause = graph.invoke({"request": "Review $121.95 refund", "decision": "pending"}, config)
        print_text(str(pause["__interrupt__"]))
        # KEY IDEA: only a trusted reviewer interface should construct the resume command.
        print_text(str(graph.invoke(Command(resume=decision), config)))


if __name__ == "__main__":
    run_cli(main)
