"""Control-flow and data-boundary checks; scripted replies are not quality evaluations."""

import json
import runpy
import sqlite3
from contextlib import closing
from dataclasses import replace

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from common.config import ROOT, Settings
from common.graphs import build_return_graph, queue_notice
from common.memory import thread_config
from common.operations import (
    RoutePlan,
    build_operations,
    route_roles,
    run_specialist,
    specialist_input,
)
from common.research import VirtualFiles, research_sources, validate_report, virtual_path
from common.returns import (
    ReturnRequest,
    SupportContext,
    inspect_return,
    record_return,
    runtime_orders,
)
from common.workflows import build_review_graph, category_facts, report_gate, review_groups


@pytest.fixture
def context(tmp_path):
    return SupportContext(
        "C001",
        runtime_orders(tmp_path / "orders.db"),
        inspected_unused=True,
        proof_and_accessories=True,
    )


def high_request():
    return {
        "order_id": "BW1001",
        "sku": "BW-014",
        "reason": "unused",
        "idempotency_key": "graph-contract",
    }


def counts(context):
    with closing(sqlite3.connect(context.database)) as db:
        returns = db.execute(
            "SELECT COUNT(*) FROM returns WHERE idempotency_key='graph-contract'"
        ).fetchone()[0]
        exists = db.execute(
            "SELECT 1 FROM sqlite_master WHERE name='notification_outbox'"
        ).fetchone()
        notices = (
            db.execute("SELECT COUNT(*) FROM notification_outbox").fetchone()[0] if exists else 0
        )
    return returns, notices


@pytest.mark.parametrize("decision,expected", [("approve", (1, 1)), ("reject", (0, 0))])
def test_reopen_review_and_exact_outbox(context, tmp_path, decision, expected):
    pytest.importorskip("langgraph.checkpoint.sqlite")
    from langgraph.checkpoint.sqlite import SqliteSaver

    config = thread_config("C001", "workflow")
    with SqliteSaver.from_conn_string(str(tmp_path / "checkpoints.db")) as saver:
        graph = build_return_graph(saver)
        assert graph.invoke({"request": high_request()}, config, context=context)["__interrupt__"]
    assert counts(context) == (0, 0)
    with SqliteSaver.from_conn_string(str(tmp_path / "checkpoints.db")) as saver:
        graph = build_return_graph(saver)
        graph.invoke(Command(resume=decision), config, context=context)
        assert counts(context) == expected
        if decision == "approve":
            graph.invoke({"request": high_request()}, config, context=context)
            assert counts(context) == (1, 1)


def test_inspection_reads_only_and_resume_rechecks_eligibility(context):
    assert inspect_return(ReturnRequest(**high_request()), context)["refund_cents"] == 12195
    assert counts(context) == (0, 0)
    graph = build_return_graph(InMemorySaver())
    config = thread_config("C001", "changed")
    graph.invoke({"request": high_request()}, config, context=context)
    result = graph.invoke(
        Command(resume="approve"), config, context=replace(context, proof_and_accessories=False)
    )
    assert "Warehouse" in result["status"] and counts(context) == (0, 0)


def test_wrong_customer_and_model_approval_fields(context):
    graph = build_return_graph(InMemorySaver())
    state = graph.invoke(
        {"request": high_request(), "approved": True},
        thread_config("C002", "blocked"),
        context=replace(context, customer_id="C002"),
    )
    assert "not found" in state["status"] and counts(context) == (0, 0)
    with pytest.raises(ValueError):
        graph.invoke(
            {"request": {**high_request(), "approved": True}},
            thread_config("C001", "invalid"),
            context=context,
        )


def test_invalid_review_does_not_write(context):
    graph = build_return_graph(InMemorySaver())
    config = thread_config("C001", "invalid")
    graph.invoke({"request": high_request()}, config, context=context)
    with pytest.raises(ValueError, match="Review must"):
        graph.invoke(Command(resume={"approved": True}), config, context=context)
    assert counts(context) == (0, 0)


