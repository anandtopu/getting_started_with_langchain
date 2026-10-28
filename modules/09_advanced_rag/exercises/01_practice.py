"""Fuse rankings without duplicates. Task: Use reciprocal-rank fusion for two rankings; repeated
IDs inside one list must not gain extra votes.

Run: uv run --extra rag python modules/09_advanced_rag/exercises/01_practice.py --offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

from langchain_core.documents import Document

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def combine(rankings: list[list[Document]]) -> list[Document]:
    return [doc for ranking in rankings for doc in ranking][:3]


# YOUR CODE HERE: improve the runnable baseline above to meet the target checks.


def main() -> None:
    lesson_settings()
    print_text(
        str(combine([[Document(id="a", page_content="Tent", metadata={"source": "products"})]]))
    )


if __name__ == "__main__":
    run_cli(main)
