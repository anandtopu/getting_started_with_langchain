"""Compare tool names AND arguments; forbid unapproved side effects even if labels contain them.

Run: uv run --extra agents python modules/19_evaluation/exercises/01_practice.py --offline
Expected: a runnable baseline; target checks reveal missing behavior.
Cost: no API calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def trajectory_ok(actual: list[dict], expected: list[dict]) -> bool:
    # YOUR CODE HERE: replace the runnable baseline.
    return len(actual) == len(expected)


def main() -> None:
    lesson_settings()
    print_text(str(trajectory_ok([], [])))


if __name__ == "__main__":
    run_cli(main)
