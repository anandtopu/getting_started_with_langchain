"""Scoped read: Call the existing customer-scoped logistics tool and preserve access denials.

Run: uv run --extra agents python modules/16_multi_agent/solutions/03_stretch.py --offline
Expected: Runnable reference result.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.tools import make_order_tools


def shipment(customer: str, order: str) -> dict:
    return make_order_tools(customer)[1].invoke({"order_id": order})


def main() -> None:
    lesson_settings()
    print_text(str(shipment("C002", "BW1001")))


if __name__ == "__main__":
    run_cli(main)
