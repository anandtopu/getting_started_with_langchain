"""Learner targets; default runs solutions, --exercise-target exercises checks edited baselines."""

import runpy

import pytest

from common.config import ROOT


def test_01_practice(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/09_advanced_rag" / target / "01_practice.py"))[
        "combine"
    ]
    from langchain_core.documents import Document

    a, b = Document(id="a", page_content="A"), Document(id="b", page_content="B")
    result = fn([[a, a, b], [b, a]])
    assert len(result) == 2
    assert {d.id for d in result} == {"a", "b"}


def test_02_apply(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/09_advanced_rag" / target / "02_apply.py"))["expand"]
    from langchain_core.documents import Document

    parent = Document(id="p", page_content="Full evidence")
    child = Document(id="c", page_content="fragment", metadata={"parent_id": "p"})
    assert fn([child, child], [parent]) == [parent]
    with pytest.raises(ValueError):
        fn([child], [])


def test_03_stretch(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/09_advanced_rag" / target / "03_stretch.py"))[
        "hit_rate"
    ]
    assert fn([True, False, None]) == 0.5
    assert fn([None]) is None
    assert fn([]) is None
    assert fn([True, True]) == 1
