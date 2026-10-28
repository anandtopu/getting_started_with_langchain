"""Security and persistence contracts; no claim about scripted model intelligence."""

import sqlite3
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import replace
from datetime import date

import pytest
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from common.config import Settings
from common.data import data_path
from common.fixtures import tool_request
from common.guardrails import HookLog, InputLimit, guarded_agent
from common.memory import Preferences, thread_config, trim_history
from common.models import get_chat_model
from common.returns import (
    ReturnRequest,
    SupportContext,
    record_return,
    return_tools,
    runtime_orders,
    scoped_order,
)


@pytest.fixture
def context(tmp_path):
    return SupportContext(
        "C008",
        runtime_orders(tmp_path / "orders.db"),
        inspected_unused=True,
        proof_and_accessories=True,
    )


def request(key="test-return"):
    return ReturnRequest(order_id="BW1008", sku="BW-021", idempotency_key=key)


def test_return_idempotency_payload_conflict_and_quantity(context):
    first = record_return(request(), context)
    assert first["refund_cents"] == 4995
    assert record_return(request(), context)["replayed"]
    with pytest.raises(ValueError, match="different request"):
        record_return(request().model_copy(update={"sku": "BW-008"}), context)
    with pytest.raises(ValueError, match="quantity"):
        record_return(request("another-key"), context)


def test_concurrent_retry_records_only_once(context):
    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(lambda _: record_return(request(), context), range(2)))
    assert sum(not r["replayed"] for r in outcomes) == 1


@pytest.mark.parametrize(
    "changes",
    [
        {"customer_id": "C001"},
        {"today": date(2026, 4, 1)},
        {"inspected_unused": False},
        {"proof_and_accessories": False},
        {"excluded_item": True},
    ],
)
def test_eligibility_is_not_overridden_by_approval(context, changes):
    with pytest.raises(ValueError):
        record_return(request(), replace(context, **changes), approved=True)


def test_model_cannot_assert_exception_or_write_seed(context):
    with pytest.raises(ValueError, match="verification"):
        record_return(request().model_copy(update={"reason": "defective"}), context)
    with pytest.raises(ValueError, match="outside data"):
        record_return(request(), replace(context, database=data_path("orders.db")))
    with pytest.raises(ValueError):
        ReturnRequest(**{**request().model_dump(), "approved": True})


@pytest.mark.parametrize("cents,allowed", [(9999, True), (10000, True), (10001, False)])
def test_exact_approval_boundary(context, cents, allowed):
    with closing(sqlite3.connect(context.database)) as db, db:
        db.execute(
            "UPDATE order_items SET unit_price_cents=? WHERE order_id='BW1008' AND sku='BW-021'",
            (cents + 600,),
        )
    if allowed:
        assert record_return(request(), context)["refund_cents"] == cents
    else:
        with pytest.raises(ValueError, match="manager approval"):
            record_return(request(), context)


def test_trusted_context_hidden_from_model_schema():
    for tool in [scoped_order, *return_tools(include_approval=True)]:
        properties = tool.tool_call_schema.model_json_schema()["properties"]
        assert not {"customer_id", "runtime", "approved", "database"} & set(properties)


@pytest.mark.parametrize("decision,count", [("approve", 1), ("reject", 0)])
def test_review_persists_and_reopens_without_preapproval_write(tmp_path, decision, count):
    pytest.importorskip(
        "langgraph.checkpoint.sqlite", reason="Install agents extra for persistence."
    )
    from langgraph.checkpoint.sqlite import SqliteSaver

    context = SupportContext(
        "C001",
        runtime_orders(tmp_path / "orders.db"),
        inspected_unused=True,
        proof_and_accessories=True,
    )
    config = thread_config("C001", "review")
    call = tool_request(
        "approve_refund",
        {
            "order_id": "BW1001",
            "sku": "BW-014",
            "reason": "unused",
            "idempotency_key": "durable-review",
        },
    )
    with SqliteSaver.from_conn_string(str(tmp_path / "checkpoints.db")) as saver:
        agent = guarded_agent(Settings(course_offline=True), [call], checkpointer=saver)
        state = agent.invoke(
            {"messages": [{"role": "user", "content": "Request manager review."}]},
            config,
            context=context,
        )
        assert state["__interrupt__"]
    with closing(sqlite3.connect(context.database)) as db:
        assert (
            db.execute(
                "SELECT COUNT(*) FROM returns WHERE idempotency_key='durable-review'"
            ).fetchone()[0]
            == 0
        )
    with SqliteSaver.from_conn_string(str(tmp_path / "checkpoints.db")) as saver:
        resumed = guarded_agent(Settings(course_offline=True), ["Reviewed."], checkpointer=saver)
        resumed.invoke(Command(resume={"decisions": [{"type": decision}]}), config, context=context)
    with closing(sqlite3.connect(context.database)) as db:
        assert (
            db.execute(
                "SELECT COUNT(*) FROM returns WHERE idempotency_key='durable-review'"
            ).fetchone()[0]
            == count
        )


