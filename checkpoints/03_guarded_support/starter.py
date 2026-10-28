"""Guarded Support starter: deny all writes until the required controls are implemented.

Run: uv run --extra agents python checkpoints/03_guarded_support/starter.py --offline
Expected: a safe all-denied baseline; learner acceptance checks require real reviewed writes.
Cost: no model calls or API fees.
"""

from common.config import Settings
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def run_case(case: dict, settings: Settings) -> dict:
    # YOUR CODE HERE: wire scoped tools, actual review interrupts and transactional records.
    return {
        "id": case["id"],
        "mode": "all-denied-baseline",
        "paused": False,
        "records_before_review": 0,
        "records": 0,
        "tool_results": [],
    }


def main() -> None:
    settings = lesson_settings()
    print_text(str(run_case({"id": "baseline"}, settings)))


if __name__ == "__main__":
    run_cli(main)
