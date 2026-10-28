"""Route a validated ticket using explicit business rules.

Run: uv run python modules/04_lcel_runnables/examples/05_routing.py --offline
Expected: high -> human review; low -> standard queue.
Cost: No model calls.
"""

from langchain_core.runnables import RunnableBranch, RunnableLambda

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def router() -> RunnableBranch:
    return RunnableBranch(
        (lambda row: row["priority"] == "high", RunnableLambda(lambda _: "human review")),
        RunnableLambda(lambda _: "standard queue"),
    )


def main() -> None:
    lesson_settings()
    # KEY IDEA: deterministic routing is often clearer than asking another model.
    print_text(str(router().batch([{"priority": "high"}, {"priority": "low"}])))
    print_text(
        "Use Python for simple conditions, LCEL for composable dataflow, "
        "LangGraph for durable loops."
    )


if __name__ == "__main__":
    run_cli(main)
