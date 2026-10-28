"""Make persistence service opt-in and demonstrate namespace isolation locally.

Run: uv run --extra apps python modules/20_production/examples/08_postgres.py --offline
Expected: Namespace isolation; real Postgres requires explicit service configuration.
Cost: No API calls; deterministic local checks. Requires: apps
"""

from langgraph.store.memory import InMemoryStore

from common.deployment import postgres_probe
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    if not settings.course_offline and settings.postgres_uri.get_secret_value():
        # KEY IDEA: real persistence closes and reopens connections; setup creates SDK tables.
        print_text(str(postgres_probe(settings)))
        return
    store = InMemoryStore()
    store.put(("C001", "preferences"), "shipping", {"method": "standard"})
    assert store.get(("C002", "preferences"), "shipping") is None
    print_text("In-memory namespace check passed; Postgres persistence was NOT tested by this run.")
    print_text(
        "Install deployment extras; set POSTGRES_URI to a disposable database; omit --offline."
    )


if __name__ == "__main__":
    run_cli(main)
