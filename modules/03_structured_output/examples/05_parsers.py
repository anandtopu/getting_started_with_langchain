"""Parse text after generation when the model has no native schema interface.

Run: uv run python modules/03_structured_output/examples/05_parsers.py --offline
Expected: A plain string and a validated TicketTriage object.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

import json

from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.schemas import TicketTriage
from common.triage import fixture_triage


def main() -> None:
    settings = lesson_settings()
    text = "Where is my shipment? No rush."
    parser = PydanticOutputParser(pydantic_object=TicketTriage)
    model = get_chat_model(settings=settings, responses=[json.dumps(fixture_triage(text))])
    message = model.invoke(parser.get_format_instructions() + "\nTicket: " + text)
    # KEY IDEA: a parser validates after generation; it cannot force valid generation.
    print_text(StrOutputParser().invoke(message))
    print_text(parser.invoke(message).model_dump_json())


if __name__ == "__main__":
    run_cli(main)
