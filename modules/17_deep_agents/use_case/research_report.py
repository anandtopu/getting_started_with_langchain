"""Plan, read synthetic sources, critique a draft and save a validated report.

Run: uv run --extra agents python modules/17_deep_agents/use_case/research_report.py --offline
Expected: Source-labelled synthetic report saved in the runtime directory.
Cost: At most six main-agent calls plus one critique call. Requires: agents
"""

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelCallLimitMiddleware,
    TodoListMiddleware,
    ToolCallLimitMiddleware,
)

from common.config import ROOT
from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.research import VirtualFiles, validate_report


def main() -> None:
    settings = lesson_settings()
    files = VirtualFiles()
    report = (
        "Synthetic outdoor-gear research\n\n48 of 80 invented shoppers "
        "preferred repairable gear [/sources/market_brief.md].\n24 of 40 "
        "invented interviewees wanted clearer tent setup guides "
        "[/sources/customer_trends.md].\nThese samples cannot establish "
        "real market trends."
    )
    responses = [
        tool_request(
            "write_todos",
            {
                "todos": [
                    {"content": "Read and cite two synthetic sources", "status": "in_progress"}
                ]
            },
            "plan",
        ),
        tool_request("read_research", {"path": "/sources/market_brief.md"}, "source1"),
        tool_request("read_research", {"path": "/sources/customer_trends.md"}, "source2"),
        tool_request("write_report", {"path": "/reports/trends.md", "content": report}, "write"),
        "Draft ready for critique.",
    ]
    agent = create_agent(
        get_chat_model(settings=settings, responses=responses),
        files.tools(),
        middleware=[
            TodoListMiddleware(),
            ModelCallLimitMiddleware(run_limit=6, exit_behavior="end"),
            ToolCallLimitMiddleware(run_limit=4, exit_behavior="end"),
        ],
    )
    agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Plan, read market_brief.md and customer_trends.md in /sources/, "
                        "then write a cited synthetic report to /reports/trends.md."
                    ),
                }
            ]
        },
        {"recursion_limit": 60},
    )
    draft = files.read("/reports/trends.md")
    citations = validate_report(draft, files)
    # KEY IDEA: source validation is code; a critic's opinion does not prove factuality.
    critique = get_chat_model(
        settings=settings,
        responses=["Synthetic scope is explicit; check exact figures against the cited files."],
    ).invoke(
        "Critique this report against its evidence: "
        + draft
        + str({p: files.read(p) for p in citations})
    )
    output = ROOT / settings.runtime_dir / "research-report"
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.md").write_text(draft, encoding="utf-8")
    (output / "critique.txt").write_text(str(critique.content), encoding="utf-8")
    print_text(str({"sources": citations, "output": str(output)}))


if __name__ == "__main__":
    run_cli(main)
