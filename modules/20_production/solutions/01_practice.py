"""Persist a three-call session ceiling and reject invalid or excess reservations.

Run: uv run --extra apps python modules/20_production/solutions/01_practice.py --offline
Expected: a runnable reference behavior.
Cost: no API calls. Requires: apps
"""

from pathlib import Path

from common.budget import BudgetLedger
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def reserve_calls(path: Path, scope: str, calls: int) -> int:
    # KEY IDEA: enforce the contract at the trusted boundary.
    return BudgetLedger(path, session_limit=3).reserve(scope, calls)


def main() -> None:
    lesson_settings()
    print_text("Use target checks with a temporary ledger.")


if __name__ == "__main__":
    run_cli(main)
