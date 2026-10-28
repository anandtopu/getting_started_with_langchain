"""Read provider token usage, including optional reasoning-token details.

Run: uv run python modules/01_chat_models/examples/06_usage_cost.py --offline
Expected: Usage fields and an honest unknown estimate when usage is absent.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from langchain_core.messages import AIMessage

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text, print_usage


def main() -> None:
    settings = lesson_settings()
    fixture = AIMessage(
        content="Welcome to Brightwave.",
        usage_metadata={
            "input_tokens": 20,
            "output_tokens": 8,
            "total_tokens": 28,
            "output_token_details": {"reasoning": 2},
        },
    )
    reply = get_chat_model(settings=settings, responses=[fixture]).invoke("Greet a customer.")
    usage = reply.usage_metadata or {}
    print_text(str(usage))
    print_text(
        "Reasoning tokens: "
        f"{usage.get('output_token_details', {}).get('reasoning', 'not reported')}"
    )
    # KEY IDEA: reasoning details are a subset of output tokens; never count them twice.
    print_usage(reply, settings=settings)
    print_usage(AIMessage(content="No usage supplied"), settings=settings)


if __name__ == "__main__":
    run_cli(main)
