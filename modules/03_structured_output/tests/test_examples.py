"""Run every lesson offline and assert the important contracts."""

import runpy

import pytest

from common.config import ROOT
from common.testing import execute_script

HERE = ROOT / "modules/03_structured_output"


def load(name: str) -> dict:
    return runpy.run_path(str(HERE / "examples" / (name + ".py")))


@pytest.mark.parametrize("path", sorted((HERE / "examples").glob("*.py")), ids=lambda p: p.stem)
def test_example_runs(path):
    execute_script(path, ["--offline"])


@pytest.mark.parametrize(
    "path",
    sorted((HERE / "exercises").glob("*.py")) + sorted((HERE / "solutions").glob("*.py")),
    ids=lambda p: p.parent.name + "-" + p.stem,
)
def test_exercise_cli_runs(path):
    execute_script(path, ["--offline"])


def test_validation_and_bounded_repair():
    from pydantic import ValidationError

    from common.fixtures import structured_fixture
    from common.models import get_chat_model
    from common.schemas import TicketTriage
    from common.triage import fixture_triage

    repair = load("04_validation_retry")["extract_with_repair"]
    values = fixture_triage("Where is my shipment? No rush.")
    bad = structured_fixture(TicketTriage, {**values, "priority": "impossible"})
    good = structured_fixture(TicketTriage, values)
    assert repair(get_chat_model(responses=[bad, good]), "ticket").priority == "low"
    with pytest.raises(ValidationError):
        repair(get_chat_model(responses=[bad, bad]), "ticket")


def test_optional_ids_and_enum_validation():
    from pydantic import ValidationError

    from common.schemas import TicketTriage
    from common.triage import fixture_triage

    values = fixture_triage("Please delete my preferences.")
    assert TicketTriage.model_validate(values).order_id is None
    with pytest.raises(ValidationError):
        TicketTriage.model_validate({**values, "category": "made-up"})


def test_parser_rejects_invalid_json():
    from langchain_core.exceptions import OutputParserException
    from langchain_core.output_parsers import PydanticOutputParser

    from common.schemas import TicketTriage

    with pytest.raises(OutputParserException):
        PydanticOutputParser(pydantic_object=TicketTriage).invoke("not JSON")
