"""Inspect the evidence retrieved before any answer is generated.

Run: uv run --extra rag python modules/08_rag_fundamentals/examples/01_index_retrieve.py
--offline
Expected: Three evidence chunks with source, IDs and optional PDF page.
Cost: No model calls or API fees.
Requires: rag
"""

from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.rag import context_text
from common.retrieval import LexicalRetriever


def main() -> None:
    # KEY IDEA: Inspect retrieved evidence before asking a model to use it.
    lesson_settings()
    index = LexicalRetriever(chunk_documents(policy_documents()))
    print_text(context_text(index.search("What is the return window?", k=3)))


if __name__ == "__main__":
    run_cli(main)
