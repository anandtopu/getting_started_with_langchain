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
    answer = result["answer"]
    assert not answer["abstained"] and answer["citations"]
    assert all(word.lower() in answer["answer"].lower() for word in case["must_contain"])
    assert case["page"] in {citation["page"] for citation in answer["citations"]}
