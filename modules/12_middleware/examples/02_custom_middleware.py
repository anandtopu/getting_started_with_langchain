"""Compare decorator hooks and a class-based input guard.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/12_middleware/examples/02_custom_middleware.py --offline
Expected: A decorator observes valid input; oversized input is rejected before generation.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import after_model

from common.errors import run_cli
from common.guardrails import InputLimit
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


@after_model
def inspect_output(state: dict, runtime: Any) -> None:
    if len(str(state["messages"][-1].content)) > 2000:
        raise ValueError("Answer exceeds the application review limit.")


def main() -> None:
    settings = lesson_settings()
    agent = create_agent(
        get_chat_model(settings=settings), tools=[], middleware=[InputLimit(), inspect_output]
    )
    # KEY IDEA: prompts ask; deterministic hooks enforce these particular limits.
    print_text(
        agent.invoke({"messages": [{"role": "user", "content": "Explain the return window."}]})[
            "messages"
        ][-1].content
    )
    try:
        agent.invoke({"messages": [{"role": "user", "content": "x" * 4001}]})
    except ValueError as error:
        print_text(str(error))


if __name__ == "__main__":
    run_cli(main)
