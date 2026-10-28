"""Adapt ordinary Python with RunnableLambda and the chain decorator.

Run: uv run python modules/04_lcel_runnables/examples/04_python_functions.py --offline
Expected: A clean Brightwave SKU and its catalogue label.
Cost: No model calls.
"""

from langchain_core.runnables import RunnableLambda, chain

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def normalize(value: str) -> str:
    return value.strip().upper()


@chain
def label(sku: str) -> str:
    return f"Brightwave product: {sku}"


def main() -> None:
    lesson_settings()
    # KEY IDEA: wrapping gives existing functions invoke/batch/config support.
    print_text((RunnableLambda(normalize) | label).invoke("  bw-001  "))


if __name__ == "__main__":
    run_cli(main)
