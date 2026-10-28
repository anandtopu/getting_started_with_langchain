"""Learner targets; default runs solutions, --exercise-target exercises checks edited baselines."""

import runpy

import pytest

from common.config import ROOT


def test_01_practice(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/06_loaders_splitters" / target / "01_practice.py"))[
        "page_document"
    ]
    doc = fn("Evidence", "handbook.pdf", 0)
    assert doc.metadata["page"] == 1
    assert doc.page_content == "Evidence"
    with pytest.raises(ValueError):
        fn("x", "handbook.pdf", -1)


def test_02_apply(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/06_loaders_splitters" / target / "02_apply.py"))[
        "split"
    ]
    from langchain_core.documents import Document

    docs = fn(
        [
            Document(
                page_content="Brightwave policy facts. " * 30,
                metadata={"source": "policy.md", "page": 2},
            )
        ]
    )
    assert len(docs) > 1
    assert all(
        len(d.page_content) <= 120 and d.metadata["page"] == 2 and d.metadata["parent_id"]
        for d in docs
    )


def test_03_stretch(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/06_loaders_splitters" / target / "03_stretch.py"))[
        "FAQDocuments"
    ]
    records = [{"question": "A", "answer": "B"}, {"question": "C", "answer": "D"}]
    docs = fn(records).load()
    assert len(docs) == 2
    assert [d.metadata["row"] for d in docs] == [1, 2]
    assert len({d.id for d in docs}) == 2
