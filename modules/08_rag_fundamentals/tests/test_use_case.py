"""Exercise the realistic application with isolated runtime outputs."""

from common.config import ROOT
from common.testing import execute_script


def test_application():
    execute_script(ROOT / "modules/08_rag_fundamentals/use_case/ask_brightwave.py", ["--offline"])
