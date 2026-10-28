"""Execute approval and rejection contracts and enforce quality release semantics."""

import runpy
from pathlib import Path

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("langgraph.checkpoint.sqlite")
from common.config import Settings
from common.support_evaluation import load_cases

ROOT = Path(__file__).parents[1]


@pytest.mark.parametrize("case", load_cases(ROOT / "eval.jsonl"), ids=lambda row: row["id"])
def test_case(case, request, tmp_path):
    name = (
        "starter.py"
        if request.config.getoption("--exercise-target") == "exercises"
        else "solution.py"
    )
    result = runpy.run_path(str(ROOT / name))["run_case"](case, tmp_path)
    assert result["passed"] and result["checks"]


def test_rehearsal_passes_engineering_and_answer_quality():
    report = runpy.run_path(str(ROOT / "solution.py"))["rehearse"](Settings(course_offline=True))
    assert report["engineering_passed"]
    assert report["quality"]["passed"] == 6
    assert report["release_allowed"]


@pytest.mark.parametrize("reject", [False, True])
def test_release_command_enforces_the_gate(tmp_path, monkeypatch, reject):
    from common import release
    from common.testing import execute_script

    monkeypatch.setenv("RUNTIME_DIR", str(tmp_path))
    if reject:
        monkeypatch.setattr(release, "evaluation_gate", lambda report: False)
        with pytest.raises(SystemExit) as stopped:
            execute_script(ROOT / "solution.py", ["--offline", "--release"])
        assert stopped.value.code == 1
    else:
        execute_script(ROOT / "solution.py", ["--offline", "--release"])
