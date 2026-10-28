"""Validated worker plan: Produce one Send per unique allowlisted category; reject empty,
repeated or unknown work.

Run: uv run --extra agents python modules/15_workflows/exercises/03_stretch.py --offline
Expected: Runnable baseline; complete YOUR CODE HERE to pass target tests.
Cost: No model calls. Requires: agents
"""

from langgraph.types import Send

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def dispatch(categories: list[str], allowed: set[str]) -> list[Send]:
    # YOUR CODE HERE: Produce one Send per unique allowlisted category; reject empty, repeated
    # or unknown work.
    return []


def main() -> None:
    lesson_settings()
    print_text(str(dispatch(["tents"], {"tents", "apparel"})))


if __name__ == "__main__":
    run_cli(main)
