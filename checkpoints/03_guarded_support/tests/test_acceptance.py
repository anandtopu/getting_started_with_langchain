"""Actual interruption and write outcomes under explicitly scripted trajectories."""

import json
import runpy
from pathlib import Path

import pytest

from common.config import Settings

CHECKPOINT = Path(__file__).parents[1]
CASES = [json.loads(line) for line in (CHECKPOINT / "eval.jsonl").read_text().splitlines()]


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_guarded_case(case, request):
    for package in ("rank_bm25", "pypdf", "fastmcp"):
        pytest.importorskip(package, reason="Install agents extra for this checkpoint.")
    target = (
        "starter" if request.config.getoption("--exercise-target") == "exercises" else "solution"
    )
    run_case = runpy.run_path(str(CHECKPOINT / f"{target}.py"))["run_case"]
    result = run_case(case, Settings(course_offline=True))
    assert result["records"] == case["expected_records"]
    assert result["paused"] == case["expected_pause"]
    if result["paused"]:
        assert result["records_before_review"] == 0
    assert result["tool_results"]
