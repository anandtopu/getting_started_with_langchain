"""Make the first Brightwave call using messages and a centrally configured model.

Run: uv run python scripts/first_call.py --offline
Expected: OFFLINE FIXTURE, followed by Brightwave's 30-day return policy.
Cost: no API fee offline/Ollama; normally less than $0.01 for a short hosted reply.
"""

import argparse

from langchain_core.messages import HumanMessage, SystemMessage

from common.config import get_settings
from common.data import data_path
from common.errors import run_cli
from common.models import get_chat_model
from common.pretty import print_message, print_text, print_usage
from common.tracing import tracing_scope


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Use a clearly labelled fixture.")
    args = parser.parse_args()
    settings = get_settings()
    if args.offline:
        settings.course_offline = True
    print_text("OFFLINE FIXTURE" if settings.course_offline else "LIVE MODEL CALL")
    policy = data_path("policies/returns.md").read_text(encoding="utf-8")
    # KEY IDEA: the model receives the real synthetic policy, not an invented business rule.
    messages = [
        SystemMessage(content="You assist Brightwave customers. Use only this policy:\n" + policy),
        HumanMessage(content="How long do I have to return unused gear? Answer in one sentence."),
    ]
    with tracing_scope(settings):
        answer = get_chat_model(settings=settings).invoke(messages)
    print_message(answer, settings=settings)
    print_usage(answer, settings=settings)


if __name__ == "__main__":
    run_cli(main)
