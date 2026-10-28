"""Scoped order lookup.

Task: Use parameterized SQL to return only an order owned by the trusted customer.

Run: uv run --extra agents python modules/10_agents/exercises/02_apply.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def lookup(customer: str, order_id: str) -> dict | None:
    # YOUR CODE HERE: Scoped order lookup.
    return None


def main() -> None:
    lesson_settings()
    print_text(str(lookup("C001", "BW1001")))


if __name__ == "__main__":
    run_cli(main)
