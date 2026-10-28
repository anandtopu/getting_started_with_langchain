"""Observe all six middleware hook boundaries around an actual tool call.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/12_middleware/examples/01_hooks.py --offline
Expected: Hook names show node hooks and nested model/tool wrappers.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from langchain.agents import create_agent

from common.errors import run_cli
from common.fixtures import tool_request
from common.guardrails import HookLog
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.tools import make_order_tools


def main() -> None:
    settings = lesson_settings()
    log = HookLog()
    agent = create_agent(
        get_chat_model(
            settings=settings,
            responses=[tool_request("check_stock", {"sku": "BW-001"}), "Checked."],
        ),
        make_order_tools("C001"),
        middleware=[log],
    )
    # KEY IDEA: wrappers surround a call; node hooks run at agent/model boundaries.
    agent.invoke({"messages": [{"role": "user", "content": "Check BW-001 stock."}]})
    print_text(str(log.events))


if __name__ == "__main__":
    run_cli(main)
