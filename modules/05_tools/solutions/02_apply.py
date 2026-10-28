"""Match tool result IDs.

Task: Dispatch an allowlisted call and return its ToolMessage with the same id. Unknown names
must return an error.
Run: uv run python modules/05_tools/solutions/02_apply.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

import json

from langchain_core.messages import ToolMessage
from pydantic import ValidationError

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def execute(call: dict, tools: list) -> ToolMessage:
    selected = {tool.name: tool for tool in tools}.get(call["name"])
    result = {"error": "Unknown tool"}
    if selected is not None:
        try:
            result = selected.invoke(call["args"])
        except ValidationError:
            result = {"error": "Invalid arguments"}
    return ToolMessage(content=json.dumps(result), tool_call_id=call["id"], name=call["name"])


def main() -> None:
    lesson_settings()
    from common.tools import make_order_tools

    print_text(
        execute(
            {"name": "check_stock", "args": {"sku": "BW-001"}, "id": "c1"}, make_order_tools("C001")
        ).content
    )


if __name__ == "__main__":
    run_cli(main)
