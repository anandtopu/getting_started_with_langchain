"""Format inspectable context. Task: Include each document ID, source, page and text in the
context string.

Run: uv run --extra rag python modules/08_rag_fundamentals/solutions/01_practice.py --offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

from langchain_core.documents import Document

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def context(documents: list[Document]) -> str:
    return "\n\n".join(
        f"ID={d.id}; source={d.metadata['source']}; page={d.metadata.get('page')}\n{d.page_content}"
        for d in documents
    )


def main() -> None:
    lesson_settings()
    print_text(
        context(
            [
                Document(
                    id="p1",
                    page_content="30-day window",
                    metadata={"source": "handbook.pdf", "page": 2},
                )
            ]
        )
    )


if __name__ == "__main__":
    run_cli(main)
