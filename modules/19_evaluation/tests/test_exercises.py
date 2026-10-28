"""Behavioral targets for learner solutions, with no external calls."""

import runpy
from pathlib import Path


def target(request, filename):
    folder = request.config.getoption("--exercise-target")
    return runpy.run_path(str(Path(__file__).parents[1] / folder / filename))


def test_exercise_1(request, tmp_path):
    f = target(request, "01_practice.py")["trajectory_ok"]
    expected = [{"name": "lookup_order", "args": {"order_id": "BW1001"}}]
    assert f(expected, expected)
    assert not f([{"name": "lookup_order", "args": {"order_id": "BW1002"}}], expected)
    bad = [{"name": "send_email", "args": {}}]
    assert not f(bad, bad)


def test_exercise_2(request, tmp_path):
    f = target(request, "02_apply.py")["safe_payload"]
    source = {"contact": ["alex@example.test"], "password": "hidden"}
    result = f(source)
    assert result == {"contact": ["[EMAIL]"], "password": "[REDACTED]"}
    assert source["password"] == "hidden"


def test_exercise_3(request, tmp_path):
    f = target(request, "03_stretch.py")["release_ok"]
    good = {
        "metrics": {
            "ownership_contract": True,
            "trajectory_exact": True,
            "keyword_correctness_proxy": True,
            "tone_rule_proxy": True,
            "exact_evidence_support_proxy": True,
        }
    }
    assert f({"rows": [good]})
    assert not f({"rows": []})
    for key in good["metrics"]:
        row = {"metrics": {**good["metrics"], key: False}}
        assert not f({"rows": [good, row]})
