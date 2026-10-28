"""Run every lesson offline and assert the important contracts."""

import runpy

import pytest

from common.config import ROOT
from common.testing import execute_script

HERE = ROOT / "modules/02_prompt_templates"


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


def test_partial_and_literal_user_braces():
    prompt = load("01_variables")["product_prompt"]()
    assert set(prompt.input_variables) == {"product", "facts"}
    assert "{attack}" in prompt.invoke({"product": "Tent", "facts": "{attack}"}).to_string()
    with pytest.raises(KeyError, match="facts"):
        prompt.invoke({"product": "Tent"})


def test_history_is_explicit_not_memory():
    from langchain_core.messages import HumanMessage

    prompt = load("02_chat_history")["history_prompt"]()
    first = prompt.invoke({"history": [HumanMessage("Earlier")], "request": "Now"})
    second = prompt.invoke({"history": [], "request": "New"})
    assert len(first.messages) == 3 and len(second.messages) == 2
    with pytest.raises(ValueError, match="list"):
        prompt.invoke({"history": "not a list", "request": "Now"})


def test_few_shot_examples_precede_new_request():
    prompt = load("03_few_shot")["few_shot_prompt"]()
    messages = prompt.invoke({"rough": "Need tracking."}).messages
    assert [m.type for m in messages] == ["system", "human", "ai", "human", "ai", "human"]
    assert messages[-1].content == "Need tracking."
