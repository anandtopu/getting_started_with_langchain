"""Run all five capstone evaluation sets; keep behavioral and answer-quality gates distinct.

Run: uv run --extra apps python scripts/evaluate.py --offline
Expected: 17/19 contracts pass; two policy misses block --release.
Cost: free offline; live calls across all five capstones incur provider costs.
"""

import argparse
import json
import runpy
from pathlib import Path
from tempfile import TemporaryDirectory

from common.config import ROOT, get_settings
from common.errors import run_cli
from common.testing import offline_environment


def evaluate(settings, output: Path) -> dict:
    if output.resolve().is_relative_to((ROOT / "data").resolve()):
        raise ValueError("Evaluation output must stay outside committed seed data.")
    reports = {}
    with TemporaryDirectory() as temporary:
        for folder in sorted((ROOT / "capstones").glob("[0-9][0-9]_*")):
            run_case = runpy.run_path(str(folder / "solution.py"))["run_case"]
            cases = [
                json.loads(line)
                for line in (folder / "eval.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            reports[folder.name] = [
                run_case(case, settings, Path(temporary) / folder.name / case["id"])
                for case in cases
            ]
    rows = [row for group in reports.values() for row in group]
    report = {
        "mode": "offline scripted contracts" if settings.course_offline else "live",
        "passed": sum(row["passed"] for row in rows),
        "total": len(rows),
        "release_allowed": all(row["passed"] for row in rows),
        "capstones": reports,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument(
        "--release", action="store_true", help="Fail if any quality contract fails."
    )
    args = parser.parse_args()
    settings = get_settings()
    if args.offline:
        settings = settings.model_copy(update={"course_offline": True})
    output = ROOT / settings.runtime_dir / "capstone-evaluation.json"
    if settings.course_offline:
        with offline_environment():
            report = evaluate(settings, output)
    else:
        report = evaluate(settings, output)
    print(json.dumps({key: value for key, value in report.items() if key != "capstones"}))
    print(f"Evidence: {output}")
    # KEY IDEA: an evaluation can finish successfully while its release decision is false.
    if args.release and not report["release_allowed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    run_cli(main)
