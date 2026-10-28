"""Target checks for learner starters or supplied solutions."""

import runpy
from pathlib import Path

import pytest


def target(request, filename):
    folder = request.config.getoption("--exercise-target")
    return runpy.run_path(str(Path(__file__).parents[1] / folder / filename))


def test_exercise_1(request, tmp_path):
    f = target(request, "01_practice.py")["needs_approval"]
    assert not f(9999) and not f(10000) and f(10001)
    with pytest.raises(ValueError):
        f(-1)


def test_exercise_2(request, tmp_path):
    f = target(request, "02_apply.py")["lookup"]
    assert f("C001", "BW1001")["order_id"] == "BW1001"
    assert f("C002", "BW1001") is None
    assert f("C001", "BW1001' OR 1=1 --") is None


def test_exercise_3(request, tmp_path):
    f = target(request, "03_stretch.py")["parse_request"]
    v = {"order_id": "BW1008", "sku": "BW-021", "idempotency_key": "exercise-return"}
    assert f(v).sku == "BW-021"
    with pytest.raises(ValueError):
        f({**v, "manager_approved": True})
    with pytest.raises(ValueError):
        f({**v, "reason": "anything"})
