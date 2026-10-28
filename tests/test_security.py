"""Adversarial analytics and host-approval boundaries, independent of model obedience."""

import sqlite3

import pytest

from common.analyst import analytics_query
from common.personal_ops import OpsRepository


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT email AS label,1 AS value FROM customers",
        "SELECT customer_id AS label,total_cents AS value FROM orders",
        "SELECT load_extension('x') AS label,1 AS value",
        "DELETE FROM orders",
        "SELECT status AS label,1 AS value FROM orders; DROP TABLE orders",
    ],
)
def test_analytics_rejects_private_or_executable_queries(sql):
    with pytest.raises((ValueError, sqlite3.DatabaseError)):
        analytics_query(sql)


def test_approval_is_exact_owner_scoped_and_replay_safe(tmp_path):
    repo = OpsRepository(tmp_path, "owner-a")
    payload = {"item_id": "note-1", "title": "Review", "body": "alex@example.test"}
    receipt = repo.approve("notes_create", payload)
    with pytest.raises(PermissionError):
        repo.apply("notes_create", {**payload, "title": "Changed"}, receipt)
    with pytest.raises(PermissionError):
        OpsRepository(tmp_path, "owner-b").apply("notes_create", payload, receipt)
    with pytest.raises(PermissionError):
        repo.apply("notes_create", payload, "guessed")
    assert not repo.apply("notes_create", payload, receipt)["replayed"]
    assert repo.apply("notes_create", payload, receipt)["replayed"]
    assert len(repo.list_items("notes")) == 1
    assert repo.list_items("notes")[0]["body"] == "[EMAIL]"
    assert OpsRepository(tmp_path, "owner-b").list_items("notes") == []
    with sqlite3.connect(repo.path) as db:
        assert "alex@example.test" not in db.execute("SELECT payload FROM approvals").fetchone()[0]


def test_completion_requires_a_specific_owned_task(tmp_path):
    repo = OpsRepository(tmp_path, "learner")
    payload = {"item_id": "task-1", "title": "Check citations"}
    repo.apply("tasks_create", payload, repo.approve("tasks_create", payload))
    completion = {"item_id": "task-1"}
    repo.apply("tasks_complete", completion, repo.approve("tasks_complete", completion))
    assert repo.list_items("tasks")[0]["done"] == 1
    missing = {"item_id": "task-missing"}
    with pytest.raises(ValueError):
        repo.apply("tasks_complete", missing, repo.approve("tasks_complete", missing))