def test_crash_between_return_and_outbox_is_recoverable(context, monkeypatch):
    import common.graphs as module

    graph = build_return_graph(InMemorySaver())
    config = thread_config("C001", "recover")
    graph.invoke({"request": high_request()}, config, context=context)
    original = module.queue_notice

    def failure(context, result):
        raise OSError("Synthetic outbox failure")

    monkeypatch.setattr(module, "queue_notice", failure)
    with pytest.raises(OSError):
        graph.invoke(Command(resume="approve"), config, context=context)
    assert counts(context) == (1, 0)
    monkeypatch.setattr(module, "queue_notice", original)
    graph.invoke(None, config, context=context)
    assert counts(context) == (1, 1)


def test_outbox_rechecks_owner_and_uses_recorded_amount(context):
    result = record_return(ReturnRequest(**high_request()), context, approved=True)
    with pytest.raises(ValueError):
        queue_notice(replace(context, customer_id="C002"), result)
    queue_notice(context, {**result, "refund_cents": 999999})
    queue_notice(context, result)
    assert counts(context) == (1, 1)
    with closing(sqlite3.connect(context.database)) as db:
        payload = json.loads(db.execute("SELECT payload FROM notification_outbox").fetchone()[0])
    assert payload["refund_cents"] == 12195


def test_review_map_reduce_gate_and_call_budget():
    groups = review_groups()
    categories = list(groups)
    assert sum(len(rows) for rows in groups.values()) == 300
    for category, rows in groups.items():
        assert category_facts(category, rows)["count"] == 50
    state = {"categories": categories, "sections": [], "attempt": 0, "model_calls": 0}
    result = build_review_graph(Settings(course_offline=True)).invoke(state, {"max_concurrency": 2})
    assert result["accepted"] and result["attempt"] == 2 and result["model_calls"] == 10
    assert len(result["sections"]) == 6 and report_gate(result["report"], categories)
    exhausted = build_review_graph(Settings(course_offline=True), max_attempts=1).invoke(state)
    assert not exhausted["accepted"] and exhausted["attempt"] == 1
    assert exhausted["model_calls"] == 8


@pytest.mark.parametrize("categories", [[], ["tents", "tents"], ["not-real"]])
def test_map_dispatch_rejects_invalid_work(categories):
    with pytest.raises(ValueError):
        build_review_graph(Settings(course_offline=True)).invoke(
            {"categories": categories, "sections": [], "attempt": 0, "model_calls": 0}
        )


def test_router_confidence_allowlist_and_context_projection():
    assert route_roles(RoutePlan(roles=["billing"], confidence=0.69)) == []
    assert route_roles(RoutePlan(roles=["billing"], confidence=0.7)) == ["billing"]
    with pytest.raises(ValueError):
        route_roles(RoutePlan(roles=["billing", "billing"], confidence=1))
    with pytest.raises(ValueError):
        RoutePlan(roles=["admin"], confidence=1)
    assert "BW1001" not in specialist_input("product", "BW1001", "BW-001")
    assert "BW-001" not in specialist_input("logistics", "BW1001", "BW-001")


@pytest.mark.parametrize("role", ["billing", "logistics"])
def test_specialist_preserves_customer_denial(role):
    report = run_specialist(Settings(course_offline=True), "C002", role, "BW1001", "BW-001")
    assert not report["verified_tool_result"]
    assert "error" in report["evidence"][0]
    assert "messages" not in report


def test_product_specialist_has_validated_citations_and_router_fallback():
    pytest.importorskip("rank_bm25")
    report = run_specialist(Settings(course_offline=True), "C001", "product", "BW1001", "BW-001")
    assert report["evidence"][0]["citations"]
    assert all(c["source"] == "products.csv" for c in report["evidence"][0]["citations"])
    result = build_operations(Settings(course_offline=True), "C001").invoke(
        {"question": "unclear", "order_id": "BW1001", "sku": "BW-001", "reports": []}
    )
    assert result["roles"] == [] and result["reports"] == []


