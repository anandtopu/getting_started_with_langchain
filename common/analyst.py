"""A bounded text-to-SQL loop over explicitly allowed synthetic staff analytics columns."""

import math
import re
import sqlite3
from pathlib import Path

from pydantic import BaseModel, Field

from common.config import Settings
from common.data import DATA_DIR, orders_connection
from common.fixtures import structured_fixture
from common.models import get_chat_model

TABLES = {
    "orders": {"order_id", "status", "total_cents", "shipping_speed"},
    "order_items": {"order_id", "sku", "quantity", "unit_price_cents"},
    "products": {"sku", "category", "name", "stock", "price_cents"},
}


def analytics_schema() -> dict:
    """Inspect actual SQLite metadata, projecting only the operator-approved columns."""
    with orders_connection() as db:
        return {
            table: {
                row["name"]: row["type"]
                for row in db.execute(f"PRAGMA table_info({table})")
                if row["name"] in allowed
            }
            for table, allowed in TABLES.items()
        }


def analytics_query(sql: str) -> list[dict]:
    if (
        len(sql) > 2000
        or not re.match(r"\A\s*SELECT\b", sql, re.I)
        or any(token in sql for token in (";", "--", "/*", "\x00"))
    ):
        raise ValueError("Use one SELECT statement of at most 2,000 characters.")

    def authorize(action, first, second, database, trigger):
        if action == sqlite3.SQLITE_SELECT:
            return sqlite3.SQLITE_OK
        if (
            action == sqlite3.SQLITE_READ
            and first in TABLES
            and (second in TABLES[first] or second == "")
        ):
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_FUNCTION and second in {
            "sum",
            "count",
            "avg",
            "round",
            "min",
            "max",
        }:
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY

    with orders_connection() as db:
        db.set_authorizer(authorize)
        db.set_progress_handler(lambda: 1, 100_000)
        rows = [dict(row) for row in db.execute(sql).fetchmany(51)]
    if not rows or len(rows) > 50:
        raise ValueError("Return 1 through 50 grouped rows.")
    for row in rows:
        if set(row) != {"label", "value"} or not isinstance(row["label"], str):
            raise ValueError("Return label text and a numeric value, using those exact aliases.")
        if (
            len(row["label"]) > 100
            or not isinstance(row["value"], (int, float))
            or (not math.isfinite(row["value"]) or row["value"] < 0)
        ):
            raise ValueError("Chart values must be finite nonnegative numbers and labels short.")
    return rows


class SQLProposal(BaseModel):
    sql: str = Field(min_length=1, max_length=2000)


def fixture_sql(question: str) -> str:
    """Only request wording drives the fixture; no evaluation labels enter the planner."""
    if "category" in question.lower():
        return (
            "SELECT p.category AS label,SUM(i.quantity) AS value FROM order_items i "
            "JOIN products p ON p.sku=i.sku GROUP BY p.category ORDER BY p.category"
        )
    if "revenue" in question.lower():
        return (
            "SELECT status AS label,SUM(total_cents) AS value FROM orders "
            "GROUP BY status ORDER BY status"
        )
    return "SELECT status AS label,COUNT(*) AS value FROM orders GROUP BY status ORDER BY status"


def analyze(question: str, settings: Settings, *, max_attempts: int = 2) -> dict:
    if not question.strip() or len(question) > 2000 or not 1 <= max_attempts <= 3:
        raise ValueError("Use a bounded question and one through three SQL attempts.")
    schema, attempts, feedback = analytics_schema(), [], ""
    rows = []
    for attempt in range(max_attempts):
        # The deliberate first typo makes repair observable instead of merely promised.
        sql = (
            "SELECT missing_column AS label,COUNT(*) AS value FROM orders"
            if attempt == 0
            else fixture_sql(question)
        )
        model = get_chat_model(
            settings=settings,
            temperature=0,
            responses=[structured_fixture(SQLProposal, {"sql": sql})],
        )
        proposal = model.with_structured_output(SQLProposal).invoke(
            "Write read-only SQLite analytics SQL. Return label and nonnegative numeric value "
            "aliases, at most 50 grouped rows. No private customer data, comments or semicolons. "
            f"Schema: {schema}. Question: {question}. Previous database feedback: {feedback}"
        )
        try:
            rows = analytics_query(proposal.sql)
        except (ValueError, sqlite3.DatabaseError) as error:
            feedback = str(error)[:200]
            attempts.append({"sql": proposal.sql, "error": feedback})
        else:
            attempts.append({"sql": proposal.sql, "rows": len(rows)})
            break
    if not rows:
        return {
            "accepted": False,
            "attempts": attempts,
            "rows": [],
            "summary": "SQL budget exhausted.",
        }
    total = sum(row["value"] for row in rows)
    summary = get_chat_model(
        settings=settings,
        temperature=0,
        responses=[
            f"Synthetic analysis of {len(rows)} groups; combined value {total}. Source: orders.db."
        ],
    ).invoke(
        f"Write a cautious executive summary of these synthetic SQL results: {rows}. "
        "Do not infer causal effects or real revenue forecasts. Identify units from the query. "
        f"Question: {question}. SQL: {attempts[-1]['sql']}"
    )
    return {
        "accepted": True,
        "attempts": attempts,
        "schema": schema,
        "rows": rows,
        "verified_total": total,
        "summary": str(summary.content),
        "mode": "scripted-sql-repair" if settings.course_offline else "live",
    }


def chart(result: dict, output: Path) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if not result["accepted"] or output.resolve().is_relative_to(DATA_DIR.resolve()):
        raise ValueError("Chart accepted results to a runtime location outside data/.")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, axis = plt.subplots(figsize=(8, 4), layout="constrained")
    axis.bar([row["label"] for row in result["rows"]], [row["value"] for row in result["rows"]])
    axis.set(title="Brightwave synthetic analytics", ylabel="Query value (see SQL for units)")
    axis.tick_params(axis="x", labelrotation=25)
    fig.savefig(output, dpi=140)
    plt.close(fig)
    return output
