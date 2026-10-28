"""Check learner implementations or reference solutions against behavioral contracts."""

import runpy
from pathlib import Path

import pytest


def target(request, filename):
    folder = request.config.getoption("--exercise-target")
    return runpy.run_path(str(Path(__file__).parents[1] / folder / filename))


def test_exercise_1(request):
    f = target(request, "01_practice.py")["report_path"]
    assert f("/reports/trends.md") == "/reports/trends.md"
    for path in ["/reports/../.env", r"C:\secrets", "/sources/market_brief.md"]:
        with pytest.raises(ValueError):
            f(path)


def test_exercise_2(request):
    f = target(request, "02_apply.py")["citations"]
    assert f("Synthetic scope [/sources/market_brief.md]") == ["/sources/market_brief.md"]
    for text in ["No citation", "Synthetic [/sources/missing.md]"]:
        with pytest.raises(ValueError):
            f(text)


def test_exercise_3(request):
    f = target(request, "03_stretch.py")["within_budget"]
    assert f(2, [1, 1], 4) and not f(2, [2, 1], 4)
    with pytest.raises(ValueError):
        f(1, [-1], 4)
