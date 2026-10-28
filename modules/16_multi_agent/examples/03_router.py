"""Use confidence to select specialists or clarification.

Run: uv run --extra agents python modules/16_multi_agent/examples/03_router.py --offline
Expected: A shipping request selects logistics; an unclear request uses fallback.
Cost: At most seven short calls across two demonstrations. Offline fixtures incur no API fee.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.operations import build_operations
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    # KEY IDEA: each invocation starts a new isolated graph run with an empty reducer.
    for question in ("Check shipping for BW1001", "I need help"):
        result = build_operations(settings, "C001").invoke(
            {"question": question, "order_id": "BW1001", "sku": "BW-001", "reports": []},
            {"max_concurrency": 2},
        )
        print_text(str({"roles": result["roles"], "answer": result["answer"]}))


if __name__ == "__main__":
    run_cli(main)
