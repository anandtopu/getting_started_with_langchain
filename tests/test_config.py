"""Configuration precedence, provider switching and secret-safe diagnostics."""

from pathlib import Path

import pytest
from pydantic import SecretStr

from common.config import ConfigurationError, Settings, get_settings


def test_one_line_switch_changes_both_profiles(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.delenv("EMBEDDINGS_PROVIDER", raising=False)
    monkeypatch.delenv("EMBEDDINGS_MODEL", raising=False)
    settings = get_settings()
    assert settings.chat_model == settings.ollama_chat_model
    assert settings.embedding_provider == "ollama"
    assert settings.embedding_model == settings.ollama_embeddings_model


def test_environment_overrides_dotenv(tmp_path: Path, monkeypatch):
    dotenv = tmp_path / ".env"
    dotenv.write_text("LLM_PROVIDER=anthropic\nLLM_MODEL=file-model\n", encoding="utf-8")
    monkeypatch.setenv("LLM_MODEL", "environment-model")
    settings = Settings(_env_file=dotenv)
    assert settings.chat_model == "environment-model"
    assert settings.llm_provider == "anthropic"


def test_independent_embeddings():
    settings = Settings(
        llm_provider="anthropic",
        embeddings_provider="google_genai",
        embeddings_model="custom-embedding",
    )
    assert settings.embedding_provider == "google_genai"
    assert settings.embedding_model == "custom-embedding"


def test_blank_profile_is_actionable():
    with pytest.raises(ConfigurationError, match="LLM_MODEL"):
        _ = Settings(_env_file=None).chat_model


def test_key_missing_is_safe():
    with pytest.raises(ConfigurationError, match="OPENAI_API_KEY"):
        Settings(_env_file=None).api_key("openai")


def test_secrets_hidden_in_repr_and_json():
    settings = Settings(openai_api_key=SecretStr("test-secret-never-print"))
    assert "test-secret-never-print" not in repr(settings)
    assert "test-secret-never-print" not in settings.model_dump_json()


def test_invalid_settings_do_not_echo_values(monkeypatch):
    monkeypatch.setenv("MODEL_TIMEOUT", "test-secret-never-print")
    with pytest.raises(ConfigurationError) as caught:
        get_settings()
    assert "MODEL_TIMEOUT" in str(caught.value)
    assert "test-secret-never-print" not in str(caught.value)
