"""Preserve a validated correlation ID and redact event fields before JSON serialization.

Run: uv run --extra apps python modules/20_production/exercises/03_stretch.py --offline
Expected: a runnable baseline; target checks reveal missing behavior.
Cost: no API calls. Requires: apps
"""

import json

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def safe_event(correlation: str, fields: dict) -> str:
    # YOUR CODE HERE: replace the runnable baseline.
    return json.dumps(fields)


def main() -> None:
    lesson_settings()
    print_text(str(safe_event("run-1", {"contact": "alex@example.test"})))


if __name__ == "__main__":
    run_cli(main)
