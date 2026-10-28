"""Conservative persistent call reservations and bounded single-process admission."""

import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from pathlib import Path
from threading import Lock
from time import monotonic

from common.config import Settings
from common.data import DATA_DIR
from common.pretty import estimate_cost


class UsageBudget:
    """Post-call cost accounting; unknown usage is unknown, never zero-dollar evidence."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.known_usd = 0.0
        self.unknown_calls = 0

    def record(self, usage: dict | None) -> float | None:
        cost = estimate_cost(usage, self.settings)
        if cost is None:
            self.unknown_calls += 1
        else:
            self.known_usd += cost
        return cost

    def before_next_call(self) -> None:
        if self.unknown_calls or self.known_usd >= self.settings.max_run_cost_usd:
            raise ValueError("Cannot authorize another call within the known dollar budget.")


class BudgetLedger:
    def __init__(self, path: Path, session_limit: int = 30) -> None:
        self.path = path.resolve()
        if self.path.is_relative_to(DATA_DIR.resolve()) or session_limit < 1:
            raise ValueError("Choose a positive budget and runtime database outside data/.")
        self.limit = session_limit
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS budgets "
                "(scope TEXT PRIMARY KEY, reserved INTEGER NOT NULL)"
            )

    def reserve(self, scope: str, calls: int) -> int:
        if not scope or calls < 1:
            raise ValueError("Positive reservations require a scope.")
        with closing(sqlite3.connect(self.path, timeout=10)) as db, db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT reserved FROM budgets WHERE scope=?", (scope,)).fetchone()
            total = (row[0] if row else 0) + calls
            if total > self.limit:
                raise ValueError("Session call budget exhausted.")
            db.execute(
                "INSERT INTO budgets VALUES (?,?) ON CONFLICT(scope) "
                "DO UPDATE SET reserved=excluded.reserved",
                (scope, total),
            )
        return total


class Admission:
    """One request per thread, limited total concurrency; not a distributed lock."""

    def __init__(self, maximum: int = 2, per_minute: int = 12) -> None:
        self.maximum, self.per_minute = maximum, per_minute
        self.active: set[str] = set()
        self.recent: dict[str, list[float]] = {}
        self.lock = Lock()

    @contextmanager
    def slot(self, thread: str, subject: str) -> Iterator[None]:
        with self.lock:
            now = monotonic()
            recent = [stamp for stamp in self.recent.get(subject, []) if now - stamp < 60]
            if (
                thread in self.active
                or len(self.active) >= self.maximum
                or len(recent) >= self.per_minute
            ):
                raise BlockingIOError("Request busy or rate limit reached; retry later.")
            self.active.add(thread)
            self.recent[subject] = [*recent, now]
        try:
            yield
        finally:
            with self.lock:
                self.active.discard(thread)


def enforce_input_budget(text: str, limit: int = 4000) -> None:
    if not text.strip() or len(text) > limit:
        raise ValueError(f"Use 1 through {limit} input characters.")
