"""Repair invalid structured data with a bounded, schema-aware retry.

Run: uv run python modules/03_structured_output/examples/04_validation_retry.py --offline
Expected: An invalid priority is rejected, then repaired on the second fixture response.
Cost: At most two calls in this demo; offline fixtures intentionally fail first.
"""

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from pydantic import ValidationError

from common.errors import run_cli
from common.fixtures import structured_fixture
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.schemas import TicketTriage
from common.triage import fixture_triage


def extract_with_repair(model: BaseChatModel, text: str, max_attempts: int = 2) -> TicketTriage:
    if not 1 <= max_attempts <= 3:
        raise ValueError("Use 1..3 attempts.")
    runnable = model.with_structured_output(TicketTriage)
    messages = [HumanMessage("Extract Brightwave ticket fields: " + text)]
    for attempt in range(max_attempts):
        try:
            result = runnable.invoke(messages)
            if result is None:
                raise ValueError("No structured result returned.")
            return result
        except ValidationError as error:
            if attempt + 1 == max_attempts:
                raise
            fields = sorted({str(item["loc"][0]) for item in error.errors()})
            # KEY IDEA: repair changes the prompt; a blind transport retry does not.
            messages.append(
                HumanMessage(
                    f"Your last extraction failed validation for {fields}. "
                    "Return the full schema; priority must be low, medium or high."
                )
            )
    raise RuntimeError("Repair attempts exhausted.")


def main() -> None:
    settings = lesson_settings()
    text = "Where is my shipment? No rush. Order BW1001, item BW-001."
    good = fixture_triage(text)
    bad = {**good, "priority": "yesterday"}
    model = get_chat_model(
        settings=settings,
        responses=[structured_fixture(TicketTriage, bad), structured_fixture(TicketTriage, good)],
    )
    print_text(extract_with_repair(model, text).model_dump_json())


if __name__ == "__main__":
    run_cli(main)
