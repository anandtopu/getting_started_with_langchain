"""The business application runs without credentials or external network."""

from pathlib import Path

import pytest

from common.testing import execute_script

FILES = sorted((Path(__file__).parents[1] / "use_case").glob("*.py"))


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_application(path):
    execute_script(path, ["--offline"])
