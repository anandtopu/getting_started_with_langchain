"""Map all review categories, evaluate a draft, and save only an accepted report.

Run: uv run --extra agents python modules/15_workflows/use_case/weekly_report.py --offline
Expected: All categories covered; two attempts; report saved under the runtime directory.
Cost: At most ten short calls with six categories. Requires: agents
"""

import json

from common.config import ROOT
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.workflows import build_review_graph, review_groups


def main() -> None:
    settings = lesson_settings()
    categories = list(review_groups())
    result = build_review_graph(settings).invoke(
        {"categories": categories, "sections": [], "attempt": 0, "model_calls": 0},
        {"max_concurrency": 2, "recursion_limit": 12},
    )
    output = ROOT / settings.runtime_dir / "weekly-report"
    output.mkdir(parents=True, exist_ok=True)
    # KEY IDEA: a rejected draft remains diagnostic evidence; it is not a published report.
    (output / "evaluation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    if result["accepted"]:
        (output / "report.md").write_text(result["report"], encoding="utf-8")
    print_text(
        str(
            {
                "accepted": result["accepted"],
                "attempts": result["attempt"],
                "model_calls": result["model_calls"],
                "output": str(output),
            }
        )
    )


if __name__ == "__main__":
    run_cli(main)
