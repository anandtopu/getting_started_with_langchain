"""Route review through the server boundary; preserve role and current interrupt validation.

Run: uv run --extra apps python modules/18_apps/solutions/03_stretch.py --offline
Expected: a runnable reference behavior.
Cost: no API calls. Requires: apps
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.security import Principal


def resume_review(service, reference: str, role: str, decision: str, interrupt_id: str) -> dict:
    # KEY IDEA: enforce the contract at the trusted boundary.
    return service.review(reference, Principal("reviewer", role), decision, interrupt_id)


def main() -> None:
    lesson_settings()
    print_text("Use target checks with a paused return.")


if __name__ == "__main__":
    run_cli(main)
