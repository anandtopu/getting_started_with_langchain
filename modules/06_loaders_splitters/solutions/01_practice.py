"""Normalize page provenance. Task: Return a new Document with source and one-based page from a
zero-based page index; reject negatives.

Run: uv run --extra rag python modules/06_loaders_splitters/solutions/01_practice.py --offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

from langchain_core.documents import Document

from common.errors import run_cli
from common.knowledge import identify
from common.lesson import lesson_settings
from common.pretty import print_text


def page_document(text: str, source: str, index: int) -> Document:
    if index < 0:
        raise ValueError("Page index must be nonnegative")
    return identify(Document(page_content=text, metadata={"source": source, "page": index + 1}))


def main() -> None:
    lesson_settings()
    print_text(str(page_document("Return window: 30 days", "handbook.pdf", 0)))


if __name__ == "__main__":
    run_cli(main)
