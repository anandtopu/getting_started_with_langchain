"""Run every use-case CLI entry point in finite offline mode."""

from pathlib import Path

import pytest

from common.testing import execute_script


@pytest.mark.parametrize("path", sorted((Path(__file__).parents[1] / "use_case").glob("*.py")))
def test_use_case(path):
    execute_script(path, ["--offline"])
