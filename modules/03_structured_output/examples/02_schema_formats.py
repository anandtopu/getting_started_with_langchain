"""Compare TypedDict and JSON Schema contracts with explicit local validation.

Run: uv run python modules/03_structured_output/examples/02_schema_formats.py --offline
Expected: Two parsed dictionaries; TypeAdapter validates the TypedDict result.
Cost: Two short hosted calls; offline/local no API fee.
"""

from pydantic import TypeAdapter
from typing_extensions import TypedDict

from common.errors import run_cli
from common.fixtures import structured_fixture
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


class ProductFact(TypedDict):
    """A product code and name copied from supplied facts."""

    sku: str
    name: str


SCHEMA = {
    "title": "ProductFactJSON",
    "description": "Extract a supplied product fact.",
    "type": "object",
    "properties": {"sku": {"type": "string"}, "name": {"type": "string"}},
    "required": ["sku", "name"],
    "additionalProperties": False,
}


def main() -> None:
    settings = lesson_settings()
    for schema in (ProductFact, SCHEMA):
        fixture = structured_fixture(schema, {"sku": "BW-001", "name": "Ridge Tent"})
        result = (
            get_chat_model(settings=settings, responses=[fixture])
            .with_structured_output(schema)
            .invoke("Extract: product code BW-001; product name Ridge Tent.")
        )
        # KEY IDEA: dict output is not a Pydantic instance; validate before business use.
        print_text(str(TypeAdapter(ProductFact).validate_python(result, strict=True)))


if __name__ == "__main__":
    run_cli(main)
