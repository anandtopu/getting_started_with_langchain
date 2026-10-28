"""The learner target must perform a real accepted case, not return a canned pass flag."""

import json
import runpy
from pathlib import Path

from common.config import Settings

ROOT = Path(__file__).parents[1]


def test_learner_target(request, tmp_path):
    name = (
        "starter.py"
        if request.config.getoption("--exercise-target") == "exercises"
        else "solution.py"
    )
    case = json.loads((ROOT / "eval.jsonl").read_text(encoding="utf-8").splitlines()[0])
    result = runpy.run_path(str(ROOT / name))["run_case"](
        case, Settings(course_offline=True), tmp_path
    )
    assert result["passed"]
    assert result["accepted"] and result["attempts"] <= case["attempts"]
    assert "Source:" in result["report"] and "Synthetic" in result["report"]
    assert result["logical_calls"] <= 13
    assert (tmp_path / "report.md").read_text(encoding="utf-8") == result["report"]
