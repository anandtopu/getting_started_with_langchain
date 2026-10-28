"""Cache vectors by model identity, dimension, input text and query/document task.

Run: uv run --extra rag python modules/07_embeddings_retrievers/examples/08_embedding_cache.py
--offline
Expected: Repeated query vectors match; cache survives another wrapper instance.
Cost: Offline: no API fees. Live embeddings depend on corpus size and the chosen provider.
Requires: rag
"""

from common.config import ROOT
from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_embeddings
from common.pretty import print_text
from common.vector_index import CachedEmbeddings, embedding_identity


def main() -> None:
    # KEY IDEA: Reuse vectors only when text, operation kind and embedding identity all match.
    settings = lesson_settings()
    wrapped = get_embeddings(settings=settings)
    dimensions = len(wrapped.embed_query("dimension probe"))
    identity = embedding_identity(settings, dimensions)
    cache = CachedEmbeddings(wrapped, ROOT / settings.runtime_dir / "embeddings.sqlite", identity)
    first = cache.embed_query("Brightwave waterproof tent")
    second = cache.embed_query("Brightwave waterproof tent")
    assert first == second
    print_text(f"Cached vector dimensions={len(first)}; identity={identity}")


if __name__ == "__main__":
    run_cli(main)
