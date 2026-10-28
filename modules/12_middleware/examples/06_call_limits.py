"""Bound model calls and tool dispatch in a deliberately repeating agent.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/12_middleware/examples/06_call_limits.py --offline
Expected: The run ends with a visible limit message rather than looping.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from itertools import repeat

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.tools import make_order_tools


def main() -> None:
    settings = lesson_settings()
    for guard in [
        ModelCallLimitMiddleware(run_limit=2),
        ToolCallLimitMiddleware(run_limit=1, exit_behavior="end"),
    ]:
        model = get_chat_model(
            settings=settings, responses=repeat(tool_request("check_stock", {"sku": "BW-001"}))
        )
        # KEY IDEA: call counts constrain amplification; they do not measure exact spending.
        agent = create_agent(model, make_order_tools("C001"), middleware=[guard])
        result = agent.invoke(
            {"messages": [{"role": "user", "content": "Check BW-001 stock repeatedly."}]},
            {"recursion_limit": 20},
        )
        print_text(str(result["messages"][-1].content))


if __name__ == "__main__":
    run_cli(main)
