"""Use correlation IDs and redact before writing a JSON event.

Run: uv run --extra apps python modules/20_production/examples/03_structured_logging.py --offline
Expected: One parseable JSON event with credential, email and card replacements.
Cost: No API calls; deterministic local checks. Requires: apps
"""

import json

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.security import log_event


def main() -> None:
    settings = lesson_settings()
    # KEY IDEA: one correlation ID joins safe events without logging raw prompts or credentials.
    line = log_event(
        "request_finished",
        "request-001",
        {
            "authorization": "Bearer synthetic",
            "contact": "alex@example.test",
            "card": "4111 1111 1111 1111",
            "status": "denied",
        },
        settings,
    )
    assert json.loads(line)["contact"] == "[EMAIL]"
    print_text(line)


if __name__ == "__main__":
    run_cli(main)
