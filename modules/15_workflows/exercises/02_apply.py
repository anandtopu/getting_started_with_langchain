"""Bounded evaluator loop: Stop if accepted or attempts reaches the positive limit; reject
negative attempts.

Run: uv run --extra agents python modules/15_workflows/exercises/02_apply.py --offline
Expected: Runnable baseline; complete YOUR CODE HERE to pass target tests.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def should_retry(accepted: bool, attempts: int, limit: int) -> bool:
    # YOUR CODE HERE: Stop if accepted or attempts reaches the positive limit; reject negative
    # attempts.
    return True


def main() -> None:
    lesson_settings()
    print_text(str(should_retry(False, 2, 2)))


if __name__ == "__main__":
    run_cli(main)
