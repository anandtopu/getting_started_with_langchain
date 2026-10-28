"""Behavioral targets: solutions pass; --exercise-target exercises checks learner edits."""

import runpy

import pytest

from common.config import ROOT


def test_01_practice(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/04_lcel_runnables" / target / "01_practice.py"))[
        "pipeline"
    ]
    assert fn().invoke(" bw-002 ") == "BW-002"
    assert fn().batch(["bw-003", " BW-004 "]) == ["BW-003", "BW-004"]


def test_02_apply(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/04_lcel_runnables" / target / "02_apply.py"))[
        "pipeline"
    ]
    row = {"review_id": "V1", "text": "Good tent"}
    result = fn().invoke(row)
    assert result["review_id"] == "V1"
    assert result["analysis"] == {"characters": 9, "words": 2}
    assert row == {"review_id": "V1", "text": "Good tent"}


def test_03_stretch(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/04_lcel_runnables" / target / "03_stretch.py"))[
        "resilient"
    ]
    from langchain_core.runnables import RunnableLambda

    calls = []

    def fail(value):
        calls.append(value)
        raise TimeoutError()

    result = fn(RunnableLambda(fail), RunnableLambda(lambda _: "backup")).invoke("tent")
    assert result == "backup" and len(calls) == 2
    with pytest.raises(ValueError):
        fn(
            RunnableLambda(lambda _: (_ for _ in ()).throw(ValueError())),
            RunnableLambda(lambda _: "backup"),
        ).invoke("x")
