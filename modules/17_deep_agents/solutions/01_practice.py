"""Confined virtual path: Validate writes against the single allowed report path; reject traversal.

Run: uv run --extra agents python modules/17_deep_agents/solutions/01_practice.py --offline
Expected: Runnable reference result.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.research import virtual_path


def report_path(path: str) -> str:
    return virtual_path(path, writable=True)


def main() -> None:
    lesson_settings()
    print_text(report_path("/reports/trends.md"))


if __name__ == "__main__":
    run_cli(main)
