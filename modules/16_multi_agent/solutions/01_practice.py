"""Confidence gate: Return sorted distinct roles only at confidence >=0.7 using RoutePlan
validation.

Run: uv run --extra agents python modules/16_multi_agent/solutions/01_practice.py --offline
Expected: Runnable reference result.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.operations import RoutePlan, route_roles
from common.pretty import print_text


def select(values: dict) -> list[str]:
    return route_roles(RoutePlan.model_validate(values))


def main() -> None:
    lesson_settings()
    print_text(str(select({"roles": ["logistics"], "confidence": 0.5})))


if __name__ == "__main__":
    run_cli(main)
