"""Execute finite capstone CLIs and starters with explicit optional-install skips."""

from importlib.util import find_spec

import pytest

from common.config import ROOT
from common.testing import execute_script

FILES = sorted((ROOT / "capstones").glob("*/*.py"))


@pytest.mark.parametrize("path", FILES, ids=lambda path: path.parent.name + "/" + path.name)
def test_capstone_script(path, tmp_path, monkeypatch):
    if any(
        find_spec(name) is None
        for name in ("fastapi", "streamlit", "fastmcp", "rank_bm25", "pypdf", "matplotlib")
    ):
        pytest.skip("Install capstone dependencies with uv sync --extra apps.")
    monkeypatch.setenv("RUNTIME_DIR", str(tmp_path))
    execute_script(path, ["--offline"])
