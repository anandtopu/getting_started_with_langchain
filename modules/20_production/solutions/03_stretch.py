"""Preserve a validated correlation ID and redact event fields before JSON serialization.

Run: uv run --extra apps python modules/20_production/solutions/03_stretch.py --offline
Expected: a runnable reference behavior.
Cost: no API calls. Requires: apps
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.security import log_event


def safe_event(correlation: str, fields: dict) -> str:
    # KEY IDEA: enforce the contract at the trusted boundary.
    return log_event("support", correlation, fields)


def main() -> None:
    lesson_settings()
    print_text(str(safe_event("run-1", {"contact": "alex@example.test"})))


if __name__ == "__main__":
    run_cli(main)
