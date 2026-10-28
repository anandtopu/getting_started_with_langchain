"""Make the first evidence-grounded Brightwave call with optional tracing.

Run: uv run python modules/00_setup/use_case/first_call.py --offline
Expected: A reply grounded in the return policy; tracing remains optional.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from langchain_core.messages import HumanMessage, SystemMessage

from common.data import data_path
from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message, print_usage
from common.tracing import tracing_scope


def main() -> None:
    settings = lesson_settings()
    policy = data_path("policies/returns.md").read_text(encoding="utf-8")
    with tracing_scope(settings):
        reply = get_chat_model(settings=settings).invoke(
            [
                SystemMessage("Use only this Brightwave policy as evidence:\n" + policy),
                HumanMessage("Can I return unused gear delivered 12 days ago with a receipt?"),
            ]
        )
    print_message(reply)
    print_usage(reply, settings=settings)


if __name__ == "__main__":
    run_cli(main)
