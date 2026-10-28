"""Scope embedding cache keys. Task: Hash provider, model, dimension, query/document kind and
exact text into a stable cache key.

Run: uv run --extra rag python modules/07_embeddings_retrievers/exercises/03_stretch.py
--offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

import hashlib

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def cache_key(provider: str, model: str, dimensions: int, kind: str, text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# YOUR CODE HERE: improve the runnable baseline above to meet the target checks.


def main() -> None:
    lesson_settings()
    print_text(cache_key("fixture", "demo", 64, "query", "tent"))


if __name__ == "__main__":
    run_cli(main)
