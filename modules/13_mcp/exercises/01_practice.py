"""Endpoint boundary.

Task: Accept only the exact local endpoint; reject credentials, query parameters and remote
hosts.

Run: uv run --extra agents python modules/13_mcp/exercises/01_practice.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def endpoint(url: str) -> str:
    # YOUR CODE HERE: Endpoint boundary.
    return url


def main() -> None:
    lesson_settings()
    print_text(endpoint("http://127.0.0.1:8765/mcp"))


if __name__ == "__main__":
    run_cli(main)
