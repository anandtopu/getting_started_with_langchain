"""Run standalone lessons and exercise baselines with networking disabled."""

from importlib.util import find_spec
from pathlib import Path

import pytest

from common.testing import execute_script

MODULE = Path(__file__).parents[1]
FILES = sorted(
    p for folder in ("examples", "exercises", "solutions") for p in (MODULE / folder).glob("*.py")
)


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.parent.name + "/" + p.name)
def test_script(path):
    if "Requires: deep" in path.read_text(encoding="utf-8") and find_spec("deepagents") is None:
        pytest.skip("Install optional SDK with uv sync --extra deep.")
    execute_script(path, ["--offline"])
