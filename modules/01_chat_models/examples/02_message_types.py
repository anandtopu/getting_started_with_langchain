"""Inspect message roles and a correctly matched tool-result transcript.

Run: uv run python modules/01_chat_models/examples/02_message_types.py --offline
Expected: system, human, ai, tool roles, followed by a reply from plain-dict input.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message


def example_history() -> list:
    return [
        SystemMessage("Help Brightwave customers."),
        HumanMessage("Stock for BW-001?"),
        AIMessage(
            content="",
            tool_calls=[{"name": "check_stock", "args": {"sku": "BW-001"}, "id": "stock-1"}],
        ),
        ToolMessage(content='{"stock": 12}', tool_call_id="stock-1"),
    ]


def main() -> None:
    settings = lesson_settings()
    # KEY IDEA: ToolMessage is a program result, not a new instruction from the customer.
    for message in example_history():
        print_message(message)
    print_message(
        get_chat_model(settings=settings).invoke(
            [
                {"role": "system", "content": "Keep Brightwave replies brief."},
                {"role": "user", "content": "Say hello."},
            ]
        )
    )


if __name__ == "__main__":
    run_cli(main)
