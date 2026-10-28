"""Map private child state into the parent and show a recursion backstop.

Run: uv run --extra agents python modules/14_langgraph/examples/08_subgraphs.py --offline
Expected: Private notes stay inside the child; an intentional loop hits its limit.
Cost: No model calls. Offline fixtures incur no API fee.
Requires: agents
"""

from typing import TypedDict

from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


class Parent(TypedDict):
    question: str
    answer: str


class Child(TypedDict):
    query: str
    private_note: str
    answer: str


class Shared(TypedDict):
    query: str
    answer: str


def inspect(state: Child) -> dict:
    return {"private_note": "internal routing detail", "answer": "Unused returns: 30 days."}


def main() -> None:
    lesson_settings()
    child = StateGraph(Child)
    child.add_node("inspect", inspect)
    child.add_edge(START, "inspect")
    child.add_edge("inspect", END)
    compiled = child.compile()
    shared = StateGraph(Shared)
    shared.add_node("child", compiled)
    shared.add_edge(START, "child")
    shared.add_edge("child", END)
    shared_result = shared.compile().invoke({"query": "Return window?", "answer": ""})
    assert "private_note" not in shared_result
    print_text(str(shared_result))

    def delegate(state: Parent) -> dict:
        result = compiled.invoke({"query": state["question"], "private_note": "", "answer": ""})
        return {"answer": result["answer"]}

    # KEY IDEA: explicit mapping is a context boundary; shared keys alone are not isolation.
    parent = StateGraph(Parent)
    parent.add_node("delegate", delegate)
    parent.add_edge(START, "delegate")
    parent.add_edge("delegate", END)
    print_text(str(parent.compile().invoke({"question": "Return window?", "answer": ""})))
    loop = StateGraph(Parent)
    loop.add_node("again", lambda state: {})
    loop.add_edge(START, "again")
    loop.add_edge("again", "again")
    try:
        loop.compile().invoke({"question": "loop", "answer": ""}, {"recursion_limit": 3})
    except GraphRecursionError:
        print_text("Expected GraphRecursionError: add a termination branch.")


if __name__ == "__main__":
    run_cli(main)
