"""Generate bounded retrieval variants, retrieve each, and deduplicate by chunk identity.

Run: uv run --extra rag python modules/09_advanced_rag/examples/01_query_rewrite.py --offline
Expected: Standalone variants and a deduplicated evidence list.
Cost: One rewrite call; offline fixtures are not semantic query understanding.
Requires: rag
"""

from common.advanced_rag import rewrite
from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.retrieval import LexicalRetriever, fuse


def main() -> None:
    # KEY IDEA: Retain the original query so a mistaken rewrite cannot erase its retrieval path.
    settings = lesson_settings()
    queries = rewrite("How long is manufacturing defect coverage?", settings)
    retriever = LexicalRetriever(chunk_documents(policy_documents()))
    found = fuse([retriever.search(query) for query in queries])
    print_text(str(queries))
    print_text(str([d.id for d in found]))


if __name__ == "__main__":
    run_cli(main)
