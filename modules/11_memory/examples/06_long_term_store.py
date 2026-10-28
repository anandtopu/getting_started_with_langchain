"""Scope a semantic preference store by authenticated customer.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/11_memory/examples/06_long_term_store.py --offline
Expected: Only C001 namespace results appear; fake-vector scores are not semantic evidence.
Cost: Embedding calls only; offline no API fee.
Requires: agents
"""

from langgraph.store.memory import InMemoryStore

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_embeddings
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    embeddings = get_embeddings(settings=settings)
    # KEY IDEA: namespace filtering is authorization scope; vector ranking is only relevance.
    store = InMemoryStore(
        index={
            "dims": len(embeddings.embed_query("dimension probe")),
            "embed": embeddings,
            "fields": ["text"],
        }
    )
    store.put(("customers", "C001"), "shipping", {"text": "Prefers standard shipping"})
    store.put(("customers", "C002"), "shipping", {"text": "Prefers expedited shipping"})
    results = store.search(("customers", "C001"), query="delivery preference", limit=2)
    print_text(str([(r.namespace, r.value, r.score) for r in results]))
    print_text("InMemoryStore does not survive a process restart. Fake ranking is non-semantic.")


if __name__ == "__main__":
    run_cli(main)
