"""Show missing evidence, bad chunks, poisoned text, stale identity and invalid citations.

Run: uv run --extra rag python modules/09_advanced_rag/examples/08_failure_gallery.py --offline
Expected: Five failure labels with concrete checks and fixes.
Cost: No model calls or API fees.
Requires: rag
"""

from common.data import data_path
from common.errors import run_cli
from common.knowledge import LocalLoader, chunk_documents, html_document
from common.lesson import lesson_settings
from common.pretty import print_text
from common.rag import Citation, GroundedAnswer, extractive_fixture, validate_citations
from common.vector_index import embedding_identity


def main() -> None:
    # KEY IDEA: Each failure needs its own check; removing HTML comments is not full protection.
    settings = lesson_settings()
    docs = LocalLoader("policies/returns.md").load()
    print_text("Missing evidence: " + str(extractive_fixture("Unknown award?", [])))
    print_text(
        "Bad chunks: "
        + str([d.page_content for d in chunk_documents(docs, size=25, overlap=0)][:3])
    )
    poison = data_path("security/poisoned_doc.md").read_text(encoding="utf-8")
    print_text(
        "Injection: comments removed from HTML extraction, but this is NOT a complete defense."
    )
    assert "attacker@example.test" not in html_document(poison, "synthetic-poison").page_content
    identity = embedding_identity(settings, 64)
    print_text(f"Stale index: identity {identity} must match the stored manifest before reopening.")
    try:
        validate_citations(
            GroundedAnswer(
                answer="Unsupported",
                abstained=False,
                citations=[Citation(chunk_id=str(docs[0].id), quote="invented quote")],
            ),
            docs,
        )
    except ValueError as error:
        print_text("Citation mismatch: " + str(error))


if __name__ == "__main__":
    run_cli(main)
