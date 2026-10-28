"""Expose a read-only logistics specialist as a supervisor tool.

Run: uv run --extra agents python modules/16_multi_agent/examples/01_supervisor_tools.py --offline
Expected: The supervisor delegates; the child performs one scoped SQL tool call.
Cost: At most six short calls across supervisor and child. Offline fixtures incur no API fee.
Requires: agents
"""

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain.tools import tool

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.operations import run_specialist
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()

    @tool
    def ask_logistics(order_id: str) -> dict:
        """Ask logistics for a read-only shipment report for this authenticated customer."""
        return run_specialist(settings, "C001", "logistics", order_id, "BW-001")

    model = get_chat_model(
        settings=settings,
        responses=[
            tool_request("ask_logistics", {"order_id": "BW1001"}),
            "Logistics evidence attached.",
        ],
    )
    # KEY IDEA: only the wrapper knows the customer; neither supervisor nor child chooses it.
    supervisor = create_agent(
        model,
        [ask_logistics],
        middleware=[
            ModelCallLimitMiddleware(run_limit=3, exit_behavior="end"),
            ToolCallLimitMiddleware(run_limit=1, exit_behavior="end"),
        ],
    )
    state = supervisor.invoke(
        {"messages": [{"role": "user", "content": "Where is order BW1001?"}]},
        {"recursion_limit": 30},
    )
    print_text(str([m.content for m in state["messages"] if m.type == "tool"]))


if __name__ == "__main__":
    run_cli(main)
