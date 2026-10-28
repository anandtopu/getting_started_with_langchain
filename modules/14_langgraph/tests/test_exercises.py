"""Check learner implementations or reference solutions against behavioral contracts."""

import runpy
from pathlib import Path

import pytest


def target(request, filename):
    folder = request.config.getoption("--exercise-target")
    return runpy.run_path(str(Path(__file__).parents[1] / folder / filename))


def test_exercise_1(request):
    f = target(request, "01_practice.py")["route"]
    assert f(10000) == "record" and f(10001) == "review"
    with pytest.raises(ValueError):
        f(-1)


def test_exercise_2(request):
    f = target(request, "02_apply.py")["build"]
    assert f().invoke({"attempts": 4})["attempts"] == 5


def test_exercise_3(request):
    f = target(request, "03_stretch.py")["resume"]
    assert f("reject").resume == "reject"
    with pytest.raises(ValueError):
        f("automatic")
