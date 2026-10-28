"""Save a transparent local evaluation report, including known answer misses.

Run: uv run --extra agents python modules/19_evaluation/use_case/support_eval.py --offline
Expected: 4/6 scripted cases; strict quality gate blocks release; report under .runtime/.
Cost: Up to thirty logical live calls; retries can add attempts. Zero offline. Requires: agents
"""

from common.config import ROOT
from common.errors import run_cli
from common.evaluation import save_report
from common.lesson import lesson_settings
from common.pretty import print_text
from common.release import evaluation_gate
from common.support_evaluation import load_cases, local_evaluate


def main() -> None:
    settings = lesson_settings()
    report = local_evaluate(load_cases(), settings)
    report["release_allowed"] = evaluation_gate(report)
    output = ROOT / settings.runtime_dir / "support-evaluation.json"
    save_report(report, output)
    print_text(
        str(
            {
                "passed": report["passed"],
                "total": report["total"],
                "release_allowed": report["release_allowed"],
                "report": str(output),
            }
        )
    )


if __name__ == "__main__":
    run_cli(main)
