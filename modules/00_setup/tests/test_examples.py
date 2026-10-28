"""Run every lesson offline and assert the important contracts."""

import runpy

import pytest

from common.config import ROOT
from common.testing import execute_script

HERE = ROOT / "modules/00_setup"


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


def test_context_budget():
    lesson = load("01_llm_basics")
    assert lesson["context_fits"](128, 128, 256)
    assert not lesson["context_fits"](129, 128, 256)
    with pytest.raises(ValueError, match="negative"):
        lesson["context_fits"](-1, 0, 10)


def test_choose_smallest_block():
    choose = load("02_ecosystem")["choose_block"]
    assert choose() == "model"
    assert choose(fixed_steps=True) == "LCEL"
    assert choose(tool_decisions=True) == "LangChain agent"
    assert choose(durable=True, tool_decisions=True) == "LangGraph"
