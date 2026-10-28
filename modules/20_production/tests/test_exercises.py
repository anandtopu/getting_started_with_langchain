"""Behavioral targets for learner solutions, with no external calls."""

import runpy
from pathlib import Path

import pytest


def target(request, filename):
    folder = request.config.getoption("--exercise-target")
    return runpy.run_path(str(Path(__file__).parents[1] / folder / filename))


def test_exercise_1(request, tmp_path):
    f = target(request, "01_practice.py")["reserve_calls"]
    path = tmp_path / "ledger.db"
    assert f(path, "session", 2) == 2
    assert f(path, "session", 1) == 3
    with pytest.raises(ValueError):
        f(path, "session", 1)
    with pytest.raises(ValueError):
        f(path, "other", 0)


def test_exercise_2(request, tmp_path):
    f = target(request, "02_apply.py")["catalogue"]
    import sqlite3

    assert f("SELECT sku FROM products LIMIT 1")[0]["sku"].startswith("BW-")
    with pytest.raises((ValueError, sqlite3.DatabaseError)):
        f("SELECT * FROM customers")
    with pytest.raises(ValueError):
        f("DELETE FROM products")


def test_exercise_3(request, tmp_path):
    f = target(request, "03_stretch.py")["safe_event"]
    import json

    value = json.loads(f("run-1", {"contact": "alex@example.test", "api_key": "hidden"}))
    assert value["correlation_id"] == "run-1"
    assert value["contact"] == "[EMAIL]" and value["api_key"] == "[REDACTED]"
    with pytest.raises(ValueError):
        f("bad\nid", {})
