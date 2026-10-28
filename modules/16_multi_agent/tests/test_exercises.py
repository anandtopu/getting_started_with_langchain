"""Check learner implementations or reference solutions against behavioral contracts."""

import runpy
from pathlib import Path

import pytest


def target(request, filename):
    folder = request.config.getoption("--exercise-target")
    return runpy.run_path(str(Path(__file__).parents[1] / folder / filename))


def test_exercise_1(request):
    f = target(request, "01_practice.py")["select"]
    assert f({"roles": ["billing"], "confidence": 0.7}) == ["billing"]
    assert f({"roles": ["billing"], "confidence": 0.69}) == []
    with pytest.raises(ValueError):
        f({"roles": ["admin"], "confidence": 1})


def test_exercise_2(request):
    f = target(request, "02_apply.py")["project"]
    assert f({"order_id": "BW1001", "email": "demo@example.test", "customer_id": "C001"}) == {
        "order_id": "BW1001"
    }


def test_exercise_3(request):
    f = target(request, "03_stretch.py")["shipment"]
    assert "error" in f("C002", "BW1001")
    assert f("C001", "BW1001")["order_id"] == "BW1001"
