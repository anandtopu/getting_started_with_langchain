"""Ask the host for customer-scoped history; a guessed thread must not bypass ownership.

Run: uv run --extra apps python modules/18_apps/exercises/02_apply.py --offline
Expected: a runnable baseline; target checks reveal missing behavior.
Cost: no API calls. Requires: apps
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def owned_history(service, thread: str, subject: str) -> dict:
    # YOUR CODE HERE: replace the runnable baseline.
    return {"thread_id": thread, "messages": []}


def main() -> None:
    lesson_settings()
    print_text("Use target checks with a temporary service.")


if __name__ == "__main__":
    run_cli(main)
