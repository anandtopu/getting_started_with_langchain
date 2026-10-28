"""Score a bounded candidate set and validate model-selected verbatim extracts.

Run: uv run --extra rag python modules/09_advanced_rag/examples/03_rerank_compress.py --offline
Expected: At most two relevant extracts, each copied from its original evidence.
Cost: Up to four reranking calls here; helper caps candidates at six. Offline is free.
Requires: rag
"""

from common.advanced_rag import rerank_compress
from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.retrieval import LexicalRetriever


def main() -> None:
    # KEY IDEA: Bound reranking calls and reject extracts that change the source text.
    settings = lesson_settings()
    question = "When is manager approval required?"
    candidates = LexicalRetriever(chunk_documents(policy_documents())).search(question, k=4)
    for doc in rerank_compress(question, candidates, settings):
        print_text(doc.page_content)
    print_text("Exact extraction protects provenance; it does not prove semantic relevance.")


if __name__ == "__main__":
    run_cli(main)
