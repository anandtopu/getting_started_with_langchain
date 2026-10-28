"""Trim old turns while preserving tool-call/result pairs.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/11_memory/examples/03_trim.py --offline
Expected: Latest complete turn remains within an approximate token budget.
Cost: No model calls. Approximate token counts are not provider billing.
Requires: agents
"""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.memory import trim_history
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    messages = [
        SystemMessage("Use only Brightwave evidence."),
        HumanMessage("Old discussion. " * 100),
        AIMessage("Earlier reply."),
        HumanMessage("Check BW-001 stock."),
        tool_request("check_stock", {"sku": "BW-001"}),
        ToolMessage(content="87", tool_call_id="call-1"),
    ]
    # KEY IDEA: discard complete older turns rather than orphaning tool messages.
    trimmed = trim_history(messages, 160)
    print_text(str([(m.type, m.content) for m in trimmed]))


if __name__ == "__main__":
    run_cli(main)
