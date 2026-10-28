"""Preserve and enrich.

Task: Use assign and parallel branches to retain review_id/text and add analysis with
characters and words.
Run: uv run python modules/04_lcel_runnables/exercises/02_apply.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain_core.runnables import Runnable, RunnableLambda

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def pipeline() -> Runnable:
    return RunnableLambda(lambda row: {"characters": len(row["text"])})


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


def main() -> None:
    lesson_settings()
    print_text(str(pipeline().invoke({"review_id": "V1", "text": "Good tent"})))


if __name__ == "__main__":
    run_cli(main)
