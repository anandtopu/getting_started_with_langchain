"""Execute a planner/researcher/writer/critic graph and save a validated sourced report.

Run: uv run --extra agents python capstones/04_research_crew/solution.py --offline
Expected: first draft fails; second passes exact-quote checks; synthetic report saved.
Cost: at most 13 logical calls with three draft attempts; zero offline. Requires: agents
"""

from pathlib import Path

from common.config import ROOT
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.research_crew import build_crew, render_report


def run_case(case: dict, settings, directory: Path) -> dict:
    result = build_crew(settings, max_attempts=case["attempts"]).invoke(
        {"question": case["question"], "attempt": 0, "evidence": [], "calls": 0},
        {"recursion_limit": 25, "max_concurrency": 2},
    )
    passed = result["accepted"] == case["accepted"] and result["calls"] <= 13
    report = render_report(result) if result["accepted"] else None
    if report:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "report.md").write_text(report, encoding="utf-8")
    return {
        "id": case["id"],
        "passed": passed,
        "accepted": result["accepted"],
        "attempts": result["attempt"],
        "logical_calls": result["calls"],
        "report": report,
    }


def main() -> None:
    settings = lesson_settings()
    # KEY IDEA: exact evidence validation AND the critic verdict gate the bounded revision loop.
    result = run_case(
        {
            "id": "trends",
            "question": "Research Brightwave customer and product trends",
            "attempts": 2,
            "accepted": True,
        },
        settings,
        ROOT / settings.runtime_dir / "research-crew",
    )
    print_text(str(result))
    if not result["passed"]:
        raise ValueError("Research acceptance failed.")


if __name__ == "__main__":
    run_cli(main)
