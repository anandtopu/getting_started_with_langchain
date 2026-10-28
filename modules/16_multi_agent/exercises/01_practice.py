"""Confidence gate: Return sorted distinct roles only at confidence >=0.7 using RoutePlan
validation.

Run: uv run --extra agents python modules/16_multi_agent/exercises/01_practice.py --offline
Expected: Runnable baseline; complete YOUR CODE HERE to pass target tests.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def select(values: dict) -> list[str]:
    # YOUR CODE HERE: Return sorted distinct roles only at confidence >=0.7 using RoutePlan
    # validation.
    return values["roles"]


def main() -> None:
    lesson_settings()
    print_text(str(select({"roles": ["logistics"], "confidence": 0.5})))


if __name__ == "__main__":
    run_cli(main)
