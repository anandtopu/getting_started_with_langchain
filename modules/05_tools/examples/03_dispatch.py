"""Bind tools, inspect a model request and return its matching ToolMessage.

Run: uv run python modules/05_tools/examples/03_dispatch.py --offline
Expected: A stock request and a result with tool_call_id=call-1.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from common.agent import dispatch
from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message
from common.tools import make_order_tools


def main() -> None:
    settings = lesson_settings()
    tools = make_order_tools("C001")
    model = get_chat_model(
        settings=settings, responses=[tool_request("check_stock", {"sku": "BW-001"})]
    )
    reply = model.bind_tools(tools).invoke("Check stock for BW-001 using the stock tool.")
    print_message(reply)
    # KEY IDEA: binding does not execute Python. The allowlisted dispatcher does.
    for call in reply.tool_calls:
        print_message(dispatch(call, tools))


if __name__ == "__main__":
    run_cli(main)
