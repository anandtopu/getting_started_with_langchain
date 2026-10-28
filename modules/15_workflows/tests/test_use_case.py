"""Run the complete module application offline."""

from pathlib import Path

import pytest

from common.testing import execute_script


@pytest.mark.parametrize("path", sorted((Path(__file__).parents[1] / "use_case").glob("*.py")))
def test_application(path):
    execute_script(path, ["--offline"])
