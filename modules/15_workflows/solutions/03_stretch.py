"""Validated worker plan: Produce one Send per unique allowlisted category; reject empty,
repeated or unknown work.

Run: uv run --extra agents python modules/15_workflows/solutions/03_stretch.py --offline
Expected: Runnable reference result.
Cost: No model calls. Requires: agents
"""

from langgraph.types import Send

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def dispatch(categories: list[str], allowed: set[str]) -> list[Send]:
    if (
        not categories
        or len(categories) > 6
        or len(set(categories)) != len(categories)
        or set(categories) - allowed
    ):
        raise ValueError("Invalid worker plan")
    return [Send("worker", {"category": category}) for category in categories]


def main() -> None:
    lesson_settings()
    print_text(str(dispatch(["tents"], {"tents", "apparel"})))


if __name__ == "__main__":
    run_cli(main)
