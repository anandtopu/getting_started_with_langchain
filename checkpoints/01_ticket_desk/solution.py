"""Smart Ticket Desk: triage, scoped order loop and a human-reviewed draft.

Run: uv run python checkpoints/01_ticket_desk/solution.py --offline --ticket T001
Expected: validated triage, two matched tool results and an unsent draft.
Cost: up to five short hosted calls; usually under $0.01. Offline/local no API fee.
"""

import argparse
import json

from common.config import get_settings
from common.data import load_jsonl
from common.desk import process_ticket
from common.errors import run_cli
from common.pretty import print_text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--ticket", default="T001")
    parser.add_argument(
        "--customer", default="C001", help="Synthetic demo login; not authentication"
    )
    args = parser.parse_args()
    settings = get_settings()
    if args.offline:
        settings = settings.model_copy(update={"course_offline": True})
    ticket = next(
        (t for t in load_jsonl("support_tickets.jsonl") if t["ticket_id"] == args.ticket), None
    )
    if ticket is None:
        raise ValueError("Unknown ticket; use T001 through T100.")
    # KEY IDEA: the selected demo login controls tool scope, not the ticket's claimed identity.
    print_text(json.dumps(process_ticket(ticket, args.customer, settings), indent=2))


if __name__ == "__main__":
    run_cli(main)
