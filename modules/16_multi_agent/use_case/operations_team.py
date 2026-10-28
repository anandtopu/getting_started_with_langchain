"""Route a customer request to three restricted specialists and synthesize their evidence.

Run: uv run --extra agents python modules/16_multi_agent/use_case/operations_team.py --offline
Expected: Billing, product RAG and logistics reports; no writes or cross-customer data.
Cost: Up to twelve short calls including product retrieval generation. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.operations import build_operations
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    # KEY IDEA: the authenticated host fixes C001; workers receive minimum necessary IDs.
    result = build_operations(settings, "C001").invoke(
        {
            "question": "Check billing total, tent product specifications, and shipping.",
            "order_id": "BW1001",
            "sku": "BW-001",
            "reports": [],
        },
        {"max_concurrency": 2, "recursion_limit": 12},
    )
    print_text(str(sorted(result["reports"], key=lambda report: report["role"])))
    print_text(result["answer"])


if __name__ == "__main__":
    run_cli(main)
