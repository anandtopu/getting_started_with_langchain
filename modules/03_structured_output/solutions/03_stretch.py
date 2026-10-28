"""Bound repair attempts.

Task: Validate model dictionaries, retry ValidationError at most twice, then surface the
error. Do not retry unrelated exceptions.
Run: uv run python modules/03_structured_output/solutions/03_stretch.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from collections.abc import Callable

from pydantic import ValidationError

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.schemas import TicketTriage


def repair(generate: Callable[[], dict]) -> TicketTriage:
    for attempt in range(2):
        try:
            return TicketTriage.model_validate(generate())
        except ValidationError:
            if attempt == 1:
                raise
    raise RuntimeError("Repair exhausted")


def main() -> None:
    lesson_settings()
    from common.triage import fixture_triage

    print_text(str(repair(lambda: fixture_triage("No rush. Where is my shipment?"))))


if __name__ == "__main__":
    run_cli(main)
