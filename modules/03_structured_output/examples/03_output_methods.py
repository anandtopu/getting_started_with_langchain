"""Select provider-native JSON schema or a schema represented as a tool call.

Run: uv run python modules/03_structured_output/examples/03_output_methods.py --offline
Expected: Both methods parse the same supplied fixture; provider enforcement is not simulated.
Cost: Two hosted calls; model capability is required. See provider capabilities guide.
"""

from common.errors import run_cli
from common.fixtures import structured_fixture
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.schemas import TicketTriage
from common.triage import fixture_triage


def main() -> None:
    settings = lesson_settings()
    text = "Where is my shipment? Order BW1001, item BW-001. No rush."
    for method in ("json_schema", "function_calling"):
        fixture = structured_fixture(TicketTriage, fixture_triage(text))
        model = get_chat_model(settings=settings, responses=[fixture])
        # KEY IDEA: native constraints are provider-side; a tool schema describes arguments.
        result = model.with_structured_output(TicketTriage, method=method).invoke(text)
        print_text(f"{method}: {result.model_dump_json()}")
    if settings.course_offline:
        print_text(
            "Both fixtures used LangChain's tool parser; "
            "native provider enforcement was not tested."
        )


if __name__ == "__main__":
    run_cli(main)
