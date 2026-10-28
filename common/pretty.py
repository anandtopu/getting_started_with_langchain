"""Readable, credential-redacted messages, tool calls, streams and estimated usage."""

import json
import re
from collections.abc import Iterable
from typing import Any

from langchain_core.messages import BaseMessage
from pydantic import SecretStr
from rich.console import Console

from common.config import Settings, get_settings

console = Console()


def redact(text: str, settings: Settings | None = None) -> str:
    """Redact configured secrets before output; this is not the later PII guardrail."""
    config = settings or get_settings()
    secrets = [
        value.get_secret_value()
        for value in config.__dict__.values()
        if isinstance(value, SecretStr) and value.get_secret_value()
    ]
    for secret in sorted(secrets, key=len, reverse=True):
        text = text.replace(secret, "[REDACTED]")
    return re.sub(r"\b(?:sk-|AIza)[A-Za-z0-9_\-]{8,}", "[REDACTED]", text)


def print_text(text: str, *, settings: Settings | None = None) -> None:
    """Treat model output as data, not Rich markup or terminal control sequences."""
    safe = redact(text, settings)
    safe = re.sub(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*\x07)", "", safe)
    console.print(safe, markup=False, highlight=False)


def message_text(message: BaseMessage) -> str:
    """Do not mistake a multimodal list for an ordinary text string."""
    if isinstance(message.content, str):
        return message.content
    return "".join(
        block if isinstance(block, str) else str(block.get("text", "")) for block in message.content
    )


def print_message(message: BaseMessage, *, settings: Settings | None = None) -> None:
    """Show readable content and any model-requested tool calls."""
    print_text(f"{message.type}: {message_text(message)}", settings=settings)
    for call in getattr(message, "tool_calls", []):
        print_text(f"tool request: {json.dumps(call, ensure_ascii=False)}", settings=settings)


def print_stream(chunks: Iterable[BaseMessage]) -> str:
    """Print complete lines so a secret split across network chunks is still redacted."""
    pending = ""
    complete: list[str] = []
    for chunk in chunks:
        text = message_text(chunk)
        complete.append(text)
        pending += text
        while "\n" in pending:
            line, pending = pending.split("\n", 1)
            print_text(line)
    if pending:
        print_text(pending)
    return "".join(complete)


def estimate_cost(usage: dict[str, Any] | None, config: Settings) -> float | None:
    """Estimate standard token cost only for the exact configured pricing profile."""
    if not usage or config.llm_provider != "openai" or config.chat_model != config.cost_model:
        return None
    if "input_tokens" not in usage or "output_tokens" not in usage:
        return None
    return (
        usage["input_tokens"] * config.cost_input_per_million
        + usage["output_tokens"] * config.cost_output_per_million
    ) / 1_000_000


def print_usage(message: BaseMessage, *, settings: Settings | None = None) -> None:
    """Missing usage or a model override must never be presented as zero real cost."""
    config = settings or get_settings()
    usage = getattr(message, "usage_metadata", None)
    estimate = estimate_cost(usage, config)
    if config.course_offline:
        print_text("OFFLINE FIXTURE: no model API fee; not a quality measurement.")
    elif config.llm_provider == "ollama":
        print_text(f"Local inference: no API fee. Usage: {usage or 'not reported'}")
    else:
        label = f"${estimate:.6f}" if estimate is not None else "unknown"
        print_text(f"Usage: {usage or 'not reported'}; estimated standard token cost: {label}.")
