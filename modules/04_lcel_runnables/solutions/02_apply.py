"""Preserve and enrich.

Task: Use assign and parallel branches to retain review_id/text and add analysis with
characters and words.
Run: uv run python modules/04_lcel_runnables/solutions/02_apply.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel, RunnablePassthrough

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def pipeline() -> Runnable:
    analysis = RunnableParallel(
        characters=RunnableLambda(lambda row: len(row["text"])),
        words=RunnableLambda(lambda row: len(row["text"].split())),
    )
    return RunnablePassthrough.assign(analysis=analysis)


def main() -> None:
    lesson_settings()
    print_text(str(pipeline().invoke({"review_id": "V1", "text": "Good tent"})))


if __name__ == "__main__":
    run_cli(main)
