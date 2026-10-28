"""Ask the host for customer-scoped history; a guessed thread must not bypass ownership.

Run: uv run --extra apps python modules/18_apps/solutions/02_apply.py --offline
Expected: a runnable reference behavior.
Cost: no API calls. Requires: apps
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.security import Principal


def owned_history(service, thread: str, subject: str) -> dict:
    # KEY IDEA: enforce the contract at the trusted boundary.
    return service.session(thread, Principal(subject, "customer"))


def main() -> None:
    lesson_settings()
    print_text("Use target checks with a temporary service.")


if __name__ == "__main__":
    run_cli(main)
