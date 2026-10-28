"""Real HTTP/UI contracts with scripted models and network denied."""

import asyncio
import json
import sqlite3
from contextlib import closing

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("streamlit")
pytest.importorskip("langgraph.checkpoint.sqlite")

from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest

from common.config import Settings
from common.release import CUSTOMER, OTHER, REVIEWER, api_contract, headers
from common.security import Principal
from common.service import SupportService
from common.web import configured_app, demo_app, sse


def pending(client):
    thread = client.post("/threads", headers=headers()).json()["thread_id"]
    result = client.post(
        f"/threads/{thread}/returns",
        headers=headers(),
        json={
            "order_id": "BW1001",
            "sku": "BW-014",
            "reason": "unused",
            "idempotency_key": "web-test-" + thread,
        },
    )
    assert result.status_code == 200
    return thread, result.json()


@pytest.mark.parametrize("decision", ["approve", "reject"])
def test_http_contract(tmp_path, decision):
    report = api_contract(tmp_path, decision)
    assert all(value for key, value in report.items() if key != "result")
    with closing(sqlite3.connect(tmp_path / "orders.db")) as db:
        count = db.execute("SELECT COUNT(*) FROM returns WHERE return_id LIKE 'R-%'").fetchone()[0]
    assert count == (1 if decision == "approve" else 0)


@pytest.mark.parametrize("change", ["warehouse", "amount"])
def test_approval_rechecks_trusted_facts(tmp_path, change):
    app = demo_app(tmp_path)
    with TestClient(app) as client:
        thread, view = pending(client)
        if change == "warehouse":
            app.state.service.attest("BW1001", "BW-014", inspected=False, proof=False)
        else:
            with closing(sqlite3.connect(app.state.service.orders)) as db, db:
                db.execute(
                    "UPDATE order_items SET unit_price_cents=unit_price_cents+100 "
                    "WHERE order_id='BW1001' AND sku='BW-014'"
                )
        response = client.post(
            f"/reviews/{thread}",
            headers=headers(REVIEWER),
            json={
                "decision": "approve",
                "interrupt_id": view["interrupt_id"],
            },
        )
        assert response.status_code == 200
        assert response.json()["result"] is None
        assert "recorded" not in response.json()["status"]
        with closing(sqlite3.connect(app.state.service.orders)) as db:
            assert (
                db.execute("SELECT COUNT(*) FROM returns WHERE return_id LIKE 'R-%'").fetchone()[0]
                == 0
            )


def test_stale_resume_and_untrusted_fields(tmp_path):
    with TestClient(demo_app(tmp_path)) as client:
        thread, view = pending(client)
        assert view["pending"]
        assert (
            client.post(
                f"/reviews/{thread}",
                headers=headers(REVIEWER),
                json={
                    "decision": "approve",
                    "interrupt_id": "stale",
                },
            ).status_code
            == 409
        )
        assert (
            client.post(
                f"/threads/{thread}/messages",
                headers=headers(),
                json={
                    "text": "Hello",
                    "customer_id": "C002",
                },
            ).status_code
            == 422
        )
        assert client.get(f"/reviews/{thread}", headers=headers(OTHER)).status_code == 403


def test_chat_persists_redacted_history_and_hides_tool_output(tmp_path):
    with TestClient(demo_app(tmp_path)) as client:
        thread = client.post("/threads", headers=headers()).json()["thread_id"]
        result = client.post(
            f"/threads/{thread}/messages",
            headers=headers(),
            json={
                "text": "BW1001 contact alex@example.test 4111 1111 1111 1111",
            },
        )
        assert "event: done" in result.text and "event: error" not in result.text
        assert "total_cents" not in result.text
        history = client.get(f"/threads/{thread}", headers=headers()).text
        assert "[EMAIL]" in history and "[CARD]" in history
        assert "alex@example.test" not in history
    reopened = SupportService(tmp_path, Settings(course_offline=True))
    assert len(reopened.session(thread, Principal("C001", "customer"))["messages"]) == 4


