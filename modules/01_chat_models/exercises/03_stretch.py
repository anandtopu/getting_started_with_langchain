"""Batch complete drafts.

Task: Use model.batch with max_concurrency=2; return text for every input in input order.
Run: uv run python modules/01_chat_models/exercises/03_stretch.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain_core.language_models import BaseChatModel

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def draft(texts: list[str], model: BaseChatModel) -> list[str]:
    return [model.invoke(texts[0]).content] if texts else []


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


def main() -> None:
    settings = lesson_settings()
    from common.models import get_chat_model

    print_text(
        str(draft(["Welcome a customer.", "Thank a customer."], get_chat_model(settings=settings)))
    )


if __name__ == "__main__":
    run_cli(main)
