"""Target checks for learner starters or supplied solutions."""

import runpy
from pathlib import Path

import pytest


def target(request, filename):
    folder = request.config.getoption("--exercise-target")
    return runpy.run_path(str(Path(__file__).parents[1] / folder / filename))


def test_exercise_1(request, tmp_path):
    f = target(request, "01_practice.py")["config"]
    assert (
        f("C001", "a")["configurable"]["thread_id"] != f("C002", "a")["configurable"]["thread_id"]
    )
    with pytest.raises(ValueError):
        f("", "a")


def test_exercise_2(request, tmp_path):
    from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

    from common.fixtures import tool_request

    f = target(request, "02_apply.py")["trim"]
    messages = [
        HumanMessage("Old context " * 200),
        AIMessage("Old reply"),
        HumanMessage("Check stock"),
        tool_request("check_stock", {"sku": "BW-001"}),
        ToolMessage(content="87", tool_call_id="call-1"),
    ]
    result = f(messages, 140)
    assert len(result) < len(messages) and result[0].content == "Check stock"
    assert any(getattr(m, "tool_calls", []) for m in result)
    assert result[-1].type == "tool"
    with pytest.raises(ValueError):
        f(messages, 0)


def test_exercise_3(request, tmp_path):
    from common.memory import Preferences

    f = target(request, "03_stretch.py")["save_and_reopen"]
    p = tmp_path / "prefs.db"
    assert f(p, "C001", "standard") == "standard"
    assert Preferences(p).get("C002") is None
    with pytest.raises(ValueError):
        f(p, "C001", "teleport")
