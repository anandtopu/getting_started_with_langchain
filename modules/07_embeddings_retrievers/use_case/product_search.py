"""Enforce catalogue constraints before ranking waterproof four-person tents under $300.

Run: uv run --extra rag python modules/07_embeddings_retrievers/use_case/product_search.py
--offline
Expected: Up to three matching tents, each strictly under $300 and exactly four-person.
Cost: Offline: no API fees. Live embeddings depend on corpus size and the chosen provider.
Requires: rag
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.retrieval import product_search


def main() -> None:
    settings = lesson_settings()
    for doc in product_search(settings):
        print_text(str(doc.metadata))
    print_text("Constraints are real. Offline ranking uses non-semantic fake vectors.")


if __name__ == "__main__":
    run_cli(main)
