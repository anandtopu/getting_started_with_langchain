"""Construct message roles.

Task: Return a system instruction followed by the unchanged customer text as a HumanMessage.
Run: uv run python modules/01_chat_models/exercises/01_practice.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain_core.messages import HumanMessage

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def messages(text: str) -> list:
    return [HumanMessage(text)]


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


def main() -> None:
    lesson_settings()
    print_text(str(messages("Where is my order?")))


if __name__ == "__main__":
    run_cli(main)
