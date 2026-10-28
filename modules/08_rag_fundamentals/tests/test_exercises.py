"""Learner targets; default runs solutions, --exercise-target exercises checks edited baselines."""

import runpy

import pytest

from common.config import ROOT


def test_01_practice(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/08_rag_fundamentals" / target / "01_practice.py"))[
        "context"
    ]
    from langchain_core.documents import Document

    text = fn(
        [Document(id="c1", page_content="Evidence", metadata={"source": "handbook.pdf", "page": 3})]
    )
    assert all(value in text for value in ["c1", "handbook.pdf", "3", "Evidence"])


def test_02_apply(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/08_rag_fundamentals" / target / "02_apply.py"))["cite"]
    from langchain_core.documents import Document

    docs = [Document(id="c1", page_content="30 days", metadata={"source": "policy.md", "page": 2})]
    assert fn("c1", "30 days", docs)["page"] == 2
    for key, quote in [("wrong", "30 days"), ("c1", "90 days"), ("c1", "")]:
        with pytest.raises(ValueError):
            fn(key, quote, docs)


def test_03_stretch(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/08_rag_fundamentals" / target / "03_stretch.py"))[
        "respond"
    ]
    from common.config import Settings
    from common.knowledge import LocalLoader
    from common.retrieval import LexicalRetriever

    retriever = LexicalRetriever(LocalLoader("policies/returns.md").load())
    result = fn("Refunds over $100 need what?", retriever, Settings(course_offline=True))
    assert not result["abstained"] and result["citations"]
    assert fn("unrelatedquasar", retriever, Settings(course_offline=True))["abstained"]
