"""Validate citation provenance. Task: Resolve an ID/quote against retrieved documents; derive
source/page from metadata and reject unmatched claims.

Run: uv run --extra rag python modules/08_rag_fundamentals/solutions/02_apply.py --offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

from langchain_core.documents import Document

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def cite(chunk_id: str, quote: str, documents: list[Document]) -> dict:
    doc = next((d for d in documents if d.id == chunk_id), None)
    if doc is None or not quote or quote not in doc.page_content:
        raise ValueError("Citation mismatch")
    return {
        "chunk_id": chunk_id,
        "quote": quote,
        "source": doc.metadata["source"],
        "page": doc.metadata.get("page"),
    }


def main() -> None:
    lesson_settings()
    print_text(
        str(
            cite(
                "c1",
                "30 days",
                [
                    Document(
                        id="c1",
                        page_content="Return within 30 days",
                        metadata={"source": "policy.md"},
                    )
                ],
            )
        )
    )


if __name__ == "__main__":
    run_cli(main)
