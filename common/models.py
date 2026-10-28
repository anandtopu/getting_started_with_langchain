"""One provider-neutral entry point for real models and explicitly selected test fakes."""

from collections.abc import Iterable
from itertools import repeat
from typing import Any

from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from langchain_core.embeddings import DeterministicFakeEmbedding, Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage

from common.config import Settings, get_settings
from common.fixtures import ScriptedChatModel

FIXTURE_REPLY = (
    "Brightwave Outfitters offers 30-day returns for unused gear with proof of purchase."
)


def get_chat_model(
    *,
    settings: Settings | None = None,
    offline: bool | None = None,
    responses: Iterable[str | AIMessage] | None = None,
    temperature: float | None = None,
    vision: bool = False,
) -> BaseChatModel:
    """Construct a chat model; configuration failures never silently become fake replies.

    Scripted responses are for tests, not semantic evaluation. A finite response iterator
    intentionally fails on exhaustion so an unexpected extra model call is detectable.
    """
    config = settings or get_settings()
    use_fake = config.course_offline if offline is None else offline
    if use_fake:
        return ScriptedChatModel(
            messages=iter(responses) if responses is not None else repeat(FIXTURE_REPLY)
        )
    provider = config.llm_provider
    model = config.ollama_vision_model if vision and provider == "ollama" else config.chat_model
    sampling = config.model_temperature if temperature is None else temperature
    options: dict[str, Any] = {}
    if provider == "ollama":
        options.update(
            base_url=config.ollama_base_url,
            temperature=sampling,
            num_predict=config.model_max_tokens,
            client_kwargs={"timeout": config.model_timeout},
        )
    else:
        options.update(
            api_key=config.api_key(provider),
            max_tokens=config.model_max_tokens,
            timeout=config.model_timeout,
            max_retries=config.model_max_retries,
        )
        if getattr(config, f"{provider}_temperature_supported"):
            options["temperature"] = sampling
        if provider == "openai":
            options["use_responses_api"] = config.openai_use_responses_api
            options["reasoning_effort"] = config.openai_reasoning_effort
            if config.openai_reasoning_effort != "none":
                options.pop("temperature", None)
    # KEY IDEA: provider-specific parameters stop here; lessons consume a chat interface.
    return init_chat_model(model, model_provider=provider, **options)


def get_embeddings(*, settings: Settings | None = None, offline: bool | None = None) -> Embeddings:
    """Create independent embeddings; deterministic fake vectors have no semantic meaning."""
    config = settings or get_settings()
    if config.course_offline if offline is None else offline:
        return DeterministicFakeEmbedding(size=64)
    provider = config.embedding_provider
    options: dict[str, Any] = {}
    if provider == "ollama":
        options.update(
            base_url=config.ollama_base_url,
            client_kwargs={"timeout": config.model_timeout},
        )
    else:
        options["api_key"] = config.api_key(provider)
        if provider == "openai":
            options.update(timeout=config.model_timeout, max_retries=config.model_max_retries)
        else:
            options["request_options"] = {"timeout": config.model_timeout}
    return init_embeddings(config.embedding_model, provider=provider, **options)
