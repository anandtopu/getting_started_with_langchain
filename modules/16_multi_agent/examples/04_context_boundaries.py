"""Give specialists only the identifiers needed for their jobs.

Run: uv run --extra agents python modules/16_multi_agent/examples/04_context_boundaries.py --offline
Expected: Product sees the SKU; logistics sees the order; neither sees the full history.
Cost: At most three short calls; cross-customer access is denied by SQL. Offline fixtures incur
no API fee.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.operations import run_specialist, specialist_input
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    private_history = "Synthetic private customer note: demo@example.test"
    for role in ("product", "logistics"):
        message = specialist_input(role, "BW1001", "BW-001")
        assert private_history not in message
        print_text(f"{role} receives: {message}")
    # KEY IDEA: projection is code; a prompt saying ignore private history is not isolation.
    report = run_specialist(settings, "C002", "logistics", "BW1001", "BW-001")
    print_text(str(report))


if __name__ == "__main__":
    run_cli(main)
