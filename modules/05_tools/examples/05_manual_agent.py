"""Write the model-tool-model loop by hand with strict limits.

Run: uv run python modules/05_tools/examples/05_manual_agent.py --offline
Expected: A stock tool result followed by a final fixture reply.
Cost: At most four model turns and eight tool calls; offline/local no API fee.
"""

from langchain_core.messages import HumanMessage

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
        settings=settings,
        responses=[
            tool_request("check_stock", {"sku": "BW-001"}),
            "The stock result is shown above; stock is not reserved.",
        ],
    )
    bound = model.bind_tools(tools)
    messages = [HumanMessage("Use the tool to check BW-001 stock.")]
    calls = 0
    for _ in range(4):
        reply = bound.invoke(messages)
        if reply.invalid_tool_calls:
            raise ValueError("Invalid tool response.")
        messages.append(reply)
        print_message(reply)
        if not reply.tool_calls:
            return
        calls += len(reply.tool_calls)
        if calls > 8:
            raise RuntimeError("Tool-call budget exhausted.")
        # KEY IDEA: each ToolMessage completes one pending model-requested call.
        for call in reply.tool_calls:
            result = dispatch(call, tools)
            messages.append(result)
            print_message(result)
    raise RuntimeError("Turn budget exhausted.")


if __name__ == "__main__":
    run_cli(main)
