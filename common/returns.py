"""Transactional synthetic return records; no payment service is connected."""

import hashlib
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal

from langchain.tools import ToolRuntime, tool
from langchain_core.tools import BaseTool
from pydantic import BaseModel, ConfigDict, Field

from common.data import DATA_DIR, copy_orders, orders_connection


@dataclass(frozen=True)
class SupportContext:
    """Trusted application inputs; the synthetic warehouse attestation is not model input."""

    customer_id: str
    database: Path
    today: date = date(2026, 1, 15)
    inspected_unused: bool = False
    proof_and_accessories: bool = False
    excluded_item: bool = False
    verified_exception: Literal["wrong_item", "defective"] | None = None


class ReturnRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    order_id: str = Field(pattern=r"^BW\d{4}$")
    sku: str = Field(pattern=r"^BW-\d{3}$")
    reason: Literal["unused", "wrong_item", "defective"] = "unused"
    idempotency_key: str = Field(pattern=r"^[a-zA-Z0-9_-]{8,80}$")


def runtime_orders(path: Path) -> Path:
    """Prepare only a fresh runtime copy; never silently overwrite a learner's work."""
    return copy_orders(path)


def _inspect_return(
    db: sqlite3.Connection, request: ReturnRequest, context: SupportContext
) -> dict:
    order = db.execute(
        "SELECT o.*, s.delivered_at FROM orders o LEFT JOIN shipments s USING(order_id) "
        "WHERE o.order_id=? AND o.customer_id=?",
        (request.order_id, context.customer_id),
    ).fetchone()
    if order is None:
        raise ValueError("Order not found for this customer.")
    previous = db.execute(
        "SELECT * FROM returns WHERE idempotency_key=?", (request.idempotency_key,)
    ).fetchone()
    if previous:
        if any(previous[key] != getattr(request, key) for key in ("order_id", "sku", "reason")):
            raise ValueError("Idempotency key already belongs to a different request.")
        return {**dict(previous), "replayed": True}
    item = db.execute(
        "SELECT * FROM order_items WHERE order_id=? AND sku=?", (request.order_id, request.sku)
    ).fetchone()
    if item is None:
        raise ValueError("SKU was not purchased on this order.")
    if (
        not order["delivered_at"]
        or not 0 <= (context.today - date.fromisoformat(order["delivered_at"])).days <= 30
    ):
        raise ValueError("Return requires delivery within the last 30 days.")
    if not context.proof_and_accessories or (
        request.reason == "unused" and not context.inspected_unused
    ):
        raise ValueError("Warehouse eligibility checks have not passed.")
    if context.excluded_item and request.reason != "defective":
        raise ValueError("Final-sale or personalized items require a defect review.")
    if request.reason != "unused" and context.verified_exception != request.reason:
        raise ValueError("Wrong-item or defect exceptions require warehouse verification.")
    used = db.execute(
        "SELECT COUNT(*) FROM returns WHERE order_id=? AND sku=? AND status!='rejected'",
        (request.order_id, request.sku),
    ).fetchone()[0]
    if used >= item["quantity"]:
        raise ValueError("Purchased quantity already has a return record.")
    amount = max(0, item["unit_price_cents"] - (600 if request.reason == "unused" else 0))
    return {"refund_cents": amount, "replayed": False}


def inspect_return(request: ReturnRequest, context: SupportContext) -> dict:
    """Read eligibility without creating a record; the writer repeats these checks atomically."""
    path = context.database.resolve()
    if path.is_relative_to(DATA_DIR.resolve()) or not path.is_file():
        raise ValueError("Use an existing runtime copy outside data/.")
    with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as db:
        db.row_factory = sqlite3.Row
        return _inspect_return(db, request, context)


def record_return(
    request: ReturnRequest,
    context: SupportContext,
    *,
    approved: bool = False,
    expected_refund_cents: int | None = None,
) -> dict:
    """One item per request; eligibility and quantity checks run inside the write transaction."""
    path = context.database.resolve()
    if path.is_relative_to(DATA_DIR.resolve()) or not path.is_file():
        raise ValueError("Use an existing runtime copy outside data/.")
    with closing(sqlite3.connect(path, timeout=10)) as db, db:
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("BEGIN IMMEDIATE")
        inspection = _inspect_return(db, request, context)
        if inspection["replayed"]:
            return inspection
        amount = inspection["refund_cents"]
        if expected_refund_cents is not None and amount != expected_refund_cents:
            raise ValueError("Refund amount changed; start a new policy review.")
        if amount > 10000 and not approved:
            raise ValueError("Refund over $100 requires manager approval; no record written.")
        key = "R-" + hashlib.sha256(request.idempotency_key.encode()).hexdigest()[:20]
        db.execute(
            "INSERT INTO returns VALUES (?,?,?,?,?,?,?,?,?)",
            (
                key,
                request.order_id,
                request.sku,
                request.reason,
                amount,
                "approved",
                int(approved),
                request.idempotency_key,
                context.today.isoformat(),
            ),
        )
        return {"return_id": key, "refund_cents": amount, "status": "approved", "replayed": False}


def return_tools(*, include_approval: bool = False) -> list[BaseTool]:
    """Approval tool must ONLY be attached with HumanInTheLoopMiddleware."""

    @tool
    def create_return(
        order_id: str,
        sku: str,
        reason: str,
        idempotency_key: str,
        runtime: ToolRuntime[SupportContext],
    ) -> dict:
        """Create one eligible return up to $100; larger refunds must use manager review."""
        try:
            return record_return(
                ReturnRequest(
                    order_id=order_id, sku=sku, reason=reason, idempotency_key=idempotency_key
                ),
                runtime.context,
            )
        except ValueError as error:
            return {"error": str(error)}

    @tool
    def approve_refund(
        order_id: str,
        sku: str,
        reason: str,
        idempotency_key: str,
        runtime: ToolRuntime[SupportContext],
    ) -> dict:
        """Request human review before recording a refund; policy eligibility still applies."""
        try:
            return record_return(
                ReturnRequest(
                    order_id=order_id, sku=sku, reason=reason, idempotency_key=idempotency_key
                ),
                runtime.context,
                approved=True,
            )
        except ValueError as error:
            return {"error": str(error)}

    return [create_return, approve_refund] if include_approval else [create_return]


@tool
def scoped_order(order_id: str, runtime: ToolRuntime[SupportContext]) -> dict:
    """Read an order only for the authenticated customer supplied by the application."""
    with orders_connection() as db:
        row = db.execute(
            "SELECT order_id,status,total_cents FROM orders WHERE order_id=? AND customer_id=?",
            (order_id, runtime.context.customer_id),
        ).fetchone()
    return dict(row) if row else {"error": "Order not found for this customer."}
