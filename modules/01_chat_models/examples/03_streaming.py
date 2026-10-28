"""Consume incremental message chunks and reconstruct a complete response.

Run: uv run python modules/01_chat_models/examples/03_streaming.py --offline
Expected: A streamed reply, then its character count.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_stream, print_text


def main() -> None:
    settings = lesson_settings()
    model = get_chat_model(
        settings=settings, responses=["Thanks for contacting Brightwave.\nHow can we help?"]
    )
    # KEY IDEA: each chunk is only a piece; downstream storage needs the assembled text.
    text = print_stream(model.stream("Greet a Brightwave customer in two short lines."))
    print_text(f"Assembled {len(text)} characters.")


if __name__ == "__main__":
    run_cli(main)
