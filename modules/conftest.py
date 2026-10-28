"""Optional retrieval lessons skip explicitly in the minimal foundations install."""

from importlib.util import find_spec

import pytest


@pytest.fixture(autouse=True)
def retrieval_dependencies(request, tmp_path, monkeypatch):
    if {"18_apps", "20_production"}.intersection(request.node.path.parts):
        if any(
            find_spec(name) is None
            for name in ("fastapi", "streamlit", "rank_bm25", "langgraph.checkpoint.sqlite")
        ):
            pytest.skip("Install app lessons with uv sync --extra apps.")
        monkeypatch.setenv("RUNTIME_DIR", str(tmp_path))
        return
    agent_modules = {
        "19_evaluation",
        "10_agents",
        "11_memory",
        "12_middleware",
        "13_mcp",
        "14_langgraph",
        "15_workflows",
        "16_multi_agent",
        "17_deep_agents",
    }
    if agent_modules.intersection(request.node.path.parts):
        if any(
            find_spec(name) is None
            for name in ("fastmcp", "mcp", "langgraph.checkpoint.sqlite", "rank_bm25", "pypdf")
        ):
            pytest.skip("Install agent lessons with uv sync --extra agents.")
        monkeypatch.setenv("RUNTIME_DIR", str(tmp_path))
        return
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
