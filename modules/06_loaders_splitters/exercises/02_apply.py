"""Split while preserving metadata. Task: Split Documents into chunks of at most 120 characters
with target overlap 20, preserving source/page and parent ID.

Run: uv run --extra rag python modules/06_loaders_splitters/exercises/02_apply.py --offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

from langchain_core.documents import Document

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def split(documents: list[Document]) -> list[Document]:
    return documents


# YOUR CODE HERE: improve the runnable baseline above to meet the target checks.


def main() -> None:
    lesson_settings()
    print_text(
        str(
            split(
                [
                    Document(
                        page_content="Brightwave return policy. " * 20,
                        metadata={"source": "policy.md", "page": 2},
                    )
                ]
            )
        )
    )


if __name__ == "__main__":
    run_cli(main)
