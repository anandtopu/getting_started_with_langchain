"""Flagship endpoints retain approval guards while adding policy retrieval and memory."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("rank_bm25")
from fastapi.testclient import TestClient

from common.copilot import copilot_demo
from common.release import api_contract, headers


@pytest.mark.parametrize("decision", ["approve", "reject"])
def test_review_contracts(tmp_path, decision):
    report = api_contract(tmp_path, decision, app_factory=copilot_demo)
    assert all(value for key, value in report.items() if key != "result")


def test_policy_tool_and_owned_memory(tmp_path):
    with TestClient(copilot_demo(tmp_path)) as client:
        thread = client.post("/threads", headers=headers()).json()["thread_id"]
        response = client.post(
            f"/threads/{thread}/messages",
            headers=headers(),
            json={"text": "What is the return window?"},
        )
        assert "event: done" in response.text
        history = client.get(f"/threads/{thread}", headers=headers()).json()["messages"]
        assert any(
            row["type"] == "tool" and row["data"]["name"] == "search_policy" for row in history
        )
        import json

        evidence = next(
            json.loads(row["data"]["content"])
            for row in history
            if row["type"] == "tool" and row["data"]["name"] == "search_policy"
        )
        assert evidence["citations"]
        assert all(f"[{item['source']}]" in response.text for item in evidence["citations"])
    reopened = copilot_demo(tmp_path)
    with TestClient(reopened) as client:
        assert client.get(f"/threads/{thread}", headers=headers()).json()["messages"] == history
