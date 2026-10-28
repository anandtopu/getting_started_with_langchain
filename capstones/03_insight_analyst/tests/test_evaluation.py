"""Run the independent evaluation set through the actual reference application."""

import json
import runpy
from pathlib import Path

import pytest

from common.config import Settings

ROOT = Path(__file__).parents[1]
CASES = [
    json.loads(line) for line in (ROOT / "eval.jsonl").read_text(encoding="utf-8").splitlines()
]


@pytest.mark.parametrize("case", CASES, ids=lambda item: item["id"])
def test_evaluation(case, tmp_path):
    result = runpy.run_path(str(ROOT / "solution.py"))["run_case"](
        case, Settings(course_offline=True), tmp_path
    )
    if ROOT.name == "02_support_copilot":
        assert result["metrics"]["http_completed"]
        assert result["metrics"]["trajectory_exact"] and result["metrics"]["ownership_contract"]
        assert result["passed"] == (case["id"] not in {"returns", "shipping"})
    else:
        assert result["passed"]
