"""Validate the contract.

Task: Return a TicketTriage instance from a dictionary; reject unsupported categories and
malformed IDs.
Run: uv run python modules/03_structured_output/solutions/01_practice.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.schemas import TicketTriage


def validate(values: dict) -> TicketTriage:
    return TicketTriage.model_validate(values)


def main() -> None:
    lesson_settings()
    from common.triage import fixture_triage

    print_text(str(validate(fixture_triage("Where is my shipment? No rush."))))


if __name__ == "__main__":
    run_cli(main)
