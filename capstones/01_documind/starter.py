"""Runnable capstone baseline; implement its run_case behavioral contract.

Run: uv run --extra apps python capstones/01_documind/starter.py --offline
Expected: incomplete result; acceptance targets fail until you implement the specification.
Cost: no calls in the baseline. Requires: apps
"""

from pathlib import Path

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def run_case(case: dict, settings, directory: Path) -> dict:
    # YOUR CODE HERE: run the real mechanism, then compare independent expected outcomes.
    return {"id": case["id"], "passed": False}


def main() -> None:
    settings = lesson_settings()
    print_text(str(run_case({"id": "practice"}, settings, Path(".runtime"))))


if __name__ == "__main__":
    run_cli(main)
