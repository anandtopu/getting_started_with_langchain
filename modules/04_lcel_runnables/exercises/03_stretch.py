"""Retry then fall back narrowly.

Task: Wrap primary: retry TimeoutError twice with no wait, then use backup. ValueError must
propagate.
Run: uv run python modules/04_lcel_runnables/exercises/03_stretch.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain_core.runnables import Runnable

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def resilient(primary: Runnable, backup: Runnable) -> Runnable:
    return primary


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


def main() -> None:
    lesson_settings()
    from langchain_core.runnables import RunnableLambda

    print_text(
        resilient(RunnableLambda(str.upper), RunnableLambda(lambda _: "review manually")).invoke(
            "tent"
        )
    )


if __name__ == "__main__":
    run_cli(main)
