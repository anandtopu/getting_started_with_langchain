"""Validated return request.

Task: Validate order ID, SKU, reason and idempotency key; forbid extra model fields.

Run: uv run --extra agents python modules/10_agents/solutions/03_stretch.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.returns import ReturnRequest


def parse_request(values: dict) -> ReturnRequest | None:
    # KEY IDEA: Validated return request.
    return ReturnRequest.model_validate(values)


def main() -> None:
    lesson_settings()
    print_text(
        str(
            parse_request(
                {
                    "order_id": "BW1008",
                    "sku": "BW-021",
                    "reason": "unused",
                    "idempotency_key": "exercise-return",
                }
            )
        )
    )


if __name__ == "__main__":
    run_cli(main)