@pytest.mark.parametrize(
    "path",
    [
        "../.env",
        "/sources/../.env",
        "C:\\private",
        "/reports//trends.md",
        "/reports/./trends.md",
        "/sources/missing.md",
    ],
)
def test_virtual_paths_refuse_escape_and_unreviewed_files(path):
    with pytest.raises(ValueError):
        virtual_path(path)


def test_virtual_write_scope_size_isolation_and_citations():
    first, second = VirtualFiles(), VirtualFiles()
    original = first.read("/sources/market_brief.md")
    with pytest.raises(ValueError):
        first.write("/sources/market_brief.md", "overwrite")
    with pytest.raises(ValueError):
        first.write("/reports/trends.md", "x" * 12001)
    first.write("/reports/trends.md", "Synthetic [/sources/market_brief.md]")
    assert "/reports/trends.md" not in second.files
    assert first.read("/sources/market_brief.md") == original
    assert validate_report(first.read("/reports/trends.md"), first) == ["/sources/market_brief.md"]
    with pytest.raises(ValueError):
        validate_report("Synthetic [/sources/missing.md]", first)


def test_offline_search_provenance_and_live_opt_in():
    pytest.importorskip("rank_bm25")
    settings = Settings(course_offline=True)
    docs = research_sources("repairable gear", settings)
    assert docs and all(
        doc.metadata["synthetic"] and doc.metadata["source"].startswith("data/research/")
        for doc in docs
    )
    with pytest.raises(ValueError, match="explicit live"):
        research_sources("repairable gear", settings, web=True)


def test_optional_sdk_real_tools_are_exercised(capsys, monkeypatch):
    pytest.importorskip("deepagents")
    import sys

    path = ROOT / "modules/17_deep_agents/examples/04_deepagents_sdk.py"
    monkeypatch.setattr(sys, "argv", [str(path), "--offline"])
    runpy.run_path(str(path))["main"]()
    assert "/reports/scope.md" in capsys.readouterr().out


def test_search_adapter_configuration_and_mocked_provenance(monkeypatch):
    package = pytest.importorskip("langchain_tavily")
    from langchain_tavily._utilities import TavilySearchAPIWrapper

    wrapper = TavilySearchAPIWrapper(tavily_api_key="synthetic-test-key")
    client = package.TavilySearch(api_wrapper=wrapper, max_results=3, search_depth="basic")
    assert client.max_results == 3
    observed = []

    class FakeSearch:
        def __init__(self, **kwargs):
            assert kwargs["max_results"] == 3 and not kwargs["include_raw_content"]

        def invoke(self, values):
            observed.append(values)
            return {"results": [{"url": "https://example.test/source", "content": "Test evidence"}]}

    monkeypatch.setattr(package, "TavilySearch", FakeSearch)
    settings = Settings(course_offline=False, tavily_api_key="synthetic-test-key")
    docs = research_sources("outdoor gear", settings, web=True)
    assert observed == [{"query": "outdoor gear"}]
    assert docs[0].metadata["source"] == "https://example.test/source"
    assert not docs[0].metadata["synthetic"]


def test_report_budget_cannot_start_with_negative_counter():
    with pytest.raises(ValueError, match="zero counters"):
        build_review_graph(Settings(course_offline=True)).invoke(
            {"categories": ["tents"], "sections": [], "attempt": -5, "model_calls": 0}
        )


def test_changed_amount_requires_new_review(context):
    graph = build_return_graph(InMemorySaver())
    config = thread_config("C001", "newprice")
    graph.invoke({"request": high_request()}, config, context=context)
    with closing(sqlite3.connect(context.database)) as db, db:
        db.execute(
            "UPDATE order_items SET unit_price_cents=20000 WHERE order_id='BW1001' AND sku='BW-014'"
        )
    result = graph.invoke(Command(resume="approve"), config, context=context)
    assert "amount changed" in result["status"] and counts(context) == (0, 0)
