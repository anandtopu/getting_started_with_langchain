"""Keep evolving task state separate from immutable customer context.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/11_memory/examples/05_custom_state.py --offline
Expected: The result retains a typed task note; identity stays in runtime context.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from pathlib import Path
from typing import NotRequired

from langchain.agents import AgentState, create_agent

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.returns import SupportContext


class SupportState(AgentState):
    task_note: NotRequired[str]


def main() -> None:
    settings = lesson_settings()
    # KEY IDEA: mutable task notes belong in state; authenticated identity belongs in context.
    agent = create_agent(
        get_chat_model(settings=settings),
        tools=[],
        state_schema=SupportState,
        context_schema=SupportContext,
    )
    result = agent.invoke(
        {
            "messages": [{"role": "user", "content": "Help with my return."}],
            "task_note": "Awaiting SKU",
        },
        context=SupportContext("C001", Path("unused")),
    )
    print_text(str({"task_note": result["task_note"], "messages": len(result["messages"])}))


if __name__ == "__main__":
    run_cli(main)
