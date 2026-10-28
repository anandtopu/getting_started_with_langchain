"""Small explicit boundaries: safe log fields, bearer roles, and public-only SQL."""

import json
import re
import secrets
import sqlite3
from dataclasses import dataclass

from common.config import Settings
from common.data import orders_connection
from common.pretty import redact


def scrub(value: object, settings: Settings | None = None) -> object:
    """Redact before storage/export. This narrow synthetic PII filter is not a DLP service."""
    if isinstance(value, dict):
        return {
            str(key): "[REDACTED]"
            if any(
                word in str(key).lower()
                for word in ("api_key", "authorization", "password", "secret", "bearer")
            )
            else scrub(item, settings)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [scrub(item, settings) for item in value]
    if isinstance(value, str):
        text = redact(value, settings)
        text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[EMAIL]", text)
        return re.sub(r"\b(?:\d[ -]?){15}\d\b", "[CARD]", text)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return "[UNSERIALIZABLE]"


def log_event(
    event: str, correlation_id: str, fields: dict, settings: Settings | None = None
) -> str:
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", correlation_id):
        raise ValueError("Invalid correlation ID.")
    return json.dumps(
        scrub({**fields, "event": event, "correlation_id": correlation_id}, settings),
        sort_keys=True,
        ensure_ascii=False,
    )


@dataclass(frozen=True)
class Principal:
    subject: str
    role: str


def authenticate(token: str, registry: dict[str, Principal]) -> Principal:
    if not token or not token.isascii():
        raise PermissionError("Authentication required.")
    for candidate, principal in registry.items():
        if secrets.compare_digest(token, candidate):
            return principal
    raise PermissionError("Authentication required.")


def public_query(sql: str, parameters: tuple = ()) -> list[dict]:
    """Teach SELECT validation plus an authorizer. Private tables are never exposed here."""
    if (
        not re.match(r"\A\s*SELECT\b", sql, re.IGNORECASE)
        or ";" in sql
        or "--" in sql
        or "/*" in sql
    ):
        raise ValueError("Use one SELECT statement without comments or separators.")
    allowed_columns = {"sku", "name", "category", "price_cents", "stock"}

    def authorize(
        action: int,
        first: str | None,
        second: str | None,
        database: str | None,
        trigger: str | None,
    ) -> int:
        if action == sqlite3.SQLITE_SELECT:
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_READ and first == "products" and second in allowed_columns:
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY

    with orders_connection() as db:
        db.set_authorizer(authorize)
        db.set_progress_handler(lambda: 1, 10000)
        return [dict(row) for row in db.execute(sql, parameters).fetchmany(20)]
