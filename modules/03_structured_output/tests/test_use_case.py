"""The realistic use case runs offline without changing committed data."""

from common.config import ROOT
from common.testing import execute_script


def test_use_case(tmp_path, monkeypatch):
    monkeypatch.setenv("RUNTIME_DIR", str(tmp_path))
    execute_script(ROOT / "modules/03_structured_output/use_case/ticket_triage.py", ["--offline"])

    import csv

    rows = list(csv.DictReader((tmp_path / "triage.csv").open(encoding="utf-8")))
    assert len(rows) == 100 and len({r["ticket_id"] for r in rows}) == 100
    assert rows[0]["order_id"] == "BW1001"
    assert rows[6]["priority"] == "high"


def test_metrics_use_ids_and_skip_unlabelled():
    from common.schemas import TicketTriage
    from common.triage import score_predictions

    labels = dict.fromkeys(TicketTriage.model_fields, "x")
    tickets = [{"ticket_id": "A", "labels": labels}, {"ticket_id": "B", "labels": None}]
    assert score_predictions([{**labels, "ticket_id": "A"}], tickets)["exact_match"] == 1
    assert score_predictions([], tickets)["exact_match"] == 0
    assert score_predictions([], [tickets[1]])["exact_match"] is None
