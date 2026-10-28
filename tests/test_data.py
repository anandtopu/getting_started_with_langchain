"""Check numeric truth, references, read-only access and deterministic regeneration."""

import hashlib
import json
import sqlite3
from pathlib import Path

import pytest

from common.data import (
    DATA_DIR,
    copy_orders,
    data_path,
    load_csv,
    load_json,
    load_jsonl,
    orders_connection,
)


def test_counts_and_manifest():
    assert len(load_csv("products.csv")) == 60
    assert len(load_csv("reviews.csv")) == 300
    assert len(load_json("faq.json")) == 40
    tickets = load_jsonl("support_tickets.jsonl")
    assert len(tickets) == 100
    assert sum(ticket["labels"] is not None for ticket in tickets) == 50
    for relative, digest in load_json("manifest.json")["files"].items():
        assert hashlib.sha256(data_path(relative).read_bytes()).hexdigest() == digest


def test_database_integrity_and_totals():
    with orders_connection() as connection:
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 200
        assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
        mismatches = connection.execute("""
            SELECT o.order_id FROM orders o JOIN order_items i USING(order_id)
            GROUP BY o.order_id
            HAVING o.subtotal_cents != SUM(i.quantity*i.unit_price_cents)
                OR o.total_cents != o.subtotal_cents+o.shipping_cents
        """).fetchall()
        assert mismatches == []
        with pytest.raises(sqlite3.OperationalError):
            connection.execute("DELETE FROM orders")
    with pytest.raises(sqlite3.ProgrammingError):
        connection.execute("SELECT 1")


def test_product_prices_match_database():
    with orders_connection() as connection:
        stored = {row["sku"]: row for row in connection.execute("SELECT * FROM products")}
    for product in load_csv("products.csv"):
        row = stored[product["sku"]]
        assert row["price_cents"] == int(product["price"].replace(".", ""))
        assert row["stock"] == int(product["stock"])


def test_fixture_references():
    with orders_connection() as connection:
        owners = dict(connection.execute("SELECT order_id, customer_id FROM orders"))
    for ticket in load_jsonl("support_tickets.jsonl"):
        if ticket["labels"]:
            assert owners[ticket["labels"]["order_id"]] == ticket["customer_id"]
    for question in load_jsonl("eval/rag.jsonl"):
        if question["source"]:
            assert data_path(question["source"]).is_file()
        for expected in question["must_contain"]:
            assert expected.lower() in question["answer"].lower()


def test_writable_copy_preserves_seed(tmp_path: Path):
    seed_before = data_path("orders.db").read_bytes()
    destination = copy_orders(tmp_path / "learner.db")
    with sqlite3.connect(destination) as connection:
        connection.execute("UPDATE products SET stock=0")
    assert data_path("orders.db").read_bytes() == seed_before
    with pytest.raises(FileExistsError):
        copy_orders(destination)
    with pytest.raises(ValueError, match="outside"):
        copy_orders(DATA_DIR / "new.db")


def test_path_escape_rejected():
    with pytest.raises(ValueError):
        data_path("../.env")


def test_handbook_pages_and_citation():
    pypdf = pytest.importorskip(
        "pypdf", reason="Install authoring group or rag extra for PDF inspection."
    )
    reader = pypdf.PdfReader(data_path("handbook/employee_handbook.pdf"))
    assert len(reader.pages) == 10
    for i, page in enumerate(reader.pages, 1):
        assert f"Page {i} of 10" in page.extract_text()
    assert "manager must approve refunds over $100" in reader.pages[7].extract_text()


def test_rebuild_is_deterministic(tmp_path: Path):
    pytest.importorskip("reportlab", reason="Install authoring group to rebuild the dataset.")
    from scripts.build_data import build

    first, second = tmp_path / "first", tmp_path / "second"
    assert build(first) == build(second)
    for relative in json.loads((first / "manifest.json").read_text())["files"]:
        assert (first / relative).read_bytes() == (second / relative).read_bytes()
