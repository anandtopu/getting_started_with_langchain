"""Replace the manual loop with the current agent factory.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/10_agents/examples/01_create_agent.py --offline
Expected: Human, assistant tool call, tool result, final assistant message.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from langchain.agents import create_agent

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message
from common.tools import make_order_tools


def main() -> None:
    settings = lesson_settings()
    model = get_chat_model(
        settings=settings,
        temperature=0,
        responses=[
            tool_request("check_stock", {"sku": "BW-001"}),
            "Stock checked; this is not a reservation.",
        ],
    )
    # KEY IDEA: create_agent owns the same model/tool loop you built in module 05.
    agent = create_agent(
        model,
        make_order_tools("C001"),
        system_prompt="Check Brightwave stock using tools. Never invent a reservation.",
    )
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Check stock for BW-001."}]},
        {"recursion_limit": 12},
    )
    for message in result["messages"]:
        print_message(message)


if __name__ == "__main__":
    run_cli(main)
