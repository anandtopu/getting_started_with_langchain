"""Budgets, redaction, least privilege and streamed tool fixture regressions."""

import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor

import pytest

from common.budget import Admission, BudgetLedger, UsageBudget
from common.config import Settings
from common.fixtures import tool_request
from common.models import get_chat_model
from common.security import Principal, authenticate, log_event, public_query, scrub


def test_atomic_reservations_and_reopen(tmp_path):
    path = tmp_path / "budget.db"
    budget = BudgetLedger(path, 6)

    def reserve(index):
        try:
            return budget.reserve("session", 3)
        except ValueError:
            return "denied"

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(reserve, range(4)))
    assert sorted(value for value in results if isinstance(value, int)) == [3, 6]
    assert results.count("denied") == 2
    with pytest.raises(ValueError):
        BudgetLedger(path, 6).reserve("session", 1)


def test_rate_concurrency_and_release():
    admission = Admission(maximum=1, per_minute=1)
    with admission.slot("one", "C001"):
        with pytest.raises(BlockingIOError):
            with admission.slot("two", "C002"):
                pass
    assert not admission.active
    with pytest.raises(BlockingIOError):
        with admission.slot("three", "C001"):
            pass
    with admission.slot("two", "C002"):
        assert admission.active == {"two"}


def test_unknown_usage_is_not_zero_cost():
    budget = UsageBudget(Settings(course_offline=True))
    assert budget.record(None) is None
    with pytest.raises(ValueError):
        budget.before_next_call()


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT * FROM customers",
        "SELECT * FROM orders",
        "SELECT load_extension('file')",
        "DELETE FROM products",
        "SELECT sku FROM products; SELECT 1",
    ],
)
def test_sql_rejects_private_and_executable_requests(sql):
    with pytest.raises((ValueError, sqlite3.DatabaseError)):
        public_query(sql)


def test_public_sql_bounded_output():
    rows = public_query("SELECT sku,name FROM products")
    assert len(rows) == 20 and set(rows[0]) == {"sku", "name"}


def test_redaction_is_recursive_and_precedes_serialization():
    settings = Settings(api_customer_token="unprintable-secret-token")
    fields = {
        "payload": ["x@example.test", "4111111111111111", "unprintable-secret-token"],
        "authorization": "anything",
    }
    result = log_event("test", "case-1", fields, settings)
    assert all(value not in result for value in fields["payload"])
    assert json.loads(result)["authorization"] == "[REDACTED]"
    assert scrub(object()) == "[UNSERIALIZABLE]"


def test_reserved_log_fields_and_invalid_credentials():
    value = json.loads(log_event("safe", "safe-id", {"correlation_id": "spoof\n", "event": "fake"}))
    assert value["correlation_id"] == "safe-id" and value["event"] == "safe"
    with pytest.raises(PermissionError):
        authenticate("invalid\u00e9", {"valid-token": Principal("C001", "customer")})


def test_modern_tool_fixture_stream_is_preserved():
    model = get_chat_model(responses=[tool_request("lookup_order", {"order_id": "BW1001"})])
    chunks = list(model.stream("Check order"))
    result = chunks[0]
    for chunk in chunks[1:]:
        result += chunk
    assert result.tool_calls[0]["args"] == {"order_id": "BW1001"}


@pytest.mark.asyncio
async def test_async_tool_fixture_stream_is_preserved():
    model = get_chat_model(responses=[tool_request("lookup_order", {"order_id": "BW1001"})])
    chunks = [chunk async for chunk in model.astream("Check order")]
    assert chunks[0].tool_calls[0]["name"] == "lookup_order"
