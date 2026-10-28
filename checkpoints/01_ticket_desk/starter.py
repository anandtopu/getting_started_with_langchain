"""Runnable Smart Ticket Desk baseline: triage and queue for human review.

Run: uv run python checkpoints/01_ticket_desk/starter.py --offline
Expected: a validated classification and a human-review draft, with no tool calls yet.
Cost: one short hosted call, normally under $0.01; --offline is free.
"""

import json

from common.config import Settings
from common.data import load_jsonl
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.triage import triage_ticket


def process_ticket(ticket: dict, customer_id: str, settings: Settings) -> dict:
    """A useful initial queue before the learner adds a scoped order-tool loop."""
    triage = triage_ticket(ticket["text"], settings)
    # YOUR CODE HERE: add the bounded loop, matching call IDs and evidence-grounded draft.
    return {
        "ticket_id": ticket["ticket_id"],
        "mode": "fixture" if settings.course_offline else "live",
        "triage": triage.model_dump(mode="json"),
        "tool_calls": [],
        "tool_results": [],
        "draft": "A Brightwave support colleague will review your ticket.",
        "sent": False,
    }


def main() -> None:
    settings = lesson_settings()
    print_text(
        json.dumps(
            process_ticket(load_jsonl("support_tickets.jsonl")[0], "C001", settings), indent=2
        )
    )


if __name__ == "__main__":
    run_cli(main)
