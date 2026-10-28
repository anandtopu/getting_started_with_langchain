"""Choose a building block.

Task: Choose LangGraph for durable work, agent for tool decisions, LCEL for fixed steps, model
otherwise.
Run: uv run python modules/00_setup/exercises/02_apply.py --offline
Expected: a runnable baseline demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def choose(*, durable: bool = False, tools: bool = False, fixed: bool = False) -> str:
    return "model"


# YOUR CODE HERE: improve the baseline function above to satisfy the task.


def main() -> None:
    lesson_settings()
    print_text(choose(durable=True))


if __name__ == "__main__":
    run_cli(main)
