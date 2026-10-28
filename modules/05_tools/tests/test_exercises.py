"""Behavioral targets: solutions pass; --exercise-target exercises checks learner edits."""

import runpy

import pytest

from common.config import ROOT


def test_01_practice(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/05_tools" / target / "01_practice.py"))["lookup"]
    from pydantic import ValidationError

    assert fn.invoke({"order_id": "BW1001"}) == {"order_id": "BW1001"}
    with pytest.raises(ValidationError):
        fn.invoke({"order_id": "arbitrary SQL"})


def test_02_apply(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/05_tools" / target / "02_apply.py"))["execute"]
    import json

    from common.tools import make_order_tools

    result = fn(
        {"name": "lookup_order", "args": {"order_id": "BW1002"}, "id": "x"},
        make_order_tools("C001"),
    )
    assert result.tool_call_id == "x"
    assert "error" in json.loads(result.content)
    unknown = fn({"name": "shell", "args": {}, "id": "y"}, [])
    assert "error" in json.loads(unknown.content)


def test_03_stretch(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/05_tools" / target / "03_stretch.py"))["answer"]
    from itertools import repeat

    from common.fixtures import tool_request
    from common.models import get_chat_model
    from common.tools import make_order_tools

    call = tool_request("check_stock", {"sku": "BW-001"})
    assert (
        fn(get_chat_model(responses=[call, "Done"]), make_order_tools("C001"), "Stock?") == "Done"
    )
    with pytest.raises(RuntimeError, match="budget"):
        fn(get_chat_model(responses=repeat(call)), make_order_tools("C001"), "Stock?")
