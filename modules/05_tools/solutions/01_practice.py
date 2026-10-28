"""Validate tool inputs.

Task: Define a tool lookup with OrderInput args_schema that returns the supplied order_id. No
database access is needed.
Run: uv run python modules/05_tools/solutions/01_practice.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain.tools import tool

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.tools import OrderInput


@tool(args_schema=OrderInput)
def lookup(order_id: str) -> dict:
    """Echo a validated Brightwave order identifier."""
    return {"order_id": order_id}


def main() -> None:
    lesson_settings()
    print_text(str(lookup.invoke({"order_id": "BW1001"})))


if __name__ == "__main__":
    run_cli(main)
