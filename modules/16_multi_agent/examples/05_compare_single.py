"""Measure call count, approximate input tokens and latency for one versus two agents.

Run: uv run --extra agents python modules/16_multi_agent/examples/05_compare_single.py --offline
Expected: Both paths expose evidence; delegation adds model work without proving better quality.
Cost: At most nine short calls across both measured paths. Offline fixtures incur no API fee.
Requires: agents
"""

from time import perf_counter

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain.tools import tool
from langchain_core.callbacks import BaseCallbackHandler

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.operations import specialist, specialist_input
from common.pretty import print_text


class Meter(BaseCallbackHandler):
    def __init__(self) -> None:
        self.calls = 0
        self.characters = 0

    def on_chat_model_start(self, serialized: dict, messages: list, **kwargs: object) -> None:
        self.calls += 1
        self.characters += sum(len(str(m.content)) for batch in messages for m in batch)


def main() -> None:
    settings = lesson_settings()
    child = specialist(settings, "C001", "logistics", "BW1001", "BW-001")

    @tool
    def delegate(order_id: str) -> str:
        """Read shipment facts for the requested order through a specialist."""
        result = child.invoke(
            {
                "messages": [
                    {"role": "user", "content": specialist_input("logistics", order_id, "BW-001")}
                ]
            }
        )
        return str([m.content for m in result["messages"] if m.type == "tool"])

    supervisor = create_agent(
        get_chat_model(
            settings=settings,
            responses=[tool_request("delegate", {"order_id": "BW1001"}), "Evidence received."],
        ),
        [delegate],
        middleware=[
            ModelCallLimitMiddleware(run_limit=3, exit_behavior="end"),
            ToolCallLimitMiddleware(run_limit=1, exit_behavior="end"),
        ],
    )
    # Use a fresh child for each measurement: finite fixtures do not rewind themselves.
    for name, agent in [
        ("single", specialist(settings, "C001", "logistics", "BW1001", "BW-001")),
        ("delegated", supervisor),
    ]:
        meter = Meter()
        start = perf_counter()
        result = agent.invoke(
            {"messages": [{"role": "user", "content": "Check shipping BW1001"}]},
            {"callbacks": [meter], "recursion_limit": 30},
        )
        # KEY IDEA: character/4 is a rough proxy, not provider token billing or a quality score.
        print_text(
            str(
                {
                    "pattern": name,
                    "model_calls": meter.calls,
                    "input_token_proxy": (meter.characters + 3) // 4,
                    "elapsed_ms": round((perf_counter() - start) * 1000, 2),
                    "tool_results": sum(m.type == "tool" for m in result["messages"]),
                }
            )
        )


if __name__ == "__main__":
    run_cli(main)
