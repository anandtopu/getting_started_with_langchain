"""Inspect snapshots, deltas, model tokens and custom progress.

Run: uv run --extra agents python modules/14_langgraph/examples/09_stream_modes.py --offline
Expected: All four stream modes emit distinct kinds of events.
Cost: One short model call. Offline fixtures incur no API fee.
Requires: agents
"""

from typing import TypedDict

from langgraph.config import get_stream_writer
from langgraph.graph import END, START, StateGraph

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


class State(TypedDict):
    question: str
    answer: str


def main() -> None:
    settings = lesson_settings()
    model = get_chat_model(settings=settings)

    def draft(state: State) -> dict:
        get_stream_writer()({"stage": "drafting", "progress": 0})
        reply = model.invoke(state["question"])
        get_stream_writer()({"stage": "complete", "progress": 100})
        return {"answer": str(reply.content)}

    builder = StateGraph(State)
    builder.add_node("draft", draft)
    builder.add_edge(START, "draft")
    builder.add_edge("draft", END)
    # KEY IDEA: a mode list labels each event; progress is not model-generated text.
    for mode, event in builder.compile().stream(
        {"question": "Explain 30-day returns.", "answer": ""},
        stream_mode=["values", "updates", "messages", "custom"],
    ):
        print_text(f"{mode}: {event}")


if __name__ == "__main__":
    run_cli(main)
