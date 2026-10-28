"""Behavioral targets for learner solutions, with no external calls."""

import runpy
from pathlib import Path

import pytest


def target(request, filename):
    folder = request.config.getoption("--exercise-target")
    return runpy.run_path(str(Path(__file__).parents[1] / folder / filename))


def test_exercise_1(request, tmp_path):
    f = target(request, "01_practice.py")["encode_event"]
    assert f("text", {"text": "a\nb"}).endswith("\n\n")
    assert f("text", {"text": "a\nb"}).count("\n\n") == 1
    with pytest.raises(ValueError):
        f("invented", {})


def test_exercise_2(request, tmp_path):
    f = target(request, "02_apply.py")["owned_history"]
    from common.config import Settings
    from common.security import Principal
    from common.service import SupportService

    service = SupportService(tmp_path, Settings(course_offline=True))
    thread = service.new_thread(Principal("C001", "customer"))
    assert f(service, thread, "C001")["thread_id"] == thread
    with pytest.raises(PermissionError):
        f(service, thread, "C002")


def test_exercise_3(request, tmp_path):
    f = target(request, "03_stretch.py")["resume_review"]
    from common.returns import ReturnRequest
    from common.security import Principal
    from common.web import demo_app

    service = demo_app(tmp_path).state.service
    thread = service.new_thread(Principal("C001", "customer"))
    view = service.request_return(
        thread,
        Principal("C001", "customer"),
        ReturnRequest(
            order_id="BW1001", sku="BW-014", reason="unused", idempotency_key="exercise-" + thread
        ),
    )
    with pytest.raises(PermissionError):
        f(service, thread, "customer", "approve", view["interrupt_id"])
    with pytest.raises(ValueError):
        f(service, thread, "manager", "approve", "stale")
    assert not f(service, thread, "manager", "reject", view["interrupt_id"])["pending"]
