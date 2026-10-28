"""Target checks for learner starters or supplied solutions."""

import runpy
from pathlib import Path

import pytest


def target(request, filename):
    folder = request.config.getoption("--exercise-target")
    return runpy.run_path(str(Path(__file__).parents[1] / folder / filename))


def test_exercise_1(request, tmp_path):
    f = target(request, "01_practice.py")["redact_email"]
    assert f("Contact demo@example.test.") == "Contact [REDACTED_EMAIL]."
    assert f("No email") == "No email"


def test_exercise_2(request, tmp_path):
    f = target(request, "02_apply.py")["review_decision"]
    assert f("reject") == {"decisions": [{"type": "reject"}]}
    assert f("approve")["decisions"][0]["type"] == "approve"
    for bad in ["edit", "respond", "automatic"]:
        with pytest.raises(ValueError):
            f(bad)


def test_exercise_3(request, tmp_path):
    f = target(request, "03_stretch.py")["retryable"]
    assert f(TimeoutError())
    assert not f(PermissionError()) and not f(ValueError())
