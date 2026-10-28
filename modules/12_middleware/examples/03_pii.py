"""Redact synthetic email and card-like data before model access and output.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/12_middleware/examples/03_pii.py --offline
Expected: Redacted markers replace synthetic identifiers in retained messages.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    guards = [
        PIIMiddleware("email", strategy="redact", apply_to_output=True, apply_to_tool_results=True),
        PIIMiddleware(
            "card_fixture",
            detector=r"\b(?:\d[ -]?){15}\d\b",
            strategy="redact",
            apply_to_output=True,
            apply_to_tool_results=True,
        ),
    ]
    # KEY IDEA: this custom detector catches card-like fixtures, not every form of PII.
    agent = create_agent(
        get_chat_model(
            settings=settings, responses=["Contact demo@example.test; fixture 4111 1111 1111 1111."]
        ),
        tools=[],
        middleware=guards,
    )
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Synthetic demo@example.test; fixture 4111 1111 1111 1111.",
                }
            ]
        }
    )
    for message in result["messages"]:
        print_text(str(message.content))


if __name__ == "__main__":
    run_cli(main)
