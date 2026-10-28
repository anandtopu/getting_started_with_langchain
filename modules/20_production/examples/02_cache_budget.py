"""Scope a public cache, record unknown usage, and persist call reservations.

Run: uv run --extra apps python modules/20_production/examples/02_cache_budget.py --offline
Expected: A cache hit, unknown cost and an exhausted persistent budget.
Cost: No API calls; deterministic local checks. Requires: apps
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from langchain_core.caches import InMemoryCache
from langchain_core.globals import get_llm_cache, set_llm_cache

from common.budget import BudgetLedger, UsageBudget
from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings().model_copy(update={"course_offline": True})
    previous = get_llm_cache()
    try:
        # KEY IDEA: this global cache is ONLY for identical public requests in this process.
        set_llm_cache(InMemoryCache(maxsize=10))
        model = get_chat_model(settings=settings, responses=["Brightwave public greeting."])
        first = model.invoke("Give a public Brightwave greeting.")
        second = model.invoke("Give a public Brightwave greeting.")
        assert first.content == second.content
    finally:
        set_llm_cache(previous)
    usage = UsageBudget(settings)
    print_text(
        str(
            {
                "known_cost": usage.record({"input_tokens": 100, "output_tokens": 10}),
                "unknown_cost": usage.record(None),
            }
        )
    )
    try:
        usage.before_next_call()
    except ValueError:
        print_text("Unknown usage blocks the next dollar-budget authorization.")
    with TemporaryDirectory() as directory:
        ledger = BudgetLedger(Path(directory) / "budget.db", session_limit=3)
        print_text(str({"reserved": ledger.reserve("C001-thread", 3)}))
        try:
            ledger.reserve("C001-thread", 1)
        except ValueError:
            print_text("Persistent session call ceiling enforced.")


if __name__ == "__main__":
    run_cli(main)
