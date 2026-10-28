"""Send a local synthetic product image through standard content blocks.

Run: uv run python modules/01_chat_models/examples/07_multimodal.py --offline
Expected: A description of the simple tent drawing; never a claim about real product quality.
Cost: One image call; price depends on image tokens, typically cents; fixtures are free.
"""

import base64

import httpx
from langchain_core.messages import HumanMessage

from common.config import ConfigurationError
from common.data import data_path
from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message, print_text


def main() -> None:
    settings = lesson_settings()
    if settings.llm_provider == "ollama" and not settings.course_offline:
        response = httpx.post(
            settings.ollama_base_url.rstrip("/") + "/api/show",
            json={"model": settings.ollama_vision_model},
            timeout=5,
        )
        response.raise_for_status()
        if "vision" not in response.json().get("capabilities", []):
            raise ConfigurationError(
                "Pull the vision model in .env; the selected model lacks vision."
            )
    encoded = base64.b64encode(data_path("fixtures/product.png").read_bytes()).decode("ascii")
    message = HumanMessage(
        content_blocks=[
            {
                "type": "text",
                "text": "Describe only visible shapes in this Brightwave tent illustration.",
            },
            {"type": "image", "base64": encoded, "mime_type": "image/png"},
        ]
    )
    print_text(f"Input block types: {[block['type'] for block in message.content_blocks]}")
    # KEY IDEA: a text-only model cannot infer image pixels from their filename.
    print_message(
        get_chat_model(
            settings=settings,
            vision=True,
            responses=["A teal triangular tent on a light background."],
        ).invoke(message.content and [message])
    )


if __name__ == "__main__":
    run_cli(main)
