"""Reopen a local Chroma collection only when its manifest matches.

Run: uv run --extra rag python
modules/07_embeddings_retrievers/examples/04_persistent_chroma.py --offline
Expected: The same stored document IDs before and after reopening.
Cost: Offline: no API fees. Live embeddings depend on corpus size and the chosen provider.
Requires: rag
"""

from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.vector_index import persistent_index


def main() -> None:
    settings = lesson_settings()
    documents = chunk_documents(policy_documents())
    first = persistent_index(documents, settings, name="lesson07-persistence")
    second = persistent_index(documents, settings, name="lesson07-persistence")
    # KEY IDEA: persistence is automatic; model/dimension/corpus identity is our responsibility.
    assert set(first.get()["ids"]) == set(second.get()["ids"])
    print_text(f"Reopened {len(second.get()['ids'])} documents without re-adding the corpus.")


if __name__ == "__main__":
    run_cli(main)
