"""Tool allowlist.

Task: Accept exactly one inventory_stock tool name; reject duplicates and additional tools.

Run: uv run --extra agents python modules/13_mcp/exercises/02_apply.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def allow_names(names: list[str]) -> list[str]:
    # YOUR CODE HERE: Tool allowlist.
    return names


def main() -> None:
    lesson_settings()
    print_text(str(allow_names(["inventory_stock"])))


if __name__ == "__main__":
    run_cli(main)
