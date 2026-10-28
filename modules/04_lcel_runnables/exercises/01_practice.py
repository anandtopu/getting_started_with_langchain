"""Compose normalization.

Task: Return a RunnableSequence: strip whitespace, then uppercase a SKU.
Run: uv run python modules/04_lcel_runnables/exercises/01_practice.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain_core.runnables import Runnable, RunnableLambda

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def pipeline() -> Runnable:
    return RunnableLambda(lambda value: value.strip())


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


def main() -> None:
    lesson_settings()
    print_text(pipeline().invoke(" bw-001 "))


if __name__ == "__main__":
    run_cli(main)
