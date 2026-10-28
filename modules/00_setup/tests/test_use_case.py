"""The realistic use case runs offline without changing committed data."""

from common.config import ROOT
from common.testing import execute_script


def test_use_case(tmp_path, monkeypatch):
    monkeypatch.setenv("RUNTIME_DIR", str(tmp_path))
    execute_script(ROOT / "modules/00_setup/use_case/first_call.py", ["--offline"])
