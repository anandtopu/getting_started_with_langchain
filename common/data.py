"""Repository-relative seed data access and isolated writable database copies."""

import csv
import json
import shutil
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from common.config import ROOT, ConfigurationError

DATA_DIR = ROOT / "data"


def data_path(relative: str) -> Path:
    """Resolve a seed path without allowing a caller to escape the dataset directory."""
    path = (DATA_DIR / relative).resolve()
    if not path.is_relative_to(DATA_DIR.resolve()):
        raise ValueError("Data paths must stay inside data/.")
    if not path.is_file():
        raise ConfigurationError(f"Missing data/{relative}; restore the committed dataset.")
    return path


def load_csv(relative: str) -> list[dict[str, str]]:
    """Load a small teaching dataset; numeric conversion belongs to its schema."""
    with data_path(relative).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(relative: str) -> Any:
    """Read a JSON dataset using the same path rules as CSV."""
    return json.loads(data_path(relative).read_text(encoding="utf-8"))


def load_jsonl(relative: str) -> list[dict[str, Any]]:
    """Read newline-delimited JSON records, preserving the committed order."""
    return [
        json.loads(line)
        for line in data_path(relative).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


@contextmanager
def orders_connection() -> Iterator[sqlite3.Connection]:
    """Open immutable course seed data read-only and close it even after an error."""
    uri = data_path("orders.db").as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    try:
        yield connection
    finally:
        connection.close()


def copy_orders(destination: Path) -> Path:
    """Create a disposable writable copy; never overwrite an existing learner database."""
    destination = destination.resolve()
    if destination.is_relative_to(DATA_DIR.resolve()):
        raise ValueError("Writable databases must be outside committed data/.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with data_path("orders.db").open("rb") as source, destination.open("xb") as target:
        shutil.copyfileobj(source, target)
    return destination
