"""Match tool result IDs.

Task: Dispatch an allowlisted call and return its ToolMessage with the same id. Unknown names
must return an error.
Run: uv run python modules/05_tools/exercises/02_apply.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain_core.messages import ToolMessage

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def execute(call: dict, tools: list) -> ToolMessage:
    return ToolMessage(content="Call received; execution not yet enabled.", tool_call_id=call["id"])


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


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
