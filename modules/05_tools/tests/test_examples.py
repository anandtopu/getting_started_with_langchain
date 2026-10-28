"""Run every lesson offline and assert the important contracts."""

import runpy

import pytest

from common.config import ROOT
from common.testing import execute_script

HERE = ROOT / "modules/05_tools"


def load(name: str) -> dict:
    return runpy.run_path(str(HERE / "examples" / (name + ".py")))


@pytest.mark.parametrize("path", sorted((HERE / "examples").glob("*.py")), ids=lambda p: p.stem)
def test_example_runs(path):
    execute_script(path, ["--offline"])


@pytest.mark.parametrize(
    "path",
    sorted((HERE / "exercises").glob("*.py")) + sorted((HERE / "solutions").glob("*.py")),
    ids=lambda p: p.parent.name + "-" + p.stem,
)
def test_exercise_cli_runs(path):
    execute_script(path, ["--offline"])


def test_ownership_and_schema_before_sql():
    from pydantic import ValidationError

    from common.tools import make_order_tools

    owner, other = make_order_tools("C001"), make_order_tools("C002")
    assert owner[0].invoke({"order_id": "BW1001"})["status"] == "delivered"
    assert "error" in other[0].invoke({"order_id": "BW1001"})
    assert "error" in other[1].invoke({"order_id": "BW1001"})
    with pytest.raises(ValidationError):
        owner[0].invoke({"order_id": "BW1001' OR 1=1 --"})


def test_unknown_tool_and_bad_arguments_are_bounded_errors():
    from common.agent import dispatch
    from common.tools import make_order_tools

    tools = make_order_tools("C001")
    for name, args in [("shell", {"cmd": "read secrets"}), ("check_stock", {"sku": "bad"})]:
        result = dispatch({"name": name, "args": args, "id": "abc"}, tools)
        assert result.tool_call_id == "abc"
        assert "error" in result.content and "read secrets" not in result.content


def test_loop_stops_and_rejects_excess_before_execution():
    from itertools import repeat

    from common.agent import run_tool_loop
    from common.fixtures import tool_request
    from common.models import get_chat_model
    from common.tools import make_order_tools

    call = tool_request("check_stock", {"sku": "BW-001"})
    with pytest.raises(RuntimeError, match="Turn budget"):
        run_tool_loop(
            get_chat_model(responses=repeat(call)), make_order_tools("C001"), "stock", max_turns=2
        )
    with pytest.raises(RuntimeError, match="Tool-call budget"):
        run_tool_loop(
            get_chat_model(responses=repeat(call)),
            make_order_tools("C001"),
            "stock",
            max_tool_calls=1,
        )


def test_runtime_is_hidden_from_model_schema():
    tool = load("06_runtime")["session_summary"]
    assert "runtime" not in tool.tool_call_schema.model_json_schema().get("properties", {})
