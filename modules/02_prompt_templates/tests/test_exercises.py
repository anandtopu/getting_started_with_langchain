"""Behavioral targets: solutions pass; --exercise-target exercises checks learner edits."""

import runpy

from common.config import ROOT


def test_01_practice(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/02_prompt_templates" / target / "01_practice.py"))[
        "template"
    ]
    prompt = fn()
    assert set(prompt.input_variables) == {"product", "facts"}
    text = prompt.invoke({"product": "Tent", "facts": "{literal} capacity 2"}).to_string()
    assert "Brightwave" in text and "{literal} capacity 2" in text


def test_02_apply(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/02_prompt_templates" / target / "02_apply.py"))[
        "template"
    ]
    from langchain_core.messages import AIMessage, HumanMessage

    history = [HumanMessage("Tent?"), AIMessage("Capacity?")]
    result = fn().invoke({"history": history, "request": "Two"})
    assert [m.type for m in result.messages] == ["system", "human", "ai", "human"]
    assert result.messages[-1].content == "Two"


def test_03_stretch(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/02_prompt_templates" / target / "03_stretch.py"))[
        "template"
    ]
    result = fn().invoke({"rough": "Need tracking."})
    assert [m.type for m in result.messages] == ["system", "human", "ai", "human"]
    assert "receipt" in result.messages[2].content
    assert result.messages[-1].content == "Need tracking."
