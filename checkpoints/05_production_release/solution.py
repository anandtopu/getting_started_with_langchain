"""Rehearse release: require both engineering and answer-quality contracts.

Run: uv run --extra apps python checkpoints/05_production_release/solution.py --offline
Expected: HTTP contracts pass, quality 6/6, release_allowed true; JSON report saved.
Add --release to enforce the gate (nonzero exit if any required contract fails).
Cost: up to 30 logical live calls; retries may add attempts. HTTP checks use fixtures.
Requires: apps
"""

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from common.config import ROOT, Settings, get_settings
from common.errors import run_cli
from common.evaluation import save_report
from common.pretty import print_text
from common.release import api_contract, evaluation_gate
from common.support_evaluation import load_cases, local_evaluate


def run_case(case: dict, directory: Path) -> dict:
    actual = api_contract(directory, case["decision"])
    result = actual["result"]
    status = result["result"]["status"] if result["result"] else result["status"]
    checks = {key: value for key, value in actual.items() if key != "result"}
    checks["expected_outcome"] = status == case["expected_status"]
    return {"id": case["id"], "checks": checks, "passed": all(checks.values())}


def rehearse(settings: Settings) -> dict:
    cases = load_cases(ROOT / "checkpoints/05_production_release/eval.jsonl")
    with TemporaryDirectory() as directory:
        contracts = [run_case(case, Path(directory) / case["id"]) for case in cases]
    quality = local_evaluate(load_cases(), settings)
    return {
        "mode": "scripted-contract" if settings.course_offline else "mixed-live-quality",
        "engineering_passed": all(row["passed"] for row in contracts),
        "contracts": contracts,
        "quality": quality,
        "release_allowed": all(row["passed"] for row in contracts) and evaluation_gate(quality),
        "limits": (
            "Local demonstration only; external identity, billing, delivery and hosting unverified."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--release", action="store_true")
    args = parser.parse_args()
    settings = get_settings()
    if args.offline:
        settings = settings.model_copy(update={"course_offline": True})
    report = rehearse(settings)
    output = ROOT / settings.runtime_dir / "production-release.json"
    save_report(report, output)
    print_text(
        json.dumps(
            {
                "engineering_passed": report["engineering_passed"],
                "release_allowed": report["release_allowed"],
                "report": str(output),
            }
        )
    )
    if not report["engineering_passed"] or (args.release and not report["release_allowed"]):
        raise ValueError("Release gate rejected the report. Inspect failed cases before deploying.")


if __name__ == "__main__":
    run_cli(main)
