"""Scoped read: Call the existing customer-scoped logistics tool and preserve access denials.

Run: uv run --extra agents python modules/16_multi_agent/exercises/03_stretch.py --offline
Expected: Runnable baseline; complete YOUR CODE HERE to pass target tests.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def shipment(customer: str, order: str) -> dict:
    # YOUR CODE HERE: Call the existing customer-scoped logistics tool and preserve access denials.
    return {"status": "unknown"}


def main() -> None:
    lesson_settings()
    print_text(str(shipment("C002", "BW1001")))


if __name__ == "__main__":
    run_cli(main)
