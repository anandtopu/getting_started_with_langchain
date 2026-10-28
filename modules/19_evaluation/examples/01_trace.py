"""Redact before opening a trace; write a safe local JSON envelope.

Run: uv run --extra agents python modules/19_evaluation/examples/01_trace.py --offline
Expected: Email and secret fields are replaced; tracing is optional.
Cost: No model calls; an explicitly enabled live trace uploads sanitized fields. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.security import log_event
from common.tracing import sanitized_trace


def main() -> None:
    settings = lesson_settings()
    # KEY IDEA: sanitization occurs before the decorated trace function receives inputs.
    safe = sanitized_trace(
        {"question": "Contact alex@example.test", "password": "synthetic"}, settings
    )
    print_text(log_event("support_demo", "demo-01", {"payload": safe}, settings))


if __name__ == "__main__":
    run_cli(main)
