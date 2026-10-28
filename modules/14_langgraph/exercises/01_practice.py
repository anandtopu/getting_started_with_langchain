"""Review routing: Reject negative cents; route strictly over 10000 cents to review.

Run: uv run --extra agents python modules/14_langgraph/exercises/01_practice.py --offline
Expected: Runnable baseline; complete YOUR CODE HERE to pass target tests.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def route(cents: int) -> str:
    # YOUR CODE HERE: Reject negative cents; route strictly over 10000 cents to review.
    return "record"


def main() -> None:
    lesson_settings()
    print_text(route(12195))


if __name__ == "__main__":
    run_cli(main)
