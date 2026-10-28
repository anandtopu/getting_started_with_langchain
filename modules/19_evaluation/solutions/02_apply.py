"""Sanitize nested inputs before the trace boundary without modifying the original object.

Run: uv run --extra agents python modules/19_evaluation/solutions/02_apply.py --offline
Expected: a runnable reference behavior.
Cost: no API calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.security import scrub


def safe_payload(value: dict) -> dict:
    # KEY IDEA: enforce the contract at the trusted boundary.
    return scrub(value)


def main() -> None:
    lesson_settings()
    print_text(str(safe_payload({"contact": "alex@example.test"})))


if __name__ == "__main__":
    run_cli(main)
