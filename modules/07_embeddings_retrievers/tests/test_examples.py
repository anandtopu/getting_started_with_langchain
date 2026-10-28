"""All teaching scripts, exercise baselines and solutions run offline."""

import pytest

from common.config import ROOT
from common.testing import execute_script

HERE = ROOT / "modules/07_embeddings_retrievers"


@pytest.mark.parametrize(
    "path",
    sorted((HERE / "examples").glob("*.py"))
    + sorted((HERE / "exercises").glob("*.py"))
    + sorted((HERE / "solutions").glob("*.py")),
    ids=lambda p: p.parent.name + "-" + p.stem,
)
def test_script_runs(path):
    execute_script(path, ["--offline"])
