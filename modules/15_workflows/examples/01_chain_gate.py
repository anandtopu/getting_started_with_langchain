"""Chain a draft and revision behind a code validation gate.

Run: uv run --extra agents python modules/15_workflows/examples/01_chain_gate.py --offline
Expected: A missing citation blocks publication; a revision supplies it.
Cost: At most two short model calls. Offline fixtures incur no API fee.
Requires: agents
"""

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


class State(TypedDict):
    draft: str
    published: bool


def main() -> None:
    settings = lesson_settings()
    model = get_chat_model(
        settings=settings,
        responses=[
            "Synthetic review: setup matters.",
            "Synthetic review: setup matters [data/reviews.csv].",
        ],
    )

    def draft(state: State) -> dict:
        return {
            "draft": str(model.invoke("Draft one cautious insight from synthetic reviews.").content)
        }

    def gate(state: State) -> Literal["publish", "revise"]:
        return "publish" if "data/reviews.csv" in state["draft"] else "revise"

    def revise(state: State) -> dict:
        return {
            "draft": str(
                model.invoke(
                    "Add source data/reviews.csv to this synthetic draft: " + state["draft"]
                ).content
            )
        }

    def publish(state: State) -> dict:
        # KEY IDEA: prompts request a citation; code refuses an uncited final draft.
        if "data/reviews.csv" not in state["draft"]:
            raise ValueError("Citation still missing after the single revision.")
        return {"published": True}

    graph = StateGraph(State)
    for name, node in [("draft", draft), ("revise", revise), ("publish", publish)]:
        graph.add_node(name, node)
    graph.add_edge(START, "draft")
    graph.add_conditional_edges("draft", gate)
    graph.add_edge("revise", "publish")
    graph.add_edge("publish", END)
    print_text(str(graph.compile().invoke({"draft": "", "published": False})))


if __name__ == "__main__":
    run_cli(main)
