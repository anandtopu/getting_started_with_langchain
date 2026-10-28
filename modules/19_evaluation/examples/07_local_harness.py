"""Report failures and demonstrate a release gate that actually rejects them.

Run: uv run --extra agents python modules/19_evaluation/examples/07_local_harness.py --offline
Expected: 6/6 offline cases pass and the strict release gate is true.
Cost: Up to thirty logical live calls; retries can add attempts. Zero offline. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.release import evaluation_gate
from common.support_evaluation import load_cases, local_evaluate


def main() -> None:
    report = local_evaluate(load_cases(), lesson_settings())
    # KEY IDEA: the default quality threshold is 100%; known misses block release.
    print_text(
        str(
            {
                "passed": report["passed"],
                "total": report["total"],
                "release_allowed": evaluation_gate(report),
                "limits": report["limits"],
            }
        )
    )


if __name__ == "__main__":
    run_cli(main)
