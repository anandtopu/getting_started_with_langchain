"""Validated configuration: process environment > .env > commented provider profiles."""

import os
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(os.environ.get("BRIGHTWAVE_ROOT") or Path(__file__).resolve().parents[1]).resolve()
Provider = Literal["openai", "anthropic", "google_genai", "ollama"]


class ConfigurationError(ValueError):
    """An actionable setup problem; safe to show without a traceback."""


class Settings(BaseSettings):
    """Changing model names live in .env.example, not in application code."""

    model_config = SettingsConfigDict(
        env_file=(ROOT / ".env.example", ROOT / ".env"),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        hide_input_in_errors=True,
    )
    llm_provider: Provider = "openai"
    llm_model: str = ""
    embeddings_provider: Literal["auto", "openai", "google_genai", "ollama"] = "auto"
    embeddings_model: str = ""
    course_offline: bool = False
    runtime_dir: Path = Path(".runtime")
    model_timeout: float = Field(default=30, gt=0, le=300)
    model_max_retries: int = Field(default=2, ge=0, le=5)
    model_max_tokens: int = Field(default=512, gt=0, le=8192)
    model_temperature: float = Field(default=0, ge=0, le=2)
    openai_chat_model: str = ""
    anthropic_chat_model: str = ""
    google_genai_chat_model: str = ""
    ollama_chat_model: str = ""
    ollama_vision_model: str = ""
    openai_embeddings_model: str = ""
    google_genai_embeddings_model: str = ""
    ollama_embeddings_model: str = ""
    openai_use_responses_api: bool = True
    openai_reasoning_effort: str = "none"
    openai_temperature_supported: bool = True
    anthropic_temperature_supported: bool = False
    google_genai_temperature_supported: bool = True
    ollama_base_url: str = "http://localhost:11434"
    openai_api_key: SecretStr = Field(default=SecretStr(""), repr=False)
    anthropic_api_key: SecretStr = Field(default=SecretStr(""), repr=False)
    google_api_key: SecretStr = Field(default=SecretStr(""), repr=False)
    tavily_api_key: SecretStr = Field(default=SecretStr(""), repr=False)
    langsmith_tracing: bool = False
    langsmith_api_key: SecretStr = Field(default=SecretStr(""), repr=False)
    langsmith_project: str = "brightwave-course"
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    postgres_uri: SecretStr = Field(default=SecretStr(""), repr=False)
    cost_model: str = ""
    cost_input_per_million: float = Field(default=0, ge=0)
    cost_output_per_million: float = Field(default=0, ge=0)
    max_run_cost_usd: float = Field(default=0.05, gt=0)
    api_customer_token: SecretStr = Field(default=SecretStr(""), repr=False)
    api_manager_token: SecretStr = Field(default=SecretStr(""), repr=False)
    api_customer_id: str = "C001"
    api_base_url: str = "http://127.0.0.1:8000"
    api_request_timeout: float = Field(default=45, gt=0, le=120)

    @property
    def chat_model(self) -> str:
        name = self.llm_model or getattr(self, f"{self.llm_provider}_chat_model")
        if not name:
            raise ConfigurationError("Set LLM_MODEL or the provider profile in .env.example.")
        return name

    @property
    def embedding_provider(self) -> str:
        if self.embeddings_provider != "auto":
            return self.embeddings_provider
        return "ollama" if self.llm_provider == "ollama" else "openai"

    @property
    def embedding_model(self) -> str:
        name = self.embeddings_model or getattr(self, f"{self.embedding_provider}_embeddings_model")
        if not name:
            raise ConfigurationError("Set EMBEDDINGS_MODEL or its provider profile.")
        return name

    def api_key(self, provider: str) -> str:
        field = "google_api_key" if provider == "google_genai" else f"{provider}_api_key"
        key = getattr(self, field).get_secret_value()
        if not key:
            raise ConfigurationError(f"Set {field.upper()} in .env for {provider}.")
        return key


def get_settings() -> Settings:
    """Read fresh settings so notebook edits take effect without restarting Python."""
    try:
        return Settings()
    except ValidationError as exc:
        fields = ", ".join(str(e["loc"][0]).upper() for e in exc.errors())
        raise ConfigurationError(
            f"Invalid configuration for: {fields}. Check .env.example."
        ) from None
