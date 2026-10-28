"""Behavioral targets: solutions pass; --exercise-target exercises checks learner edits."""

import runpy

import pytest

from common.config import ROOT


def test_01_practice(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/03_structured_output" / target / "01_practice.py"))[
        "validate"
    ]
    from pydantic import ValidationError

    from common.schemas import TicketTriage
    from common.triage import fixture_triage

    values = fixture_triage("Where is my shipment?")
    assert isinstance(fn(values), TicketTriage)
    with pytest.raises(ValidationError):
        fn({**values, "category": "unknown"})
    with pytest.raises(ValidationError):
        fn({**values, "order_id": "malformed"})


def test_02_apply(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/03_structured_output" / target / "02_apply.py"))[
        "accuracy"
    ]
    tickets = [
        {"ticket_id": "A", "labels": {"priority": "high"}},
        {"ticket_id": "B", "labels": {"priority": "low"}},
        {"ticket_id": "C", "labels": None},
    ]
    assert (
        fn([{"ticket_id": "B", "priority": "low"}, {"ticket_id": "A", "priority": "low"}], tickets)
        == 0.5
    )
    assert fn([], []) is None
    assert fn([], tickets) == 0


def test_03_stretch(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/03_structured_output" / target / "03_stretch.py"))[
        "repair"
    ]
    from pydantic import ValidationError

    from common.triage import fixture_triage

    valid = fixture_triage("Where is my shipment?")
    responses = iter([{**valid, "priority": "bad"}, valid])
    assert fn(lambda: next(responses)).category == "shipping"
    with pytest.raises(ValidationError):
        fn(lambda: {})
    with pytest.raises(PermissionError):
        fn(lambda: (_ for _ in ()).throw(PermissionError()))
