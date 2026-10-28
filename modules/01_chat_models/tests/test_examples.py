"""Run every lesson offline and assert the important contracts."""

import runpy

import pytest

from common.config import ROOT
from common.testing import execute_script

HERE = ROOT / "modules/01_chat_models"


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


def test_tool_result_matches_pending_call():
    messages = load("02_message_types")["example_history"]()
    assert messages[-1].tool_call_id == messages[-2].tool_calls[0]["id"]


def test_usage_missing_and_reasoning_subset():
    from common.config import Settings
    from common.pretty import estimate_cost

    settings = Settings(
        llm_provider="openai",
        llm_model="test-model",
        cost_model="test-model",
        cost_input_per_million=1,
        cost_output_per_million=2,
    )
    assert estimate_cost(None, settings) is None
    assert estimate_cost(
        {"input_tokens": 100, "output_tokens": 50, "output_token_details": {"reasoning": 20}},
        settings,
    ) == pytest.approx(0.0002)


def test_mock_http_protocol():
    import httpx

    with httpx.Client(
        transport=httpx.MockTransport(load("09_http_by_hand")["mock_chat"])
    ) as client:
        response = client.post("http://fixture.invalid/api/chat", json={"stream": False})
        assert response.json()["message"]["content"] == "Welcome to Brightwave."


def test_message_requires_matching_id():
    from langchain_core.messages import ToolMessage
    from pydantic import ValidationError

    with pytest.raises((ValidationError, KeyError)):
        ToolMessage(content="Stock is 12")


@pytest.mark.parametrize("provider", ["openai", "ollama"])
def test_http_lesson_both_wire_formats(provider, monkeypatch, capsys):
    monkeypatch.setenv("LLM_PROVIDER", provider)
    execute_script(HERE / "examples/09_http_by_hand.py", ["--offline"])
    assert "Raw HTTP: Welcome to Brightwave." in capsys.readouterr().out
