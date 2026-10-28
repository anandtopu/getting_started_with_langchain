"""Improve a draft until the gate passes or the iteration budget ends.

Run: uv run --extra agents python modules/15_workflows/examples/06_evaluator_optimizer.py --offline
Expected: Two attempts, six logical model calls, and an accepted synthetic report.
Cost: At most six short calls: two workers plus two draft/evaluate pairs. Offline fixtures incur
no API fee.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.workflows import build_review_graph, review_groups


def main() -> None:
    settings = lesson_settings()
    categories = list(review_groups())[:2]
    # KEY IDEA: maximum attempts is enforced even if an evaluator never approves.
    result = build_review_graph(settings, max_attempts=2).invoke(
        {"categories": categories, "sections": [], "attempt": 0, "model_calls": 0},
        {"recursion_limit": 12, "max_concurrency": 2},
    )
    print_text(
        str({key: result[key] for key in ("attempt", "model_calls", "accepted", "feedback")})
    )
    print_text(result["report"])


if __name__ == "__main__":
    run_cli(main)
