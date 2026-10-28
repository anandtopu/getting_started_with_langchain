"""Transfer ownership with Command and explicitly return to the supervisor.

Run: uv run --extra agents python modules/16_multi_agent/examples/02_handoffs.py --offline
Expected: Supervisor hands off to billing, then receives the read-only result.
Cost: At most three short specialist model calls. Offline fixtures incur no API fee.
Requires: agents
"""

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from common.errors import run_cli
from common.lesson import lesson_settings
from common.operations import run_specialist
from common.pretty import print_text


class State(TypedDict):
    owner: str
    report: dict


def main() -> None:
    settings = lesson_settings()

    def supervisor(state: State) -> Command[Literal["billing", "__end__"]]:
        return (
            Command(update={"owner": "supervisor"}, goto=END)
            if state["report"]
            else Command(update={"owner": "billing"}, goto="billing")
        )

    def billing(state: State) -> Command[Literal["supervisor"]]:
        report = run_specialist(settings, "C001", "billing", "BW1001", "BW-001")
        return Command(update={"owner": "supervisor", "report": report}, goto="supervisor")

    # KEY IDEA: ownership is explicit state; no separate static edge duplicates the handoff.
    graph = StateGraph(State)
    graph.add_node("supervisor", supervisor)
    graph.add_node("billing", billing)
    graph.add_edge(START, "supervisor")
    print_text(
        str(graph.compile().invoke({"owner": "supervisor", "report": {}}, {"recursion_limit": 5}))
    )


if __name__ == "__main__":
    run_cli(main)
