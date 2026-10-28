"""Delegation budget: Charge parent plus every worker call against a nonnegative budget; reject
invalid inputs.

Run: uv run --extra agents python modules/17_deep_agents/solutions/03_stretch.py --offline
Expected: Runnable reference result.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def within_budget(parent: int, workers: list[int], limit: int) -> bool:
    if min([parent, limit, *workers]) < 0:
        raise ValueError("Negative call count")
    return parent + sum(workers) <= limit


def main() -> None:
    lesson_settings()
    print_text(str(within_budget(3, [2, 1], 5)))


if __name__ == "__main__":
    run_cli(main)
