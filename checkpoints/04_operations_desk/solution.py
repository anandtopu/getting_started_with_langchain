"""Evaluate a bounded read-only operations desk over explicitly scripted model trajectories.

Run: uv run --extra agents python checkpoints/04_operations_desk/solution.py --offline
Expected: Eight contract cases pass; a report and graph diagram are saved under .runtime/.
Cost: Up to twelve short calls per case in live mode. Requires: agents
"""

import json
from pathlib import Path

from common.config import ROOT, Settings
from common.errors import run_cli
from common.lesson import lesson_settings
from common.operations import build_operations
from common.pretty import print_text


def run_case(case: dict, settings: Settings) -> dict:
    graph = build_operations(settings, case["customer"])
    result = graph.invoke(
        {
            "question": case["question"],
            "order_id": case["order_id"],
            "sku": case["sku"],
            "reports": [],
        },
        {"max_concurrency": 2, "recursion_limit": 12},
    )
    reports = sorted(result["reports"], key=lambda report: report["role"])
    denied = [report["role"] for report in reports if not report["verified_tool_result"]]
    return {
        "id": case["id"],
        "roles": result["roles"],
        "denied": denied,
        "passed": result["roles"] == case["expected_roles"] and denied == case["expected_denied"],
        "reports": reports,
        "answer": result["answer"],
    }


def main() -> None:
    settings = lesson_settings()
    cases = [
        json.loads(line)
        for line in (Path(__file__).with_name("eval.jsonl"))
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    results = [run_case(case, settings) for case in cases]
    output = ROOT / settings.runtime_dir / "operations-desk"
    output.mkdir(parents=True, exist_ok=True)
    payload = {
        "mode": "scripted-contract" if settings.course_offline else "live",
        "quality_claim": "None: fixtures test routing and access controls, not model intelligence.",
        "passed": sum(row["passed"] for row in results),
        "total": len(results),
        "cases": results,
    }
    (output / "evaluation.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    # KEY IDEA: the account-free diagram shows the same compiled graph used in the cases.
    (output / "graph.mmd").write_text(
        build_operations(settings, "C001").get_graph().draw_mermaid(), encoding="utf-8"
    )
    print_text(str({"passed": payload["passed"], "total": len(results), "output": str(output)}))
    if not all(row["passed"] for row in results):
        raise ValueError("One or more operations-desk contracts failed.")


if __name__ == "__main__":
    run_cli(main)
