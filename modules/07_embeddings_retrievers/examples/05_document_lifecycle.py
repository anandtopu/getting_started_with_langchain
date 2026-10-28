"""Add, update and delete a temporary document by a stable explicit ID.

Run: uv run --extra rag python
modules/07_embeddings_retrievers/examples/05_document_lifecycle.py --offline
Expected: A temporary note changes content, then disappears; seed documents stay intact.
Cost: Offline: no API fees. Live embeddings depend on corpus size and the chosen provider.
Requires: rag
"""

from langchain_core.documents import Document

from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.vector_index import persistent_index


def main() -> None:
    # KEY IDEA: Stable IDs select which record is updated or deleted.
    settings = lesson_settings()
    store = persistent_index(
        chunk_documents(policy_documents()), settings, name="lesson07-lifecycle"
    )
    key = "temporary-training-note"
    store.add_documents(
        [Document(page_content="Brightwave demo stock: 10", metadata={"source": "synthetic-note"})],
        ids=[key],
    )
    store.update_documents(
        [key],
        [Document(page_content="Brightwave demo stock: 8", metadata={"source": "synthetic-note"})],
    )
    print_text(str(store.get(ids=[key])["documents"]))
    store.delete(ids=[key])
    assert store.get(ids=[key])["ids"] == []
    print_text("Temporary ID deleted. Changed embedding/corpus identity requires a new index name.")


if __name__ == "__main__":
    run_cli(main)
