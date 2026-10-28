"""Compare a fixed read with agent-driven tool selection.

Run: uv run --extra agents python modules/15_workflows/examples/07_choose_workflow.py --offline
Expected: Both get the same stock; the fixed read uses zero model calls.
Cost: At most three short agent model calls; fixed path has no model fee. Offline fixtures incur
no API fee.
Requires: agents
"""

from time import perf_counter

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.tools import make_order_tools


def main() -> None:
    settings = lesson_settings()
    stock = make_order_tools("C001")[2]
    start = perf_counter()
    fixed = stock.invoke({"sku": "BW-001"})
    fixed_ms = (perf_counter() - start) * 1000
    model = get_chat_model(
        settings=settings,
        responses=[tool_request("check_stock", {"sku": "BW-001"}), "Read complete."],
    )
    agent = create_agent(
        model, [stock], middleware=[ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")]
    )
    start = perf_counter()
    state = agent.invoke({"messages": [{"role": "user", "content": "Check BW-001 stock."}]})
    # KEY IDEA: compare observed work, not an invented claim that agents are more accurate.
    print_text(
        str(
            {
                "fixed_result": fixed,
                "fixed_ms": round(fixed_ms, 2),
                "agent_ms": round((perf_counter() - start) * 1000, 2),
                "agent_model_turns": sum(m.type == "ai" for m in state["messages"]),
                "agent_tool_results": [m.content for m in state["messages"] if m.type == "tool"],
            }
        )
    )


if __name__ == "__main__":
    run_cli(main)
