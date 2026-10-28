"""Validate return policy and make retries idempotent on a disposable database.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/10_agents/examples/06_return_write.py --offline
Expected: One refund record for 4995 cents; replay does not add a second record.
Cost: No model calls or API fees.
Requires: agents
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.returns import ReturnRequest, SupportContext, record_return, runtime_orders


def main() -> None:
    lesson_settings()
    with TemporaryDirectory(prefix="brightwave-return-") as folder:
        context = SupportContext(
            "C008",
            runtime_orders(Path(folder) / "orders.db"),
            inspected_unused=True,
            proof_and_accessories=True,
        )
        request = ReturnRequest(order_id="BW1008", sku="BW-021", idempotency_key="lesson10-return")
        # KEY IDEA: amount, ownership, eligibility and quantity are checked in one transaction.
        print_text(str(record_return(request, context)))
        print_text(str(record_return(request, context)))
    print_text("Synthetic warehouse attestation; no payment was sent.")


if __name__ == "__main__":
    run_cli(main)
