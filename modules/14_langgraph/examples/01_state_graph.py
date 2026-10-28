"""Compare two state schemas for the same return check.

Run: uv run --extra agents python modules/14_langgraph/examples/01_state_graph.py --offline
Expected: Both graphs route a 12,195-cent refund to review.
Cost: No model calls. Offline fixtures incur no API fee.
Requires: agents
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


class ReturnState(TypedDict):
    cents: int
    review: bool


class ValidatedState(BaseModel):
    cents: int = Field(ge=0)
    review: bool = False


def check_dict(state: ReturnState) -> dict:
    return {"review": state["cents"] > 10000}


def check_model(state: ValidatedState) -> dict:
    return {"review": state.cents > 10000}


def main() -> None:
    lesson_settings()
    for schema, node in [(ReturnState, check_dict), (ValidatedState, check_model)]:
        # KEY IDEA: a node returns a partial update, not a mutated shared dictionary.
        builder = StateGraph(schema)
        builder.add_node("check", node)
        builder.add_edge(START, "check")
        builder.add_edge("check", END)
        graph = builder.compile()
        print_text(str(graph.invoke({"cents": 12195, "review": False})))


if __name__ == "__main__":
    run_cli(main)
