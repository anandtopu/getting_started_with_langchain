"""Require nonempty data, exact safe trajectories and every correctness contract.
Never average away access failure.

Run: uv run --extra agents python modules/19_evaluation/solutions/03_stretch.py --offline
Expected: a runnable reference behavior.
Cost: no API calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.release import evaluation_gate


def release_ok(report: dict) -> bool:
    # KEY IDEA: enforce the contract at the trusted boundary.
    return evaluation_gate(report)


def main() -> None:
    lesson_settings()
    print_text(str(release_ok({"rows": []})))


if __name__ == "__main__":
    run_cli(main)
