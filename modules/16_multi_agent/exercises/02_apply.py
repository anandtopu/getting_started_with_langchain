"""Private context projection: Return only order_id to logistics; do not include history, email
or customer ID.

Run: uv run --extra agents python modules/16_multi_agent/exercises/02_apply.py --offline
Expected: Runnable baseline; complete YOUR CODE HERE to pass target tests.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def project(state: dict) -> dict:
    # YOUR CODE HERE: Return only order_id to logistics; do not include history, email or
    # customer ID.
    return dict(state)


def main() -> None:
    lesson_settings()
    print_text(str(project({"order_id": "BW1001", "private": "Synthetic private note"})))


if __name__ == "__main__":
    run_cli(main)
