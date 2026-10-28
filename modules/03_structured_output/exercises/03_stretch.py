"""Bound repair attempts.

Task: Validate model dictionaries, retry ValidationError at most twice, then surface the
error. Do not retry unrelated exceptions.
Run: uv run python modules/03_structured_output/exercises/03_stretch.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from collections.abc import Callable

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.schemas import TicketTriage


def repair(generate: Callable[[], dict]) -> TicketTriage:
    return TicketTriage.model_validate(generate())


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


def main() -> None:
    lesson_settings()
    from common.triage import fixture_triage

    print_text(str(repair(lambda: fixture_triage("No rush. Where is my shipment?"))))


if __name__ == "__main__":
    run_cli(main)
