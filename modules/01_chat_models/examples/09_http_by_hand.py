"""Build an OpenAI or Ollama HTTP call, then use the central LangChain factory.

Run: uv run python modules/01_chat_models/examples/09_http_by_hand.py --offline
Expected: The mock raw API and LangChain both return a greeting in offline mode.
Cost: Two short hosted calls, typically under $0.01; local and offline have no API fee.
"""

import httpx

from common.config import ConfigurationError
from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message, print_text


def mock_chat(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/v1/responses":
        return httpx.Response(
            200,
            json={
                "status": "completed",
                "output": [
                    {
                        "type": "message",
                        "content": [{"type": "output_text", "text": "Welcome to Brightwave."}],
                    }
                ],
            },
        )
    return httpx.Response(
        200,
        json={"message": {"role": "assistant", "content": "Welcome to Brightwave."}, "done": True},
    )


def main() -> None:
    settings = lesson_settings()
    if settings.llm_provider not in {"openai", "ollama"}:
        raise ConfigurationError(
            "This wire-protocol lesson supports OpenAI and Ollama. "
            "Set LLM_PROVIDER=openai or ollama; other lessons use the common adapter."
        )
    transport = httpx.MockTransport(mock_chat) if settings.course_offline else None
    messages = [{"role": "user", "content": "Greet a Brightwave customer in one sentence."}]
    # KEY IDEA: by hand, we own endpoint, JSON, HTTP status, timeout and response parsing.
    with httpx.Client(
        transport=transport, timeout=settings.model_timeout, trust_env=False
    ) as client:
        if settings.llm_provider == "ollama":
            url = settings.ollama_base_url.rstrip("/") + "/api/chat"
            headers = {}
            payload = {
                "model": settings.chat_model,
                "messages": messages,
                "stream": False,
                "options": {"num_predict": 96, "temperature": 0},
            }
        else:
            url = "https://api.openai.com/v1/responses"
            headers = (
                {}
                if settings.course_offline
                else {"Authorization": "Bearer " + settings.api_key("openai")}
            )
            payload = {
                "model": settings.chat_model,
                "input": messages,
                "store": False,
                "max_output_tokens": settings.model_max_tokens,
                "reasoning": {"effort": settings.openai_reasoning_effort},
            }
        reply = client.post(url, headers=headers, json=payload)
        reply.raise_for_status()
        result = reply.json()
        if settings.llm_provider == "ollama":
            text = result["message"]["content"]
        else:
            if result.get("status") != "completed":
                raise ConfigurationError("Response incomplete; inspect the output-token budget.")
            text = "".join(
                block["text"]
                for item in result["output"]
                if item["type"] == "message"
                for block in item["content"]
                if block["type"] == "output_text"
            )
        print_text("Raw HTTP: " + text)
    print_message(
        get_chat_model(settings=settings, responses=["Welcome to Brightwave."]).invoke(messages)
    )


if __name__ == "__main__":
    run_cli(main)
