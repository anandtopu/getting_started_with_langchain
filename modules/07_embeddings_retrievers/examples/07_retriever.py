"""Expose a vector store as a configurable Runnable retriever.

Run: uv run --extra rag python modules/07_embeddings_retrievers/examples/07_retriever.py
--offline
Expected: Two filtered tent Documents from retriever.invoke.
Cost: Offline: no API fees. Live embeddings depend on corpus size and the chosen provider.
Requires: rag
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.retrieval import product_documents
from common.vector_index import persistent_index


def main() -> None:
    settings = lesson_settings()
    store = persistent_index(product_documents(), settings, name="lesson07-products")
    retriever = store.as_retriever(
        search_type="similarity", search_kwargs={"k": 2, "filter": {"category": "tents"}}
    )
    # KEY IDEA: a retriever returns Documents; generation belongs to a separate stage.
    print_text(str([doc.metadata["sku"] for doc in retriever.invoke("rain shelter")]))


if __name__ == "__main__":
    run_cli(main)
