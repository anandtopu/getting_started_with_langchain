"""Page-retrieval and evidence contracts for the handbook checkpoint."""

import json
import runpy

import pytest

pytest.importorskip("pypdf", reason="Install rag extra for Handbook Q&A.")
pytest.importorskip("rank_bm25", reason="Install rag extra for Handbook Q&A.")

from common.config import ROOT, Settings
from common.knowledge import LocalLoader

CASES = [
    json.loads(line)
    for line in (ROOT / "checkpoints/02_handbook_qa/eval.jsonl")
    .read_text(encoding="utf-8")
    .splitlines()
]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_handbook_answer(case, request):
    target = (
        "starter" if request.config.getoption("--exercise-target") == "exercises" else "solution"
    )
    answer = runpy.run_path(str(ROOT / f"checkpoints/02_handbook_qa/{target}.py"))[
        "answer_handbook"
    ]
    result = answer(case["question"], Settings(course_offline=True))
    if case["page"] is None:
        assert result["abstained"] and not result["citations"]
    else:
        assert case["page"] in result["retrieved_pages"]
        assert not result["abstained"] and result["citations"]
        pages = LocalLoader("handbook/employee_handbook.pdf").load()
        for citation in result["citations"]:
            assert citation["source"] == "handbook/employee_handbook.pdf"
            assert citation["quote"] in pages[citation["page"] - 1].page_content
