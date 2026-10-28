"""Run a guarded refund request and leave high-value writes paused for review.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/12_middleware/use_case/guarded_agent.py --offline
Expected: A human-review interrupt appears; the synthetic ledger remains unchanged.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from common.errors import run_cli
from common.fixtures import tool_request
from common.guardrails import guarded_agent
from common.lesson import lesson_settings
from common.memory import thread_config
from common.pretty import print_text
from common.returns import SupportContext, runtime_orders


def main() -> None:
    settings = lesson_settings()
    with TemporaryDirectory() as folder:
        context = SupportContext(
            "C001",
            runtime_orders(Path(folder) / "orders.db"),
            inspected_unused=True,
            proof_and_accessories=True,
        )
        agent = guarded_agent(
            settings,
            [
                tool_request(
                    "approve_refund",
                    {
                        "order_id": "BW1001",
                        "sku": "BW-014",
                        "reason": "unused",
                        "idempotency_key": "guarded-demo",
                    },
                )
            ],
        )
        # KEY IDEA: interruption is a successful safety outcome, not a completed refund.
        state = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Please return BW-014 on BW1001; use key guarded-demo.",
                    }
                ]
            },
            thread_config("C001", "review"),
            context=context,
        )
        print_text(str(state.get("__interrupt__", state["messages"][-1].content)))
        print_text("Demo stops here. A real UI must authenticate the reviewer before resuming.")


if __name__ == "__main__":
    run_cli(main)
