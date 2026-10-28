"""Answer order-status questions using the audited, bounded manual tool loop.

Run: uv run python modules/05_tools/use_case/order_status.py --offline
Expected: Order and shipment results for C001/BW1001, then a draft response.
Cost: At most four model calls, usually under $0.01; offline/local no API fee.
"""

from common.agent import run_tool_loop
from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message
from common.tools import make_order_tools


def main() -> None:
    settings = lesson_settings()
    # Synthetic demo login is trusted application context; never read identity from a prompt.
    tools = make_order_tools("C001")
    model = get_chat_model(
        settings=settings,
        responses=[
            tool_request("lookup_order", {"order_id": "BW1001"}, "order-1"),
            tool_request("get_shipment_status", {"order_id": "BW1001"}, "shipment-1"),
            "Order BW1001 is delivered. "
            "Please review the shipment record above for its delivery date.",
        ],
    )
    for message in run_tool_loop(
        model, tools, "Please look up order BW1001 and its shipment status."
    )[2:]:
        print_message(message)


if __name__ == "__main__":
    run_cli(main)
