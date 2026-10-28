"""Whole-turn trimming.

Task: Keep recent complete turns using approximate tokens without orphaning tool results.

Run: uv run --extra agents python modules/11_memory/exercises/02_apply.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from langchain_core.messages import BaseMessage, HumanMessage

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def trim(messages: list[BaseMessage], budget: int) -> list[BaseMessage]:
    # YOUR CODE HERE: Whole-turn trimming.
    return messages


def main() -> None:
    lesson_settings()
    print_text(str(trim([HumanMessage("Remember standard shipping.")], 60)))


if __name__ == "__main__":
    run_cli(main)
