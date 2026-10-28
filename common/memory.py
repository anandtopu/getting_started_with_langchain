"""Thread-boundary helpers and customer-scoped durable preference storage."""

import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Literal

from langchain_core.messages import BaseMessage, trim_messages

from common.data import DATA_DIR


def thread_config(customer_id: str, conversation_id: str) -> dict:
    """A trusted host constructs this scope; it must never accept another user's thread ID."""
    if not customer_id.isalnum() or not conversation_id.isalnum():
        raise ValueError("Thread components must be nonempty alphanumeric identifiers.")
    return {
        "configurable": {"thread_id": f"{customer_id}:{conversation_id}"},
        "recursion_limit": 60,
    }


def trim_history(messages: list[BaseMessage], budget: int) -> list[BaseMessage]:
    """Keep whole latest turns; approximate token counts reserve an explicit input budget."""
    if budget < 1:
        raise ValueError("Token budget must be positive.")
    return trim_messages(
        messages,
        max_tokens=budget,
        token_counter="approximate",
        strategy="last",
        start_on="human",
        end_on=("human", "tool"),
        include_system=True,
        allow_partial=False,
    )


class Preferences:
    """Small SQL-backed application repository, not a fake LangGraph BaseStore."""

    def __init__(self, path: Path) -> None:
        if path.resolve().is_relative_to(DATA_DIR.resolve()):
            raise ValueError("Preferences must be outside committed data/.")
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(path)) as db, db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS preferences(customer TEXT PRIMARY KEY, "
                "shipping TEXT NOT NULL CHECK(shipping IN ('standard','expedited')))"
            )

    def put(self, customer: str, shipping: Literal["standard", "expedited"]) -> None:
        if not customer or shipping not in {"standard", "expedited"}:
            raise ValueError("Choose standard or expedited for a known customer.")
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute(
                "INSERT INTO preferences VALUES (?,?) ON CONFLICT(customer) "
                "DO UPDATE SET shipping=excluded.shipping",
                (customer, shipping),
            )

    def get(self, customer: str) -> str | None:
        with closing(sqlite3.connect(self.path)) as db:
            row = db.execute(
                "SELECT shipping FROM preferences WHERE customer=?", (customer,)
            ).fetchone()
        return row[0] if row else None
