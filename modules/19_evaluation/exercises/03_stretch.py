"""Require nonempty data, exact safe trajectories and every correctness contract.
Never average away access failure.

Run: uv run --extra agents python modules/19_evaluation/exercises/03_stretch.py --offline
Expected: a runnable baseline; target checks reveal missing behavior.
Cost: no API calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def release_ok(report: dict) -> bool:
    # YOUR CODE HERE: replace the runnable baseline.
    return bool(report["rows"])


def main() -> None:
    lesson_settings()
    print_text(str(release_ok({"rows": []})))


if __name__ == "__main__":
    run_cli(main)
