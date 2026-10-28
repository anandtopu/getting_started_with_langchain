"""Inspect analytics schema, repair SQL, plot measured rows and write an executive summary.

Run: uv run --extra agents python capstones/03_insight_analyst/solution.py --offline
Expected: one failed query is repaired; 200 orders in three groups; runtime PNG and summary.
Cost: up to four logical calls; SDK retries may add attempts. Zero offline. Requires: agents
"""

import json
from pathlib import Path

from common.analyst import analyze, chart
from common.config import ROOT
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def run_case(case: dict, settings, directory: Path) -> dict:
    result = analyze(case["question"], settings, max_attempts=case.get("attempts", 2))
    passed = result["accepted"] == case["accepted"]
    if result["accepted"]:
        passed = (
            passed
            and result["verified_total"] == case["total"]
            and len(result["rows"]) == case["groups"]
        )
        chart(result, directory / "analytics.png")
    return {"id": case["id"], "passed": bool(passed), "result": result}


def main() -> None:
    settings = lesson_settings()
    result = analyze("Count orders by status", settings)
    output = ROOT / settings.runtime_dir / "insight-analyst"
    if not result["accepted"]:
        raise ValueError("No accepted SQL result; no chart written.")
    # KEY IDEA: chart numbers come from the read-only database, never the model's prose.
    chart(result, output / "orders.png")
    (output / "summary.md").write_text(result["summary"] + "\n", encoding="utf-8")
    (output / "evidence.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print_text(
        str({"verified_total": result["verified_total"], "chart": str(output / "orders.png")})
    )


if __name__ == "__main__":
    run_cli(main)
