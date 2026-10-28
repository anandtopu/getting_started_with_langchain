"""Check installation, profiles and optional provider connectivity without printing secrets.

Run: uv run python scripts/check_env.py --offline
Expected: Python/package/data checks followed by OFFLINE CHECK PASSED. No API cost.
Without --offline, keys are checked locally and Ollama is probed without generating text.
"""

import argparse
import sys
from importlib.metadata import PackageNotFoundError, version

import httpx

from common.config import ConfigurationError, get_settings
from common.data import data_path
from common.errors import run_cli
from common.models import get_chat_model, get_embeddings
from common.pretty import print_text
from common.testing import offline_environment

PACKAGES = [
    "langchain",
    "langchain-core",
    "langgraph",
    "langchain-text-splitters",
    "langchain-openai",
    "langchain-anthropic",
    "langchain-google-genai",
    "langchain-ollama",
    "pydantic",
    "pydantic-settings",
    "langsmith",
    "numpy",
    "httpx",
    "rich",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Never contact any provider.")
    args = parser.parse_args()
    if not (3, 12) <= sys.version_info[:2] < (3, 15):
        raise ConfigurationError("Use Python 3.12, 3.13 or 3.14; 3.12 is recommended.")
    print_text(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    for package in PACKAGES:
        try:
            installed = version(package)
        except PackageNotFoundError:
            raise ConfigurationError(f"Missing {package}; run uv sync.") from None
        print_text(f"  {package}: {installed}")
    data_path("manifest.json")
    data_path("orders.db")
    settings = get_settings()
    if args.offline or settings.course_offline:
        with offline_environment():
            get_chat_model(offline=True).invoke("Installation check")
            get_embeddings(offline=True).embed_query("Installation check")
        print_text("OFFLINE CHECK PASSED. No provider, tracing or semantic quality was tested.")
        return
    providers = {settings.llm_provider, settings.embedding_provider}
    for provider in sorted(providers - {"ollama"}):
        settings.api_key(provider)
        print_text(f"{provider}: key configured (not validated with a paid call).")
    if "ollama" in providers:
        try:
            response = httpx.get(settings.ollama_base_url.rstrip("/") + "/api/tags", timeout=3)
            response.raise_for_status()
            names = {model["name"] for model in response.json()["models"]}
        except (httpx.HTTPError, ValueError, KeyError, TypeError):
            raise ConfigurationError(
                "Ollama is unavailable; start it and check OLLAMA_BASE_URL."
            ) from None
        required = []
        if settings.llm_provider == "ollama":
            required.append(settings.chat_model)
        if settings.embedding_provider == "ollama":
            required.append(settings.embedding_model)
        if any(name not in names and name + ":latest" not in names for name in required):
            raise ConfigurationError("An Ollama profile is not installed; pull the models in .env.")
        print_text("Ollama: server reachable and requested text/embedding models installed.")
    print_text("SETUP CHECK PASSED. Next: uv run python scripts/first_call.py")


if __name__ == "__main__":
    run_cli(main)
