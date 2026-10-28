"""Fan the same review out into named Runnable branches.

Run: uv run python modules/04_lcel_runnables/examples/02_parallel.py --offline
Expected: A dictionary with length and words, both computed from the same input.
Cost: Pure Python; no model calls.
"""

from langchain_core.runnables import RunnableLambda, RunnableParallel

from common.data import load_csv
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    pipeline = RunnableParallel(
        length=RunnableLambda(len), words=RunnableLambda(lambda text: len(text.split()))
    )
    # KEY IDEA: branches receive the same input, not another branch's output.
    print_text(str(pipeline.invoke(load_csv("reviews.csv")[0]["text"])))


if __name__ == "__main__":
    run_cli(main)
