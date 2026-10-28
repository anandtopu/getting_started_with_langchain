"""Validate tool inputs.

Task: Define a tool lookup with OrderInput args_schema that returns the supplied order_id. No
database access is needed.
Run: uv run python modules/05_tools/exercises/01_practice.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain.tools import tool

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


@tool
def lookup(order_id: str) -> dict:
    """Echo a Brightwave order identifier."""
    return {"order_id": order_id}


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


def main() -> None:
    lesson_settings()
    print_text(str(lookup.invoke({"order_id": "BW1001"})))


if __name__ == "__main__":
    run_cli(main)
