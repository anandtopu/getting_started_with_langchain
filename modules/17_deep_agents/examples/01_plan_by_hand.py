"""Add an explicit bounded plan to create_agent before using a deep-agent harness.

Run: uv run --extra agents python modules/17_deep_agents/examples/01_plan_by_hand.py --offline
Expected: The todo list is pending; a plan is not evidence that tasks ran.
Cost: At most three short model calls. Offline fixtures incur no API fee.
Requires: agents
"""

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelCallLimitMiddleware,
    TodoListMiddleware,
    ToolCallLimitMiddleware,
)

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    tasks = [
        {"content": "Read synthetic research sources", "status": "pending"},
        {"content": "Write and critique a cited report", "status": "pending"},
    ]
    model = get_chat_model(
        settings=settings,
        responses=[
            tool_request("write_todos", {"todos": tasks}),
            "Plan created; research not yet performed.",
        ],
    )
    # KEY IDEA: TodoListMiddleware stores a plan; separate tool calls must perform the work.
    agent = create_agent(
        model,
        [],
        middleware=[
            TodoListMiddleware(),
            ModelCallLimitMiddleware(run_limit=3, exit_behavior="end"),
            ToolCallLimitMiddleware(run_limit=1, exit_behavior="end"),
        ],
    )
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Plan a synthetic outdoor-gear report."}]},
        {"recursion_limit": 30},
    )
    print_text(str(result.get("todos", [])))


if __name__ == "__main__":
    run_cli(main)
