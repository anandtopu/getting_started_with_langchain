"""Capstones are optional in the foundation-only installation."""

from importlib.util import find_spec

import pytest


@pytest.fixture(autouse=True)
def capstone_dependencies(request, tmp_path, monkeypatch):
    required = ("rank_bm25", "pypdf", "matplotlib", "langgraph.checkpoint.sqlite", "fastmcp")
    if {"01_documind", "02_support_copilot"}.intersection(request.node.path.parts):
        required += ("fastapi", "streamlit")
    if any(find_spec(name) is None for name in required):
        pytest.skip("Install all capstones with uv sync --extra apps.")
    monkeypatch.setenv("RUNTIME_DIR", str(tmp_path))
