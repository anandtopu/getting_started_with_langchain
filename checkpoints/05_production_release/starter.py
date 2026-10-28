"""Runnable release-check baseline; replace the decision stub with real contract evidence.

Run: uv run --extra apps python checkpoints/05_production_release/starter.py --offline
Expected: an explicitly incomplete acceptance result. Cost: none. Requires: apps
"""

from pathlib import Path

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def run_case(case: dict, directory: Path) -> dict:
    # YOUR CODE HERE: execute HTTP behavior and compare the independent expected status.
    return {"id": case["id"], "checks": {}, "passed": False}


def main() -> None:
    lesson_settings()
    print_text(str(run_case({"id": "approve", "decision": "approve"}, Path(".runtime"))))


if __name__ == "__main__":
    run_cli(main)
