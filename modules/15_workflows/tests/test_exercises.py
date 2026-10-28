"""Check learner implementations or reference solutions against behavioral contracts."""

import runpy
from pathlib import Path

import pytest


def target(request, filename):
    folder = request.config.getoption("--exercise-target")
    return runpy.run_path(str(Path(__file__).parents[1] / folder / filename))


def test_exercise_1(request):
    f = target(request, "01_practice.py")["merge"]
    rows = [{"category": "tents"}, {"category": "apparel"}]
    assert [r["category"] for r in f(rows)] == ["apparel", "tents"]
    assert rows[0]["category"] == "tents"


def test_exercise_2(request):
    f = target(request, "02_apply.py")["should_retry"]
    assert f(False, 1, 2) and not f(False, 2, 2) and not f(True, 1, 2)
    with pytest.raises(ValueError):
        f(False, 0, 0)


def test_exercise_3(request):
    f = target(request, "03_stretch.py")["dispatch"]
    jobs = f(["tents"], {"tents"})
    assert jobs[0].node == "worker" and jobs[0].arg == {"category": "tents"}
    for categories in [[], ["tents", "tents"], ["unknown"]]:
        with pytest.raises(ValueError):
            f(categories, {"tents"})
