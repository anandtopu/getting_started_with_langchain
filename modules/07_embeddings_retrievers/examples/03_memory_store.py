"""Add documents to an in-memory vector index and retrieve similar text.

Run: uv run --extra rag python modules/07_embeddings_retrievers/examples/03_memory_store.py
--offline
Expected: Three result IDs and sources; offline order has no semantic meaning.
Cost: Offline: no API fees. Live embeddings depend on corpus size and the chosen provider.
Requires: rag
"""

from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.retrieval import memory_index


def main() -> None:
    # KEY IDEA: The query and stored documents must use the same embedding space.
    settings = lesson_settings()
    documents = chunk_documents(policy_documents())
    store = memory_index(documents, settings)
    for doc in store.similarity_search("How long do returns take?", k=3):
        print_text(str(doc.metadata))


if __name__ == "__main__":
    run_cli(main)
