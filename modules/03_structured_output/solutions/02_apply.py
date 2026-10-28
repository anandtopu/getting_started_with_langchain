"""Measure extraction honestly.

Task: Compute exact-match accuracy on labelled tickets by ticket_id, ignoring unlabelled rows.
Return None for no labels.
Run: uv run python modules/03_structured_output/solutions/02_apply.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def accuracy(predictions: list[dict], tickets: list[dict]) -> float | None:
    indexed = {row["ticket_id"]: row for row in predictions}
    labelled = [row for row in tickets if row.get("labels")]
    if not labelled:
        return None
    correct = sum(
        all(
            indexed.get(row["ticket_id"], {}).get(key) == value
            for key, value in row["labels"].items()
        )
        for row in labelled
    )
    return correct / len(labelled)


def main() -> None:
    lesson_settings()
    print_text(str(accuracy([], [])))


if __name__ == "__main__":
    run_cli(main)
