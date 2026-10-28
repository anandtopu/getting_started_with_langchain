"""Fuse BM25 and vector rankings by rank rather than incompatible scores.

Run: uv run --extra rag python modules/09_advanced_rag/examples/02_hybrid.py --offline
Expected: A deduplicated hybrid list; fake-vector ranking is explicitly non-semantic.
Cost: Offline: no API fees. Live embeddings depend on corpus size and the chosen provider.
Requires: rag
"""

from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.retrieval import LexicalRetriever, fuse, memory_index


def main() -> None:
    settings = lesson_settings()
    chunks = chunk_documents(policy_documents())
    lexical, vectors = LexicalRetriever(chunks), memory_index(chunks, settings)
    question = "unused gear return time limit"
    # KEY IDEA: reciprocal rank fusion uses 1/(60+rank), not addition of raw distances.
    results = fuse([lexical.search(question), vectors.similarity_search(question, k=3)])
    print_text(str([d.metadata for d in results]))
    if settings.course_offline:
        print_text(
            "Fake-vector fusion verifies mechanics only; the benchmark excludes fake vectors."
        )


if __name__ == "__main__":
    run_cli(main)
