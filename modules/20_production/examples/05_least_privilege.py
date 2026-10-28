"""Validate SQL intent, deny private tables, and inspect bounded public output.

Run: uv run --extra apps python modules/20_production/examples/05_least_privilege.py --offline
Expected: One public product and three denied SQL requests.
Cost: No API calls; deterministic local checks. Requires: apps
"""

import sqlite3

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.security import public_query, scrub


def main() -> None:
    lesson_settings()
    result = public_query("SELECT sku,name,price_cents FROM products WHERE sku=?", ("BW-001",))
    assert all(set(row) == {"sku", "name", "price_cents"} for row in result)
    print_text(str(scrub(result)))
    for sql in ("DELETE FROM orders", "SELECT * FROM customers", "SELECT load_extension('x')"):
        try:
            # KEY IDEA: SELECT alone is insufficient; the authorizer denies private reads/functions.
            public_query(sql)
        except (ValueError, sqlite3.DatabaseError):
            print_text("Unsafe or private SQL denied.")


if __name__ == "__main__":
    run_cli(main)
