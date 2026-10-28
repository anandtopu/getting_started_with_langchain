"""Delegate research and critique with isolated histories and finite budgets.

Run: uv run --extra agents python modules/17_deep_agents/examples/03_subagents.py --offline
Expected: Research returns a source; critique receives only the draft evidence.
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
    researcher = create_agent(
        get_chat_model(
            settings=settings,
            responses=[
                tool_request("read_research", {"path": "/sources/customer_trends.md"}),
                "Synthetic evidence: clearer setup guidance matters.",
            ],
        ),
        files.tools()[:1],
        middleware=[
            ModelCallLimitMiddleware(run_limit=3, exit_behavior="end"),
            ToolCallLimitMiddleware(run_limit=1, exit_behavior="end"),
        ],
    )
    result = researcher.invoke(
        {"messages": [{"role": "user", "content": "Read /sources/customer_trends.md."}]},
        {"recursion_limit": 30},
    )
    evidence = [m.content for m in result["messages"] if m.type == "tool"]
    critic = create_agent(
        get_chat_model(
            settings=settings,
            responses=["Keep the synthetic label; do not generalize 40 interviews to the market."],
        ),
        [],
        middleware=[ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")],
    )
    # KEY IDEA: the critic gets evidence and a narrow question, not the researcher's history.
    critique = critic.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Critique generalization risk in this evidence: " + str(evidence),
                }
            ]
        }
    )
    print_text(str(critique["messages"][-1].content))


if __name__ == "__main__":
    run_cli(main)
