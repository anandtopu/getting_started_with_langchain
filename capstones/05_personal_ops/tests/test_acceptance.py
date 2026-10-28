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
    state = result["result"]
    assert len(state["notes"]) == case["expected_notes"]
    assert len(state["tasks"]) == case["expected_tasks"]
    assert state["approved_by_host"] == case["approved"]
    assert {entry["operation"] for entry in state["audit"]} == {"notes_create", "tasks_create"}
