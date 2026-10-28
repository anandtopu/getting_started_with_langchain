"""Bound an agent loop.

Task: Use the shared loop with max_turns=3 and max_tool_calls=4; return final text. Repeated
calls must stop.
Run: uv run python modules/05_tools/exercises/03_stretch.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain_core.language_models import BaseChatModel

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import message_text, print_text


def answer(model: BaseChatModel, tools: list, question: str) -> str:
    return message_text(model.invoke(question))


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


def main() -> None:
    settings = lesson_settings()
    from common.models import get_chat_model
    from common.tools import make_order_tools

    print_text(answer(get_chat_model(settings=settings), make_order_tools("C001"), "Say hello."))


if __name__ == "__main__":
    run_cli(main)
