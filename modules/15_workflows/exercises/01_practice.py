"""Deterministic merge: Sort by category without mutating worker result lists.

Run: uv run --extra agents python modules/15_workflows/exercises/01_practice.py --offline
Expected: Runnable baseline; complete YOUR CODE HERE to pass target tests.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def merge(rows: list[dict]) -> list[dict]:
    # YOUR CODE HERE: Sort by category without mutating worker result lists.
    return rows


def main() -> None:
    lesson_settings()
    print_text(str(merge([{"category": "tents"}, {"category": "apparel"}])))


if __name__ == "__main__":
    run_cli(main)
