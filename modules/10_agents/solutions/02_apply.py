"""Scoped order lookup.

Task: Use parameterized SQL to return only an order owned by the trusted customer.

Run: uv run --extra agents python modules/10_agents/solutions/02_apply.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from common.data import orders_connection
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def lookup(customer: str, order_id: str) -> dict | None:
    # KEY IDEA: Scoped order lookup.
    with orders_connection() as db:
        row = db.execute(
            "SELECT order_id,status FROM orders WHERE order_id=? AND customer_id=?",
            (order_id, customer),
        ).fetchone()
    return dict(row) if row else None


def main() -> None:
    lesson_settings()
    print_text(str(lookup("C001", "BW1001")))


if __name__ == "__main__":
    run_cli(main)
