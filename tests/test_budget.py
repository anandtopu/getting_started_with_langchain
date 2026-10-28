"""Nested policy calls reserve capacity, including requests that later fail or cancel."""

import sqlite3
from contextlib import closing

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("langgraph.checkpoint.sqlite")
pytest.importorskip("rank_bm25")
from fastapi.testclient import TestClient

from common.copilot import copilot_demo
from common.release import headers


def test_copilot_reserves_nested_call_budget_before_execution(tmp_path):
    app = copilot_demo(tmp_path)
    with TestClient(app) as client:
        thread = client.post("/threads", headers=headers()).json()["thread_id"]
        for _ in range(6):
            response = client.post(
                f"/threads/{thread}/messages", headers=headers(), json={"text": "Hello"}
            )
            assert "event: done" in response.text
        response = client.post(
            f"/threads/{thread}/messages", headers=headers(), json={"text": "Hello"}
        )
        assert "event: error" in response.text and "event: done" not in response.text
    with closing(sqlite3.connect(app.state.service.database)) as db:
        assert (
            db.execute("SELECT reserved FROM budgets WHERE scope=?", (thread,)).fetchone()[0] == 30
        )


def test_two_policy_tools_fit_reserved_budget(tmp_path, monkeypatch):
    from langchain_core.messages import AIMessage

    from common import rag, service

    real_factory = service.get_chat_model
    nested_calls = []

    def agent_factory(**kwargs):
        kwargs["responses"] = [
            AIMessage(
                content="",
                tool_calls=[
                    {"name": "search_policy", "args": {"query": query}, "id": str(i)}
                    for i, query in enumerate(["return window", "shipping costs"])
                ],
            ),
            "Please review the policy evidence.",
        ]
        return real_factory(**kwargs)

    def nested_factory(**kwargs):
        nested_calls.append(kwargs["settings"].model_max_retries)
        return real_factory(**kwargs)

    monkeypatch.setattr(service, "get_chat_model", agent_factory)
    monkeypatch.setattr(rag, "get_chat_model", nested_factory)
    app = copilot_demo(tmp_path)
    with TestClient(app) as client:
        thread = client.post("/threads", headers=headers()).json()["thread_id"]
        response = client.post(
            f"/threads/{thread}/messages", headers=headers(), json={"text": "Compare policies"}
        )
        assert "event: done" in response.text
    assert nested_calls == [0, 0]
    assert app.state.service.request_call_reservation == 3 + len(nested_calls)
