"""Golden protocol/ownership checks; fake metrics are never semantic model accuracy."""

import json
import runpy

import pytest

from common.config import ROOT, Settings
from common.data import data_path

CASES = [
    json.loads(line)
    for line in (ROOT / "checkpoints/01_ticket_desk/eval.jsonl").read_text().splitlines()
]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_ticket_desk(case, request):
    target = (
        "starter" if request.config.getoption("--exercise-target") == "exercises" else "solution"
    )
    process = runpy.run_path(str(ROOT / f"checkpoints/01_ticket_desk/{target}.py"))[
        "process_ticket"
    ]
    before = data_path("orders.db").read_bytes()
    result = process(
        {"ticket_id": case["id"], "text": case["text"]},
        case["customer_id"],
        Settings(course_offline=True),
    )
    assert result["mode"] == "fixture"
    assert result["triage"]["category"] == case["expected_category"]
    assert [call["name"] for call in result["tool_calls"]] == case["expected_tools"]
    assert [call["id"] for call in result["tool_calls"]] == [
        r["call_id"] for r in result["tool_results"]
    ]
    if case["expected_tools"]:
        assert all(("error" in row["result"]) == case["denied"] for row in result["tool_results"])
    assert result["draft"] and result["sent"] is False
    assert data_path("orders.db").read_bytes() == before
