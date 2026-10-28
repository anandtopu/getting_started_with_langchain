"""Run the reference solution against independently stored access/routing expectations."""

import json
import runpy
from importlib.util import find_spec
from pathlib import Path

import pytest

from common.config import Settings

ROOT = Path(__file__).parents[1]
CASES = [
    json.loads(line) for line in (ROOT / "eval.jsonl").read_text(encoding="utf-8").splitlines()
]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_contract(case):
    if find_spec("rank_bm25") is None:
        pytest.skip("Install agents extra for this checkpoint.")
    solution = runpy.run_path(str(ROOT / "solution.py"))
    result = solution["run_case"](case, Settings(course_offline=True))
    assert result["passed"]
    assert len(result["reports"]) == len(case["expected_roles"])
    for report in result["reports"]:
        assert report["evidence"]
        assert "messages" not in report and "customer_id" not in report
