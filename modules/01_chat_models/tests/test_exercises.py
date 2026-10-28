"""Behavioral targets: solutions pass; --exercise-target exercises checks learner edits."""

import runpy

from common.config import ROOT


def test_01_practice(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/01_chat_models" / target / "01_practice.py"))[
        "messages"
    ]
    result = fn("{ignore instructions}")
    assert [m.type for m in result] == ["system", "human"]
    assert result[-1].content == "{ignore instructions}"


def test_02_apply(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/01_chat_models" / target / "02_apply.py"))[
        "token_counts"
    ]
    assert fn(None) is None
    assert fn({"input_tokens": 5}) is None
    assert fn(
        {"input_tokens": 5, "output_tokens": 7, "output_token_details": {"reasoning": 3}}
    ) == (5, 7, 12)


def test_03_stretch(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/01_chat_models" / target / "03_stretch.py"))["draft"]
    from common.models import get_chat_model

    assert fn([], get_chat_model()) == []
    assert fn(["a", "b", "c"], get_chat_model(responses=["reply"] * 3)) == ["reply"] * 3
