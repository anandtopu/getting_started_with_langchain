"""Source provenance: Require synthetic wording and validate each cited virtual source exists.

Run: uv run --extra agents python modules/17_deep_agents/exercises/02_apply.py --offline
Expected: Runnable baseline; complete YOUR CODE HERE to pass target tests.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def citations(report: str) -> list[str]:
    # YOUR CODE HERE: Require synthetic wording and validate each cited virtual source exists.
    return []


def main() -> None:
    lesson_settings()
    print_text(str(citations("Synthetic scope [/sources/market_brief.md]")))


if __name__ == "__main__":
    run_cli(main)
