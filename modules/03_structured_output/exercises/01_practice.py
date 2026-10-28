"""Validate the contract.

Task: Return a TicketTriage instance from a dictionary; reject unsupported categories and
malformed IDs.
Run: uv run python modules/03_structured_output/exercises/01_practice.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def validate(values: dict) -> dict:
    return dict(values)


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


def main() -> None:
    lesson_settings()
    from common.triage import fixture_triage

    print_text(str(validate(fixture_triage("Where is my shipment? No rush."))))


if __name__ == "__main__":
    run_cli(main)
