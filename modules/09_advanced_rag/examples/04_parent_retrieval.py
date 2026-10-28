"""Retrieve small children, then expand them to original parent documents.

Run: uv run --extra rag python modules/09_advanced_rag/examples/04_parent_retrieval.py
--offline
Expected: Child IDs followed by fewer, larger parent documents.
Cost: No model calls or API fees.
Requires: rag
"""

from common.advanced_rag import expand_parents
from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.retrieval import LexicalRetriever


def main() -> None:
    lesson_settings()
    parents = policy_documents()
    children = chunk_documents(parents, size=160, overlap=30)
    found = LexicalRetriever(children).search("refund manager approval")
    expanded = expand_parents(found, parents)
    # KEY IDEA: parent IDs map back to unchanged originals, not reconstructed text fragments.
    print_text(str([doc.id for doc in found]))
    print_text(str([(doc.metadata["source"], len(doc.page_content)) for doc in expanded]))


if __name__ == "__main__":
    run_cli(main)