@pytest.mark.parametrize("mode", ["failure", "timeout"])
def test_stream_error_releases_admission_and_hides_exception(tmp_path, monkeypatch, mode):
    app = demo_app(tmp_path)
    app.state.service.settings.api_request_timeout = 0.01

    async def broken(*args):
        if mode == "timeout":
            await asyncio.sleep(10)
        raise RuntimeError("private@example.test secret payload")
        yield  # unreachable: preserves the async-generator protocol

    monkeypatch.setattr(app.state.service, "chat", broken)
    with TestClient(app) as client:
        thread = client.post("/threads", headers=headers()).json()["thread_id"]
        result = client.post(f"/threads/{thread}/messages", headers=headers(), json={"text": "Hi"})
        assert "event: error" in result.text and "event: done" not in result.text
        assert "private@example.test" not in result.text + str(app.state.events)
        assert not app.state.service.admission.active


def test_sse_framing_is_not_injectable():
    framed = sse("text", {"text": "hello\n\nevent: done\ndata: {}"})
    assert framed.count("\n\n") == 1
    assert json.loads(framed.split("data: ", 1)[1])["text"].startswith("hello\n")


@pytest.mark.asyncio
async def test_disconnect_closes_source_and_releases_slot(tmp_path, monkeypatch):
    app = demo_app(tmp_path)
    thread = app.state.service.new_thread(Principal("C001", "customer"))
    emitted, closed = asyncio.Event(), asyncio.Event()

    async def source(*args):
        try:
            yield "step", {"status": "working"}
            await asyncio.sleep(60)
        finally:
            closed.set()

    monkeypatch.setattr(app.state.service, "chat", source)
    body_sent = False

    async def receive():
        nonlocal body_sent
        if not body_sent:
            body_sent = True
            return {"type": "http.request", "body": b'{"text":"Hello"}', "more_body": False}
        await emitted.wait()
        return {"type": "http.disconnect"}

    async def send(message):
        if message["type"] == "http.response.body" and message.get("body"):
            emitted.set()

    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": f"/threads/{thread}/messages",
        "query_string": b"",
        "headers": [
            (b"authorization", ("Bearer " + CUSTOMER).encode()),
            (b"content-type", b"application/json"),
        ],
        "client": ("127.0.0.1", 1234),
        "server": ("testserver", 80),
    }
    async with asyncio.timeout(2):
        await app(scope, receive, send)
    assert closed.is_set()
    assert not app.state.service.admission.active


def test_startup_never_accepts_demo_credentials(tmp_path):
    with pytest.raises(ValueError):
        configured_app(
            Settings(runtime_dir=str(tmp_path), api_customer_token="", api_manager_token="")
        )


def button(app, label):
    return next(item for item in app.button if item.label == label)


@pytest.mark.parametrize("decision", ["Approve", "Reject"])
def test_streamlit_chat_reset_identity_and_review(tmp_path, decision):
    with TestClient(demo_app(tmp_path)) as client:
        app = AppTest.from_string(
            "import streamlit as st\nfrom common.ui import render\n"
            'render(st.session_state["client"])',
            default_timeout=15,
        )
        app.session_state["client"] = client
        AppTest.run(app)
        app.text_input(key="customer_token").input(CUSTOMER)
        AppTest.run(app)
        first = app.session_state["thread_id"]
        app.chat_input[0].set_value("Please check BW1001")
        AppTest.run(app)
        assert len(app.session_state["conversation"]) == 2
        button(app, "Check return eligibility").click()
        AppTest.run(app)
        assert app.session_state["review_state"]["pending"]
        app.text_input(key="reviewer_token").input(REVIEWER)
        AppTest.run(app)
        button(app, "Load review").click()
        AppTest.run(app)
        button(app, decision).click()
        AppTest.run(app)
        assert not app.session_state["manager_review"]["pending"]
        button(app, "New conversation").click()
        AppTest.run(app)
        assert app.session_state["thread_id"] != first
        assert app.session_state["conversation"] == []
        app.text_input(key="customer_token").input(OTHER)
        AppTest.run(app)
        assert app.session_state["identity_token"] == OTHER
        assert "manager_review" not in app.session_state
        assert not app.exception
