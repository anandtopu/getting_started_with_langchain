"""Narrow transient failures eligible for the foundation fallback demonstration."""

import httpx
from anthropic import APIConnectionError as AnthropicConnectionError
from anthropic import RateLimitError as AnthropicRateLimitError
from google.genai.errors import ServerError as GeminiServerError
from openai import APIConnectionError as OpenAIConnectionError
from openai import RateLimitError as OpenAIRateLimitError

TRANSIENT_ERRORS = (
    TimeoutError,
    httpx.TransportError,
    OpenAIConnectionError,
    OpenAIRateLimitError,
    AnthropicConnectionError,
    AnthropicRateLimitError,
    GeminiServerError,
)
