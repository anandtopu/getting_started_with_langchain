"""Delegation budget: Charge parent plus every worker call against a nonnegative budget; reject
invalid inputs.

Run: uv run --extra agents python modules/17_deep_agents/exercises/03_stretch.py --offline
Expected: Runnable baseline; complete YOUR CODE HERE to pass target tests.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def within_budget(parent: int, workers: list[int], limit: int) -> bool:
    # YOUR CODE HERE: Charge parent plus every worker call against a nonnegative budget; reject
    # invalid inputs.
    return True


def main() -> None:
    lesson_settings()
    print_text(str(within_budget(3, [2, 1], 5)))


if __name__ == "__main__":
    run_cli(main)
