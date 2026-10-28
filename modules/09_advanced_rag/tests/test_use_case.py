"""Exercise the realistic application with isolated runtime outputs."""

from common.config import ROOT
from common.testing import execute_script


def test_application():
    execute_script(ROOT / "modules/09_advanced_rag/use_case/rag_benchmark.py", ["--offline"])
