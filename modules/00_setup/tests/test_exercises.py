"""Behavioral targets: solutions pass; --exercise-target exercises checks learner edits."""

import runpy

import pytest

from common.config import ROOT


def test_01_practice(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/00_setup" / target / "01_practice.py"))["fits"]
    assert fn(80, 20, 100) is True
    assert fn(90, 20, 100) is False
    with pytest.raises(ValueError):
        fn(-1, 0, 100)


def test_02_apply(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/00_setup" / target / "02_apply.py"))["choose"]
    assert fn() == "model"
    assert fn(fixed=True) == "LCEL"
    assert fn(tools=True) == "agent"
    assert fn(durable=True, tools=True) == "LangGraph"


def test_03_stretch(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/00_setup" / target / "03_stretch.py"))["profile"]
    from common.config import Settings

    result = fn(Settings(llm_provider="ollama", openai_api_key="private-demo-value"))
    assert result["local"] is True
    assert result["model"]
    assert "private-demo-value" not in str(result)
