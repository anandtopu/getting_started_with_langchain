"""Approval boundary.

Task: Require approval only for integer cents strictly above 10000; reject negatives.

Run: uv run --extra agents python modules/10_agents/solutions/01_practice.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def needs_approval(cents: int) -> bool:
    # KEY IDEA: Approval boundary.
    if cents < 0:
        raise ValueError("Refund must be nonnegative.")
    return cents > 10000


def main() -> None:
    lesson_settings()
    print_text(str(needs_approval(10001)))


if __name__ == "__main__":
    run_cli(main)
