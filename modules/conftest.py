"""Optional retrieval lessons skip explicitly in the minimal foundations install."""

from importlib.util import find_spec

import pytest


@pytest.fixture(autouse=True)
def retrieval_dependencies(request, tmp_path, monkeypatch):
    retrieval_modules = {
        "06_loaders_splitters",
        "07_embeddings_retrievers",
        "08_rag_fundamentals",
        "09_advanced_rag",
    }
    if not retrieval_modules.intersection(request.node.path.parts):
        return
    if any(
        find_spec(name) is None for name in ("pypdf", "rank_bm25", "langchain_chroma", "matplotlib")
    ):
        pytest.skip("Install retrieval lessons with uv sync --extra rag.")
    monkeypatch.setenv("RUNTIME_DIR", str(tmp_path))
