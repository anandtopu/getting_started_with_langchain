"""Scope embedding cache keys. Task: Hash provider, model, dimension, query/document kind and
exact text into a stable cache key.

Run: uv run --extra rag python modules/07_embeddings_retrievers/solutions/03_stretch.py
--offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

import hashlib
import json

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def cache_key(provider: str, model: str, dimensions: int, kind: str, text: str) -> str:
    if dimensions < 1 or kind not in {"query", "document"}:
        raise ValueError("Invalid cache identity")
    return hashlib.sha256(
        json.dumps([provider, model, dimensions, kind, text]).encode()
    ).hexdigest()


def main() -> None:
    lesson_settings()
    print_text(cache_key("fixture", "demo", 64, "query", "tent"))


if __name__ == "__main__":
    run_cli(main)
