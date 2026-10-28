"""Persist a scoped preference with SQLite and reopen it.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/11_memory/examples/07_durable_preferences.py --offline
Expected: C001 shipping survives reopening; C002 has no preference.
Cost: No model calls or API fees.
Requires: agents
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from common.errors import run_cli
from common.lesson import lesson_settings
from common.memory import Preferences
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    with TemporaryDirectory() as folder:
        path = Path(folder) / "preferences.db"
        Preferences(path).put("C001", "standard")
        # KEY IDEA: this is an application repository, not a LangGraph store implementation.
        reopened = Preferences(path)
        print_text(str({"C001": reopened.get("C001"), "C002": reopened.get("C002")}))


if __name__ == "__main__":
    run_cli(main)
