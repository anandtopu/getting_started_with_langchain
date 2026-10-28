"""Explicit return workflow with durable review and an idempotent local outbox."""

import json
import sqlite3
from contextlib import closing
from typing import Any, Literal, NotRequired, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from langgraph.types import Command, interrupt

from common.data import DATA_DIR
from common.returns import ReturnRequest, SupportContext, inspect_return, record_return


class ReturnState(TypedDict):
    request: dict
    category: NotRequired[str]
    refund_cents: NotRequired[int]
    approved: NotRequired[bool]
    result: NotRequired[dict]
    status: NotRequired[str]


def queue_notice(context: SupportContext, result: dict) -> str:
    """Queue once after a committed return; retry repairs a crash between the two writes."""
    key = result["return_id"]
    path = context.database.resolve()
    if path.is_relative_to(DATA_DIR.resolve()) or not path.is_file():
        raise ValueError("Use an existing runtime copy outside data/.")
    with closing(sqlite3.connect(path)) as db, db:
        db.execute("PRAGMA foreign_keys=ON")
        db.execute(
            "CREATE TABLE IF NOT EXISTS notification_outbox "
            "(return_id TEXT PRIMARY KEY REFERENCES returns(return_id), "
            "customer_id TEXT, payload TEXT)"
        )
        owned = db.execute(
            "SELECT r.refund_cents FROM returns r JOIN orders o USING(order_id) "
            "WHERE r.return_id=? AND o.customer_id=?",
            (key, context.customer_id),
        ).fetchone()
        if not owned:
            raise ValueError("Cannot queue another customer's return.")
        payload = json.dumps({"return_id": key, "refund_cents": owned[0]}, sort_keys=True)
        db.execute(
            "INSERT OR IGNORE INTO notification_outbox VALUES (?,?,?)",
            (key, context.customer_id, payload),
        )
    return key


def build_return_graph(checkpointer: Any = None) -> Any:
    """Only the host provides identity and warehouse attestations through runtime context."""

    def classify(state: ReturnState) -> dict:
        request = ReturnRequest.model_validate(state["request"])
        return {"request": request.model_dump(), "category": request.reason, "approved": False}

    def policy(
        state: ReturnState, runtime: Runtime[SupportContext]
    ) -> Command[Literal["review", "record", "denied"]]:
        try:
            quote = inspect_return(ReturnRequest(**state["request"]), runtime.context)
        except ValueError as error:
            return Command(update={"status": str(error)}, goto="denied")
        destination = (
            "review" if quote["refund_cents"] > 10000 and not quote["replayed"] else "record"
        )
        return Command(update={"refund_cents": quote["refund_cents"]}, goto=destination)

    def review(state: ReturnState) -> Command[Literal["record", "denied"]]:
        decision = interrupt({"request": state["request"], "refund_cents": state["refund_cents"]})
        # KEY IDEA: the node restarts on resume; there are no writes before interrupt.
        if decision not in ("approve", "reject"):
            raise ValueError("Review must be approve or reject.")
        return Command(
            update={"approved": decision == "approve", "status": decision},
            goto="record" if decision == "approve" else "denied",
        )

    def record(
        state: ReturnState, runtime: Runtime[SupportContext]
    ) -> Command[Literal["notify", "denied"]]:
        try:
            result = record_return(
                ReturnRequest(**state["request"]),
                runtime.context,
                approved=state.get("approved", False),
                expected_refund_cents=state["refund_cents"],
            )
        except ValueError as error:
            return Command(update={"status": str(error)}, goto="denied")
        return Command(update={"result": result}, goto="notify")

    def notify(state: ReturnState, runtime: Runtime[SupportContext]) -> dict:
        queue_notice(runtime.context, state["result"])
        return {"status": "recorded; notification queued locally"}

    graph = StateGraph(ReturnState, context_schema=SupportContext)
    for name, node in (
        ("classify", classify),
        ("policy", policy),
        ("review", review),
        ("record", record),
        ("notify", notify),
        ("denied", lambda state: {}),
    ):
        graph.add_node(name, node)
    graph.add_edge(START, "classify")
    graph.add_edge("classify", "policy")
    graph.add_edge("notify", END)
    graph.add_edge("denied", END)
    return graph.compile(checkpointer=checkpointer)


class StudioState(TypedDict):
    request: str
    result: NotRequired[str]


def studio_check(state: StudioState) -> dict:
    """Account-free read-only graph for local development; no model, database or credentials."""
    return {
        "result": "Review required" if "refund" in state["request"].lower() else "Route to support"
    }


_studio_builder = StateGraph(StudioState)
_studio_builder.add_node("classify", studio_check)
_studio_builder.add_edge(START, "classify")
_studio_builder.add_edge("classify", END)
studio_graph = _studio_builder.compile()
