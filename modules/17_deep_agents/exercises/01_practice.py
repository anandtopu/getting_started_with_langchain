"""Confined virtual path: Validate writes against the single allowed report path; reject traversal.

Run: uv run --extra agents python modules/17_deep_agents/exercises/01_practice.py --offline
Expected: Runnable baseline; complete YOUR CODE HERE to pass target tests.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def report_path(path: str) -> str:
    # YOUR CODE HERE: Validate writes against the single allowed report path; reject traversal.
    return path


def main() -> None:
    lesson_settings()
    print_text(report_path("/reports/trends.md"))


if __name__ == "__main__":
    run_cli(main)
