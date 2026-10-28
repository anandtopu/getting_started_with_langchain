"""Exercise parser/capability adapters and notebook/source parity without API requests."""

import hashlib
import json

import pytest

from common.config import ROOT, Settings
from common.fixtures import structured_fixture
from common.models import get_chat_model
from common.schemas import TicketTriage
from common.triage import fixture_triage


def test_structured_fixture_uses_real_validation_and_include_raw():
    invalid = {**fixture_triage("Where is my shipment?"), "priority": "invalid"}
    response = get_chat_model(responses=[structured_fixture(TicketTriage, invalid)])
    result = response.with_structured_output(TicketTriage, include_raw=True).invoke("ticket")
    assert result["parsed"] is None
    assert result["parsing_error"] is not None
    assert result["raw"].tool_calls[0]["args"]["priority"] == "invalid"


@pytest.mark.parametrize("provider", ["openai", "anthropic", "google_genai", "ollama"])
@pytest.mark.parametrize("method", ["json_schema", "function_calling"])
def test_real_adapters_construct_structured_binding(provider, method):
    settings = Settings(
        course_offline=False,
        llm_provider=provider,
        openai_api_key="test-not-real",
        anthropic_api_key="test-not-real",
        google_api_key="test-not-real",
    )
    runnable = get_chat_model(settings=settings).with_structured_output(TicketTriage, method=method)
    assert callable(runnable.invoke)  # Construction is not provider-side capability verification.


def test_notebooks_mirror_every_example_and_use_case():
    for notebook in (ROOT / "modules").glob("*/notebook.ipynb"):
        cells = json.loads(notebook.read_text(encoding="utf-8"))["cells"]
        expected = {
            p.relative_to(notebook.parent).as_posix()
            for folder in ("examples", "use_case")
            for p in (notebook.parent / folder).glob("*.py")
        }
        seen = set()
        for cell in cells:
            metadata = cell.get("metadata", {})
            if "brightwave_source" not in metadata:
                continue
            relative = metadata["brightwave_source"]
            source = (notebook.parent / relative).read_text(encoding="utf-8")
            assert metadata["source_sha256"] == hashlib.sha256(source.encode()).hexdigest()
            assert source.split('if __name__ == "__main__":')[0].strip() in "".join(cell["source"])
            assert not cell["outputs"] and cell["execution_count"] is None
            seen.add(relative)
        assert seen == expected
