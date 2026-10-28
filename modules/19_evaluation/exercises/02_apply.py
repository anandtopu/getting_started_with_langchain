"""Sanitize nested inputs before the trace boundary without modifying the original object.

Run: uv run --extra agents python modules/19_evaluation/exercises/02_apply.py --offline
Expected: a runnable baseline; target checks reveal missing behavior.
Cost: no API calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def safe_payload(value: dict) -> dict:
    # YOUR CODE HERE: replace the runnable baseline.
    return value.copy()


def main() -> None:
    lesson_settings()
    print_text(str(safe_payload({"contact": "alex@example.test"})))


if __name__ == "__main__":
    run_cli(main)