def test_hook_order_and_input_guard():
    from common.tools import make_order_tools

    log = HookLog()
    agent = create_agent(
        get_chat_model(
            offline=True, responses=[tool_request("check_stock", {"sku": "BW-001"}), "Done"]
        ),
        make_order_tools("C001"),
        middleware=[InputLimit(), log],
    )
    agent.invoke({"messages": [HumanMessage("Check stock")]})
    assert log.events == [
        "before_agent",
        "before_model",
        "model_enter",
        "model_exit",
        "after_model",
        "tool_enter",
        "tool_exit",
        "before_model",
        "model_enter",
        "model_exit",
        "after_model",
        "after_agent",
    ]
    with pytest.raises(ValueError, match="4000"):
        agent.invoke({"messages": [HumanMessage("x" * 4001)]})


def test_memory_scopes_preferences_and_complete_tool_turns(tmp_path):
    agent = create_agent(get_chat_model(offline=True), tools=[], checkpointer=InMemorySaver())
    first = thread_config("C001", "same")
    agent.invoke({"messages": [HumanMessage("private note")]}, first)
    other = agent.invoke({"messages": [HumanMessage("hello")]}, thread_config("C002", "same"))
    assert len(other["messages"]) == 2
    prefs = Preferences(tmp_path / "prefs.db")
    prefs.put("C001", "standard")
    assert (
        Preferences(tmp_path / "prefs.db").get("C001") == "standard" and prefs.get("C002") is None
    )
    messages = [
        HumanMessage("Old " * 500),
        AIMessage("Old reply"),
        HumanMessage("stock"),
        tool_request("check_stock", {"sku": "BW-001"}),
        ToolMessage(content="87", tool_call_id="call-1"),
    ]
    trimmed = trim_history(messages, 140)
    assert len(trimmed) == 3 and trimmed[-1].tool_call_id == trimmed[-2].tool_calls[0]["id"]
    with pytest.raises(ValueError):
        agent.invoke({"messages": [HumanMessage("missing thread")]})
    with pytest.raises(ValueError):
        thread_config("", "invalid")
    with pytest.raises(ValueError, match="outside committed"):
        Preferences(data_path("orders.db"))


def test_invalid_review_decision_does_not_execute(tmp_path):
    context = SupportContext(
        "C001",
        runtime_orders(tmp_path / "orders.db"),
        inspected_unused=True,
        proof_and_accessories=True,
    )
    agent = guarded_agent(
        Settings(course_offline=True),
        [
            tool_request(
                "approve_refund",
                {
                    "order_id": "BW1001",
                    "sku": "BW-014",
                    "reason": "unused",
                    "idempotency_key": "invalid-decision",
                },
            )
        ],
    )
    config = thread_config("C001", "invaliddecision")
    assert agent.invoke(
        {"messages": [HumanMessage("Request refund review.")]}, config, context=context
    )["__interrupt__"]
    with pytest.raises(ValueError):
        agent.invoke(
            Command(resume={"decisions": [{"type": "respond", "message": "approved"}]}),
            config,
            context=context,
        )
    with closing(sqlite3.connect(context.database)) as db:
        assert (
            db.execute(
                "SELECT COUNT(*) FROM returns WHERE idempotency_key='invalid-decision'"
            ).fetchone()[0]
            == 0
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("transport", ["memory", "stdio", "http"])
async def test_actual_mcp_transports(transport, monkeypatch):
    pytest.importorskip("fastmcp", reason="Install agents extra for MCP.")
    from common.mcp import call_inventory, inventory_adapter

    if transport == "stdio":
        import io
        import sys

        # Jupyter's stream has no usable fileno; retain this portability regression check.
        monkeypatch.setattr(sys, "stderr", io.StringIO())

    async with inventory_adapter(transport) as adapter:
        result = await call_inventory(adapter, "BW-001")
        assert result == {"sku": "BW-001", "stock": 87, "name": "Ridge Tent"}
        with pytest.raises(ValueError):
            await call_inventory(adapter, "not-a-sku")


def test_mcp_rejects_unreviewed_endpoints_and_tools():
    from common.mcp import InventoryResult, checked_tools, validate_endpoint

    for value in [
        "https://example.test/mcp",
        "http://user@127.0.0.1:8765/mcp",
        "http://127.0.0.1:8765/mcp?q=1",
    ]:
        with pytest.raises(ValueError):
            validate_endpoint(value)
    with pytest.raises(ValueError):
        checked_tools([])
    with pytest.raises(ValueError):
        InventoryResult(sku="BW-001", stock=-1, name="Ridge Tent")
