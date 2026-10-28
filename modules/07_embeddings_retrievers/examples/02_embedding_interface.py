"""Use independent embedding configuration through embed_query and embed_documents.

Run: uv run --extra rag python
modules/07_embeddings_retrievers/examples/02_embedding_interface.py --offline
Expected: Two document vectors and a query vector with matching dimensions.
Cost: Offline: no API fees. Live embeddings depend on corpus size and the chosen provider.
Requires: rag
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_embeddings
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    embeddings = get_embeddings(settings=settings)
    documents = embeddings.embed_documents(
        ["Waterproof Brightwave tent", "Brightwave hiking boots"]
    )
    query = embeddings.embed_query("shelter for a rainy trip")
    # KEY IDEA: query/document APIs may use different task prefixes inside a provider.
    print_text(f"Document vectors={len(documents)}, dimensions={len(query)}")
    print_text(
        "Fake embeddings are repeatable random vectors, not semantic representations."
        if settings.course_offline
        else f"Embedding provider: {settings.embedding_provider}; model: {settings.embedding_model}"
    )


if __name__ == "__main__":
    run_cli(main)
