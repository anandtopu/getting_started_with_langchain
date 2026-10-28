"""Exercise actual factories and fake interfaces without any external request."""

import socket

import pytest
from langchain_core.messages import AIMessage

from common.config import Settings
from common.models import get_chat_model, get_embeddings


def test_fake_invoke_batch_stream():
    model = get_chat_model(responses=["one", "two", "three", "four five"])
    assert model.invoke("ignored").content == "one"
    assert [m.content for m in model.batch(["a", "b"], config={"max_concurrency": 1})] == [
        "two",
        "three",
    ]
    assert "".join(chunk.content for chunk in model.stream("ignored")) == "four five"


@pytest.mark.asyncio
async def test_fake_async():
    result = await get_chat_model(responses=["async reply"]).ainvoke("hello")
    assert result.content == "async reply"


def test_scripted_tool_call_message():
    scripted = AIMessage(
        content="", tool_calls=[{"name": "check_stock", "args": {"sku": "BW-001"}, "id": "call-1"}]
    )
    result = get_chat_model(responses=[scripted]).invoke("stock?")
    assert result.tool_calls[0]["args"] == {"sku": "BW-001"}
    # This verifies a message fixture, not an unimplemented bind_tools provider adapter.


def test_fake_embeddings_repeatable():
    first = get_embeddings()
    second = get_embeddings()
    assert first.embed_query("tent") == second.embed_documents(["tent"])[0]
    assert first.embed_query("tent") != first.embed_query("boot")
    assert len(first.embed_query("tent")) == 64


@pytest.mark.parametrize("provider", ["openai", "anthropic", "google_genai", "ollama"])
def test_real_chat_factory_constructs_without_network(provider):
    settings = Settings(
        llm_provider=provider,
        course_offline=False,
        openai_api_key="test-not-a-real-key",
        anthropic_api_key="test-not-a-real-key",
        google_api_key="test-not-a-real-key",
    )
    model = get_chat_model(settings=settings)
    assert model is not None
    if provider == "anthropic":
        assert model.temperature is None
    if provider == "openai":
        assert model.use_responses_api is True
        assert model.reasoning_effort == "none"
    if provider == "ollama":
        assert model.num_predict == settings.model_max_tokens


@pytest.mark.parametrize("provider", ["openai", "google_genai", "ollama"])
def test_real_embedding_factory_constructs_without_network(provider):
    model = get_embeddings(
        settings=Settings(
            course_offline=False,
            embeddings_provider=provider,
            openai_api_key="test-not-a-real-key",
            google_api_key="test-not-a-real-key",
        )
    )
    assert callable(model.embed_query)


def test_reasoning_omits_temperature():
    model = get_chat_model(
        settings=Settings(
            course_offline=False,
            openai_reasoning_effort="low",
            openai_api_key="test-not-a-real-key",
        )
    )
    assert model.temperature is None


def test_network_denial_includes_localhost():
    with pytest.raises(RuntimeError, match="Network disabled"):
        socket.create_connection(("127.0.0.1", 11434))
