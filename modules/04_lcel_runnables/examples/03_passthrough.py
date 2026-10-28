"""Preserve original fields and enrich an input dictionary with assign.

Run: uv run python modules/04_lcel_runnables/examples/03_passthrough.py --offline
Expected: The original review_id/text plus character count.
Cost: No model calls.
"""

from langchain_core.runnables import RunnablePassthrough

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    pipeline = RunnablePassthrough.assign(characters=lambda row: len(row["text"]))
    # KEY IDEA: assign adds keys to a dictionary; passthrough alone returns its input.
    print_text(str(pipeline.invoke({"review_id": "V0001", "text": "Comfortable tent."})))


if __name__ == "__main__":
    run_cli(main)
