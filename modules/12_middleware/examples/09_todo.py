"""Track a small support plan through TodoListMiddleware.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/12_middleware/examples/09_todo.py --offline
Expected: The final state contains two pending tasks; planning does not execute them.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    todos = [
        {"content": "Read return policy", "status": "pending"},
        {"content": "Review customer order", "status": "pending"},
    ]
    # KEY IDEA: writing a plan records intentions; it does not execute or verify those tasks.
    model = get_chat_model(
        settings=settings,
        responses=[
            tool_request("write_todos", {"todos": todos}),
            "Plan recorded; both tasks still need execution.",
        ],
    )
    agent = create_agent(model, tools=[], middleware=[TodoListMiddleware()])
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Plan an order and policy review. Do not execute it yet.",
                }
            ]
        }
    )
    print_text(str(result["todos"]))


if __name__ == "__main__":
    run_cli(main)
