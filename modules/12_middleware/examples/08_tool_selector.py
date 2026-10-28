"""Use a separate model to select relevant tools from a reviewed set.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/12_middleware/examples/08_tool_selector.py --offline
Expected: Only the reviewed stock tool is selected; selection adds model calls.
Cost: Two agent calls plus up to two selection calls in the scripted path.
Requires: agents
"""

from itertools import repeat

from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolSelectorMiddleware

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.tools import make_order_tools


def main() -> None:
    settings = lesson_settings()
    selector = get_chat_model(
        settings=settings,
        responses=repeat(tool_request("ToolSelectionResponse", {"tools": ["check_stock"]})),
    )
    model = get_chat_model(
        settings=settings,
        responses=[tool_request("check_stock", {"sku": "BW-001"}), "Checked stock."],
    )
    # KEY IDEA: relevance selection narrows schemas, but authorization still lives in tools.
    agent = create_agent(
        model,
        make_order_tools("C001"),
        middleware=[LLMToolSelectorMiddleware(model=selector, max_tools=1, max_retries=0)],
    )
    result = agent.invoke({"messages": [{"role": "user", "content": "Check stock for BW-001."}]})
    print_text(str([(m.type, m.content) for m in result["messages"]]))


if __name__ == "__main__":
    run_cli(main)
