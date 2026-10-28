"""Bounded evaluator loop: Stop if accepted or attempts reaches the positive limit; reject
negative attempts.

Run: uv run --extra agents python modules/15_workflows/solutions/02_apply.py --offline
Expected: Runnable reference result.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def should_retry(accepted: bool, attempts: int, limit: int) -> bool:
    if limit < 1 or attempts < 0:
        raise ValueError("Invalid budget")
    return not accepted and attempts < limit


def main() -> None:
    lesson_settings()
    print_text(str(should_retry(False, 2, 2)))


if __name__ == "__main__":
    run_cli(main)
