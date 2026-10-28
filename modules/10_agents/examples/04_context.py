"""Inject authenticated customer identity outside the tool schema.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/10_agents/examples/04_context.py --offline
Expected: BW1001 is visible only to C001; the schema has no customer_id.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from pathlib import Path

from langchain.agents import create_agent

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.returns import SupportContext, scoped_order


def main() -> None:
    settings = lesson_settings()
    print_text(str(scoped_order.tool_call_schema.model_json_schema()))
    for customer in ["C001", "C002"]:
        model = get_chat_model(
            settings=settings,
            responses=[
                tool_request("scoped_order", {"order_id": "BW1001"}),
                "Use only the returned order evidence.",
            ],
        )
        agent = create_agent(model, [scoped_order], context_schema=SupportContext)
        # KEY IDEA: context is supplied by trusted application code, not generated arguments.
        result = agent.invoke(
            {"messages": [{"role": "user", "content": "Look up BW1001."}]},
            context=SupportContext(customer, Path("unused-read-only")),
        )
        print_text(str([m.content for m in result["messages"] if m.type == "tool"]))


if __name__ == "__main__":
    run_cli(main)
