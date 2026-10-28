"""Handle a tool error and stop an endless tool loop.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/10_agents/examples/05_errors_limits.py --offline
Expected: One recovered read error, then GraphRecursionError from a deliberate loop.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from itertools import count
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langgraph.errors import GraphRecursionError

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


@tool
def unavailable_stock(sku: str) -> dict:
    """Synthetic unavailable stock reader used to demonstrate bounded recovery."""
    raise TimeoutError("Synthetic stock timeout")


@wrap_tool_call
def safe_error(request: Any, handler: Any) -> Any:
    try:
        return handler(request)
    except TimeoutError:
        return ToolMessage(
            content="Stock unavailable; ask for manual review.",
            tool_call_id=request.tool_call["id"],
            status="error",
        )


def main() -> None:
    settings = lesson_settings()
    call = tool_request("unavailable_stock", {"sku": "BW-001"})
    for responses in [
        [call, "Stock unavailable; manual review needed."],
        (tool_request("unavailable_stock", {"sku": "BW-001"}, f"loop-{i}") for i in count()),
    ]:
        agent = create_agent(
            get_chat_model(settings=settings, responses=responses),
            [unavailable_stock],
            middleware=[safe_error],
        )
        # KEY IDEA: recursion_limit bounds graph steps; it is not a dollar or token budget.
        try:
            print_text(
                str(
                    agent.invoke(
                        {"messages": [{"role": "user", "content": "Check stock."}]},
                        {"recursion_limit": 6},
                    )["messages"][-1].content
                )
            )
        except GraphRecursionError:
            print_text("GraphRecursionError: loop stopped; investigate before raising the limit.")


if __name__ == "__main__":
    run_cli(main)
