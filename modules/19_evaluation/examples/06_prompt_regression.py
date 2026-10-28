"""Compare versioned prompts on held-out expectations, not exact reply text.

Run: uv run --extra agents python modules/19_evaluation/examples/06_prompt_regression.py --offline
Expected: Different prompt hashes and equal offline contract results.
Cost: Up to sixty logical calls live; SDK retries can add attempts. Zero offline. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.support_evaluation import load_cases, local_evaluate


def main() -> None:
    settings = lesson_settings()
    for version in ("v1", "v2"):
        result = local_evaluate(load_cases(), settings, version=version)
        print_text(
            str(
                {
                    "version": version,
                    "passed": result["passed"],
                    "total": result["total"],
                    "prompt_hash": result["rows"][0]["answer"]["prompt_sha256"],
                }
            )
        )
    # KEY IDEA: the offline fixture ignores prompt prose, so equal scores prove no improvement.
    print_text(
        "Offline equality is expected. Compare live runs and human-reviewed failures separately."
    )


if __name__ == "__main__":
    run_cli(main)
