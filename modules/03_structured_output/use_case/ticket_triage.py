"""Extract every ticket into CSV and score only the labelled subset.

Run: uv run python modules/03_structured_output/use_case/ticket_triage.py --offline
Expected: 100 rows in .runtime/triage.csv and separately labelled fixture/live metrics.
Cost: 100 short calls; budget up to $0.10 on the default low-cost profile. Run --offline first.
"""

import json

from common.config import ROOT
from common.data import load_jsonl
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.triage import score_predictions, triage_ticket, write_triage_csv


def main() -> None:
    settings = lesson_settings()
    tickets = load_jsonl("support_tickets.jsonl")
    rows = []
    for ticket in tickets:
        # KEY IDEA: gold labels never enter the model prompt.
        prediction = triage_ticket(ticket["text"], settings)
        rows.append({"ticket_id": ticket["ticket_id"], **prediction.model_dump(mode="json")})
    output = ROOT / settings.runtime_dir / "triage.csv"
    write_triage_csv(rows, output)
    label = (
        "FIXTURE plumbing score (not model accuracy)"
        if settings.course_offline
        else "LIVE model accuracy"
    )
    print_text(f"{len(rows)} rows -> {output}")
    print_text(label + ": " + json.dumps(score_predictions(rows, tickets)))


if __name__ == "__main__":
    run_cli(main)
