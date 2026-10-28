"""Validate server response.

Task: Validate stock bounds and identity, then reject a response for a different requested SKU.

Run: uv run --extra agents python modules/13_mcp/exercises/03_stretch.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def validate_result(requested: str, values: dict) -> dict:
    # YOUR CODE HERE: Validate server response.
    return values


def main() -> None:
    lesson_settings()
    print_text(str(validate_result("BW-001", {"sku": "BW-001", "stock": 87, "name": "Ridge Tent"})))


if __name__ == "__main__":
    run_cli(main)
