"""Translate a constrained query into a validated metadata filter.

Run: uv run --extra rag python modules/09_advanced_rag/examples/05_query_filters.py --offline
Expected: Only four-person tents under $300; no generated SQL is executed.
Cost: One extraction call plus product embeddings; offline is free.
Requires: rag
"""

from common.advanced_rag import extract_filter
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.retrieval import product_documents
from common.vector_index import persistent_index


def main() -> None:
    settings = lesson_settings()
    spec = extract_filter("Show four-person tents under $300", settings)
    where = {
        "$and": [
            {"category": spec.category},
            {"capacity": spec.capacity},
            {"price": {"$lt": spec.max_price}},
        ]
    }
    store = persistent_index(product_documents(), settings, name="lesson09-filters")
    # KEY IDEA: only allowlisted fields/operators are assembled by application code.
    print_text(str(where))
    print_text(
        str([doc.metadata for doc in store.similarity_search("waterproof tent", k=3, filter=where)])
    )


if __name__ == "__main__":
    run_cli(main)
