"""Compare tool names AND arguments; forbid unapproved side effects even if labels contain them.

Run: uv run --extra agents python modules/19_evaluation/solutions/01_practice.py --offline
Expected: a runnable reference behavior.
Cost: no API calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.support_evaluation import evaluate_trajectory


def trajectory_ok(actual: list[dict], expected: list[dict]) -> bool:
    # KEY IDEA: enforce the contract at the trusted boundary.
    return evaluate_trajectory(actual, expected, ["send_email", "approve_refund"])


def main() -> None:
    lesson_settings()
    print_text(str(trajectory_ok([], [])))


if __name__ == "__main__":
    run_cli(main)
