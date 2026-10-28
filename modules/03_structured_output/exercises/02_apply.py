"""Measure extraction honestly.

Task: Compute exact-match accuracy on labelled tickets by ticket_id, ignoring unlabelled rows.
Return None for no labels.
Run: uv run python modules/03_structured_output/exercises/02_apply.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def accuracy(predictions: list[dict], tickets: list[dict]) -> float | None:
    return None


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


def main() -> None:
    lesson_settings()
    print_text(str(accuracy([], [])))


if __name__ == "__main__":
    run_cli(main)
