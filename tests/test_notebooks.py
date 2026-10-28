"""Regression: notebook checks must not dispatch into an unrelated global interpreter."""

import json
import subprocess
import sys

import pytest

from scripts import check_notebooks


def test_notebook_runner_pins_the_active_interpreter(tmp_path, monkeypatch):
    folder = tmp_path / "modules/lesson"
    folder.mkdir(parents=True)
    (folder / "notebook.ipynb").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(check_notebooks, "ROOT", tmp_path)
    commands = []

    def capture(command, **kwargs):
        commands.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(check_notebooks.subprocess, "run", capture)
    with pytest.raises(SystemExit) as stopped:
        check_notebooks.main()
    assert stopped.value.code == 0
    assert commands[0][0][:3] == [sys.executable, "-m", "nbconvert"]
    spec = json.loads(
        (tmp_path / ".runtime/notebooks/jupyter/kernels/brightwave-course/kernel.json").read_text(
            encoding="utf-8"
        )
    )
    assert spec["argv"][0] == sys.executable
    assert commands[0][1]["env"]["COURSE_OFFLINE"] == "true"
