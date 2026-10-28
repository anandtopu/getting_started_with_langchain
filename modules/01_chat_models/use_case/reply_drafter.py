"""Stream a polite ticket reply grounded in a supplied Brightwave policy.

Run: uv run python modules/01_chat_models/use_case/reply_drafter.py --offline
Expected: A draft and usage/cost summary; no email is sent.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from collections.abc import Iterator

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from common.data import data_path, load_jsonl
from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_stream, print_usage


def main() -> None:
    settings = lesson_settings()
    ticket = load_jsonl("support_tickets.jsonl")[1]
    policy = data_path("policies/returns.md").read_text(encoding="utf-8")
    model = get_chat_model(settings=settings)
    total = None

    def chunks() -> Iterator[BaseMessage]:
        nonlocal total
        for chunk in model.stream(
            [
                SystemMessage(
                    "Draft only, using this policy. Never assert a refund was issued. " + policy
                ),
                HumanMessage(ticket["text"]),
            ]
        ):
            total = chunk if total is None else total + chunk
            yield chunk

    # KEY IDEA: adding chunks preserves final usage metadata as well as text.
    print_stream(chunks())
    if total is not None:
        print_usage(total, settings=settings)


if __name__ == "__main__":
    run_cli(main)
