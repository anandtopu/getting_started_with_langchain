"""Use the public-only authorized SQL connection and keep private tables inaccessible.

Run: uv run --extra apps python modules/20_production/solutions/02_apply.py --offline
Expected: a runnable reference behavior.
Cost: no API calls. Requires: apps
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.security import public_query


def catalogue(sql: str) -> list[dict]:
    # KEY IDEA: enforce the contract at the trusted boundary.
    return public_query(sql)


def main() -> None:
    lesson_settings()
    print_text(str(catalogue("SELECT sku FROM products LIMIT 1")))


if __name__ == "__main__":
    run_cli(main)
