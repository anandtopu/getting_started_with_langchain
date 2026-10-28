"""Target checks for learner starters or supplied solutions."""

import runpy
from pathlib import Path

import pytest


def target(request, filename):
    folder = request.config.getoption("--exercise-target")
    return runpy.run_path(str(Path(__file__).parents[1] / folder / filename))


def test_exercise_1(request, tmp_path):
    f = target(request, "01_practice.py")["endpoint"]
    assert f("http://127.0.0.1:8765/mcp").endswith("/mcp")
    for bad in [
        "https://example.test/mcp",
        "http://user:pass@127.0.0.1:8765/mcp",
        "http://127.0.0.1:8765/mcp?token=x",
        "http://127.0.0.1:9999/mcp",
    ]:
        with pytest.raises(ValueError):
            f(bad)


def test_exercise_2(request, tmp_path):
    f = target(request, "02_apply.py")["allow_names"]
    assert f(["inventory_stock"]) == ["inventory_stock"]
    for bad in [[], ["inventory_stock", "shell"], ["inventory_stock", "inventory_stock"]]:
        with pytest.raises(ValueError):
            f(bad)


def test_exercise_3(request, tmp_path):
    f = target(request, "03_stretch.py")["validate_result"]
    v = {"sku": "BW-001", "stock": 87, "name": "Ridge Tent"}
    assert f("BW-001", v)["stock"] == 87
    with pytest.raises(ValueError):
        f("BW-002", v)
    with pytest.raises(ValueError):
        f("BW-001", {**v, "stock": -1})
