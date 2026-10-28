"""Exercise the verified optional SDK with state-backed files and a named subagent.

Run: uv run --extra deep python modules/17_deep_agents/examples/04_deepagents_sdk.py --offline
Expected: Planning, delegation and a virtual file write run through the actual SDK.
Cost: At most five supervisor calls plus bounded child calls; no shell or web service. Offline
fixtures incur no API fee.
Requires: deep
"""

from deepagents import create_deep_agent
from deepagents.backends import StateBackend
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
    researcher = get_chat_model(
        settings=settings, responses=["Synthetic report only; no real market inference."]
    )
    responses = [
        tool_request(
            "write_todos",
            {"todos": [{"content": "Prepare synthetic scope note", "status": "in_progress"}]},
            "plan",
        ),
        tool_request(
            "task",
            {"subagent_type": "researcher", "description": "Write a synthetic-data scope note."},
            "delegate",
        ),
        tool_request(
            "write_file",
            {
                "file_path": "/reports/scope.md",
                "content": "Synthetic report only; no real market inference.",
            },
            "file",
        ),
        "Scope note saved in state; no host file was written.",
    ]
    # KEY IDEA: StateBackend has virtual state storage, not host filesystem or shell access.
    agent = create_deep_agent(
        model=get_chat_model(settings=settings, responses=responses),
        backend=StateBackend(),
        subagents=[
            {
                "name": "general-purpose",
                "description": "Return a manual-review note; no further delegation",
                "model": get_chat_model(settings=settings, responses=["Request manual review."]),
                "tools": [],
                "middleware": [ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")],
            },
            {
                "name": "researcher",
                "description": "Prepare scope notes",
                "system_prompt": "Use only synthetic evidence.",
                "model": researcher,
                "tools": [],
                "middleware": [ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")],
            },
        ],
        middleware=[
            TodoListMiddleware(),
            ModelCallLimitMiddleware(run_limit=5, exit_behavior="end"),
            ToolCallLimitMiddleware(run_limit=3, exit_behavior="end"),
        ],
    )
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Plan a scope note, delegate it to researcher, then write "
                        "/reports/scope.md."
                    ),
                }
            ]
        },
        {"recursion_limit": 60},
    )
    print_text(str({"files": result.get("files", {}), "todos": result.get("todos", [])}))


if __name__ == "__main__":
    run_cli(main)
