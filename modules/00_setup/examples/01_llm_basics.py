"""Compare supplied evidence with an unknown fact; tokens are pieces of text.

Run: uv run python modules/00_setup/examples/01_llm_basics.py --offline
Expected: A grounded return-window reply; unknown private facts require evidence.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from langchain_core.messages import HumanMessage, SystemMessage

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message, print_text


def context_fits(input_tokens: int, output_reserve: int, context_window: int) -> bool:
    if min(input_tokens, output_reserve, context_window) < 0:
        raise ValueError("Token counts cannot be negative.")
    return input_tokens + output_reserve <= context_window


def main() -> None:
    settings = lesson_settings()
    # KEY IDEA: these are supplied counts, not an inaccurate character-based tokenizer.
    print_text(f"120 input + 40 reserved fit a 256-token window: {context_fits(120, 40, 256)}")
    model = get_chat_model(settings=settings, temperature=0)
    print_message(
        model.invoke(
            [
                SystemMessage(
                    "Answer from this evidence only: unused gear can be returned within "
                    "30 days of delivery with proof of purchase. Say unknown if absent."
                ),
                HumanMessage(
                    "What is the return window? What is my private order's delivery date?"
                ),
            ]
        )
    )
    print_text("Temperature changes sampling, not truth. A fluent answer still needs checking.")


if __name__ == "__main__":
    run_cli(main)
