"""Validate nested ticket data with Pydantic enums and nullable identifiers.

Run: uv run python modules/03_structured_output/examples/01_pydantic.py --offline
Expected: A TriageEnvelope containing shipping, low, positive and identifiers.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from common.data import load_jsonl
from common.errors import run_cli
from common.fixtures import structured_fixture
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.schemas import TriageEnvelope
from common.triage import fixture_triage


def main() -> None:
    settings = lesson_settings()
    text = load_jsonl("support_tickets.jsonl")[0]["text"]
    fixture = structured_fixture(
        TriageEnvelope, {"triage": fixture_triage(text), "evidence": "Where is my shipment?"}
    )
    # KEY IDEA: Pydantic is a Python data validator; validation checks shape, not truth.
    structured = get_chat_model(settings=settings, responses=[fixture]).with_structured_output(
        TriageEnvelope
    )
    result = structured.invoke("Extract ticket fields and a short evidence quote: " + text)
    print_text(result.model_dump_json(indent=2))


if __name__ == "__main__":
    run_cli(main)
