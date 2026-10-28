"""Run examples and runnable exercise baselines with network denied."""

from pathlib import Path

import pytest

from common.testing import execute_script

MODULE = Path(__file__).parents[1]
FILES = sorted(
    p for folder in ("examples", "exercises", "solutions") for p in (MODULE / folder).glob("*.py")
)


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.parent.name + "/" + p.name)
def test_script(path):
    execute_script(path, ["--offline"])
