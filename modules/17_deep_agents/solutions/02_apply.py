"""Source provenance: Require synthetic wording and validate each cited virtual source exists.

Run: uv run --extra agents python modules/17_deep_agents/solutions/02_apply.py --offline
Expected: Runnable reference result.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.research import VirtualFiles, validate_report


def citations(report: str) -> list[str]:
    return validate_report(report, VirtualFiles())


def main() -> None:
    lesson_settings()
    print_text(str(citations("Synthetic scope [/sources/market_brief.md]")))


if __name__ == "__main__":
    run_cli(main)
