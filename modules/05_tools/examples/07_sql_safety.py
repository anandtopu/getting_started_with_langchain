"""Enforce ownership and reject SQL-shaped arguments through constrained tools.

Run: uv run python modules/05_tools/examples/07_sql_safety.py --offline
Expected: Owned order found, another customer denied, malformed ID rejected.
Cost: No model calls; all database connections are read-only.
"""

from common.agent import dispatch
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.tools import make_order_tools


def main() -> None:
    lesson_settings()
    tools = make_order_tools("C001")
    for order_id in ("BW1001", "BW1002", "BW1001' OR 1=1 --"):
        result = dispatch(
            {"name": "lookup_order", "args": {"order_id": order_id}, "id": "safe-1"}, tools
        )
        print_text(result.content)
    # KEY IDEA: SQL placeholders handle values; a separate customer predicate enforces scope.
    print_text("No arbitrary SQL, shell, filesystem or Python-execution tool is exposed.")


if __name__ == "__main__":
    run_cli(main)
