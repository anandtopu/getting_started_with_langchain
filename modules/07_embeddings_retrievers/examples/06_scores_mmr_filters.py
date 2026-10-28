"""Compare scored similarity with diverse MMR results under a metadata filter.

Run: uv run --extra rag python
modules/07_embeddings_retrievers/examples/06_scores_mmr_filters.py --offline
Expected: Only tents appear; cosine distances are not answer probabilities.
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
    where = {"$and": [{"category": "tents"}, {"price": {"$lt": 300}}]}
    for doc, distance in store.similarity_search_with_score("waterproof tent", k=3, filter=where):
        print_text(f"{doc.metadata['sku']}: cosine distance={distance:.4f}; lower is closer")
    # KEY IDEA: MMR trades off query similarity against repeated, similar results.
    diverse = store.max_marginal_relevance_search(
        "waterproof tent", k=3, fetch_k=8, lambda_mult=0.5, filter=where
    )
    print_text("MMR: " + str([doc.metadata["sku"] for doc in diverse]))


if __name__ == "__main__":
    run_cli(main)
