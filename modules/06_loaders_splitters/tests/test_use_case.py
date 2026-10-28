"""Exercise the realistic application with isolated runtime outputs."""

from common.config import ROOT
from common.testing import execute_script


def test_application():
    execute_script(
        ROOT / "modules/06_loaders_splitters/use_case/knowledge_ingest.py", ["--offline"]
    )
