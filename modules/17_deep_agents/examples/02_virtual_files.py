"""Use an allowlisted in-memory filesystem with no shell access.

Run: uv run --extra agents python modules/17_deep_agents/examples/02_virtual_files.py --offline
Expected: One source read, one virtual report, and rejected path traversal.
Cost: At most four short model calls. Offline fixtures incur no API fee.
Requires: agents
"""

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.research import VirtualFiles


def main() -> None:
    settings = lesson_settings()
    files = VirtualFiles()
    responses = [
        tool_request("read_research", {"path": "/sources/market_brief.md"}, "read"),
        tool_request(
            "write_report",
            {
                "path": "/reports/trends.md",
                "content": (
                    "Synthetic sample: 48 of 80 preferred repairable gear "
                    "[/sources/market_brief.md]."
                ),
            },
            "write",
        ),
        "Draft stored in virtual memory.",
    ]
    agent = create_agent(
        get_chat_model(settings=settings, responses=responses),
        files.tools(),
        middleware=[
            ModelCallLimitMiddleware(run_limit=4, exit_behavior="end"),
            ToolCallLimitMiddleware(run_limit=2, exit_behavior="end"),
        ],
    )
    agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Read the market brief, then write a cited synthetic summary to "
                        "/reports/trends.md."
                    ),
                }
            ]
        },
        {"recursion_limit": 30},
    )
    # KEY IDEA: virtual file names never become host paths, even for valid writes.
    print_text(files.files.get("/reports/trends.md", "No report was written."))
    try:
        files.read("/sources/../../.env")
    except ValueError as error:
        print_text(str(error))


if __name__ == "__main__":
    run_cli(main)
