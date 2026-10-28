"""Durable preference.

Task: Write a customer preference, reopen the SQLite repository, and return only that customer
value.

Run: uv run --extra agents python modules/11_memory/solutions/03_stretch.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from common.errors import run_cli
from common.lesson import lesson_settings
from common.memory import Preferences
from common.pretty import print_text


def save_and_reopen(path: Path, customer: str, shipping: str) -> str | None:
    # KEY IDEA: Durable preference.
    Preferences(path).put(customer, shipping)
    return Preferences(path).get(customer)


def main() -> None:
    lesson_settings()
    with TemporaryDirectory() as folder:
        print_text(str(save_and_reopen(Path(folder) / "prefs.db", "C001", "standard")))


if __name__ == "__main__":
    run_cli(main)
