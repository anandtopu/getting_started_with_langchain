"""User-facing first call and setup errors, with no secrets and no network."""

import sys
from pathlib import Path

import pytest

from common.config import ROOT
from common.testing import execute_script
from scripts.run_all_examples import targets


def test_first_call_offline(capsys):
    execute_script(ROOT / "scripts/first_call.py", ["--offline"])
    output = capsys.readouterr().out
    assert "OFFLINE FIXTURE" in output
    assert "30-day" in output


def test_environment_offline(capsys):
    execute_script(ROOT / "scripts/check_env.py", ["--offline"])
    assert "OFFLINE CHECK PASSED" in capsys.readouterr().out


def test_missing_live_key_exits_cleanly(monkeypatch, capsys):
    from common.config import ConfigurationError
    from common.errors import run_cli

    def missing_key():
        raise ConfigurationError("Set OPENAI_API_KEY in .env.")

    with pytest.raises(SystemExit) as caught:
        run_cli(missing_key)
    assert caught.value.code == 1
    output = capsys.readouterr().err
    assert "scripts/check_env.py" in output
    assert "Traceback" not in output


def test_provider_error_does_not_print_body(capsys):
    from common.errors import run_cli

    def failure():
        raise RuntimeError("Authorization: secret-example-key")

    with pytest.raises(SystemExit):
        run_cli(failure)
    assert "secret-example-key" not in capsys.readouterr().err


def test_smoke_discovers_new_examples(tmp_path: Path):
    example = tmp_path / "modules/01_chat_models/examples/01_hello.py"
    example.parent.mkdir(parents=True)
    example.write_text("print('fixture')", encoding="utf-8")
    assert (example, []) in targets(tmp_path, False)


def test_configure_preserves_existing_file(tmp_path: Path, monkeypatch, capsys):
    from scripts import configure

    script = tmp_path / "scripts/configure.py"
    script.parent.mkdir()
    monkeypatch.setattr(configure, "__file__", str(script))
    (tmp_path / ".env.example").write_text("LLM_PROVIDER=ollama\n", encoding="utf-8")
    configure.main()
    (tmp_path / ".env").write_text("PRIVATE_KEY=do-not-overwrite\n", encoding="utf-8")
    configure.main()
    assert (tmp_path / ".env").read_text() == "PRIVATE_KEY=do-not-overwrite\n"
    assert "do-not-overwrite" not in capsys.readouterr().out


def test_worker_restores_arguments():
    before = sys.argv
    execute_script(ROOT / "scripts/check_env.py", ["--offline"])
    assert sys.argv is before


def test_offline_cli_overrides_ambient_tracing(monkeypatch):
    import os

    from common.errors import run_cli

    monkeypatch.setattr(sys, "argv", ["lesson.py", "--offline"])
    monkeypatch.setenv("LANGSMITH_TRACING", "true")
    observed = []
    run_cli(lambda: observed.append(os.environ["LANGSMITH_TRACING"]))
    assert observed == ["false"]
    assert os.environ["LANGSMITH_TRACING"] == "true"
