"""Redact synthetic email.

Task: Replace email-like tokens with [REDACTED_EMAIL]; preserve ordinary text. This is a narrow
regex exercise.

Run: uv run --extra agents python modules/12_middleware/solutions/01_practice.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

import re

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def redact_email(text: str) -> str:
    # KEY IDEA: Redact synthetic email.
    return re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[REDACTED_EMAIL]", text)


def main() -> None:
    lesson_settings()
    print_text(redact_email("Contact demo@example.test about my return."))


if __name__ == "__main__":
    run_cli(main)
