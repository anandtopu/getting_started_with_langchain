"""Reject malformed tool arguments before any database operation.

Run: uv run python modules/05_tools/examples/02_args_schema.py --offline
Expected: Invalid SKU rejected, followed by a valid stock result.
Cost: No model calls.
"""

from pydantic import ValidationError

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.tools import make_order_tools


def main() -> None:
    lesson_settings()
    stock = make_order_tools("C001")[2]
    try:
        stock.invoke({"sku": "not-a-sku"})
    except ValidationError:
        print_text("Invalid SKU rejected before SQL execution.")
    # KEY IDEA: validation is a boundary, not a guarantee the SKU exists.
    print_text(str(stock.invoke({"sku": "BW-001"})))


if __name__ == "__main__":
    run_cli(main)
