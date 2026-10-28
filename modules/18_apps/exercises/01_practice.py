"""Frame one safe SSE event; reject unknown event names. Delegate to the checked framing helper.

Run: uv run --extra apps python modules/18_apps/exercises/01_practice.py --offline
Expected: a runnable baseline; target checks reveal missing behavior.
Cost: no API calls. Requires: apps
"""

import json

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def encode_event(event: str, data: dict) -> str:
    # YOUR CODE HERE: replace the runnable baseline.
    return json.dumps(data)


def main() -> None:
    lesson_settings()
    print_text(str(encode_event("text", {"text": "hello\nworld"})))


if __name__ == "__main__":
    run_cli(main)
