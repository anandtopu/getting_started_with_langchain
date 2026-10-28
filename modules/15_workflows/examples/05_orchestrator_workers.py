"""Validate a model plan before dispatching bounded workers.

Run: uv run --extra agents python modules/15_workflows/examples/05_orchestrator_workers.py --offline
Expected: A real structured parser produces two allowed category assignments.
Cost: One short planning model call. Offline fixtures incur no API fee.
Requires: agents
"""

import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from pydantic import BaseModel, Field

from common.errors import run_cli
from common.fixtures import structured_fixture
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.workflows import category_facts, review_groups


class Plan(BaseModel):
    categories: list[str] = Field(min_length=1, max_length=3)


class State(TypedDict):
    categories: list[str]
    facts: Annotated[list[dict], operator.add]


def main() -> None:
    settings = lesson_settings()
    groups = review_groups()
    model = get_chat_model(
        settings=settings, responses=[structured_fixture(Plan, {"categories": list(groups)[:2]})]
    ).with_structured_output(Plan)

    def plan(state: State) -> dict:
        result = model.invoke(
            "Select up to three categories for a review audit: " + str(list(groups))
        )
        if (
            len(set(result.categories)) != len(result.categories)
            or set(result.categories) - groups.keys()
        ):
            raise ValueError("Planner returned duplicate or unknown work.")
        return {"categories": result.categories}

    def dispatch(state: State) -> list[Send]:
        return [Send("worker", {"category": category}) for category in state["categories"]]

    def worker(state: dict) -> dict:
        return {"facts": [category_facts(state["category"], groups[state["category"]])]}

    # KEY IDEA: the planner proposes a finite plan; validated code controls dispatch.
    graph = StateGraph(State)
    graph.add_node("plan", plan)
    graph.add_node("worker", worker)
    graph.add_edge(START, "plan")
    graph.add_conditional_edges("plan", dispatch, ["worker"])
    graph.add_edge("worker", END)
    result = graph.compile().invoke({"categories": [], "facts": []})
    print_text(str(sorted(result["facts"], key=lambda row: row["category"])))


if __name__ == "__main__":
    run_cli(main)
