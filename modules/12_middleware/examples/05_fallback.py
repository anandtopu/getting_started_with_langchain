"""Recover from a synthetic primary model failure using model fallback.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/12_middleware/examples/05_fallback.py --offline
Expected: Backup response appears after the injected primary failure.
Cost: One backup generation; primary failure is deliberately injected in every mode.
Requires: agents
"""

from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware, wrap_model_call

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


@wrap_model_call
def inject_primary_failure(request: Any, handler: Any) -> Any:
    if request.model is PRIMARY:
        raise TimeoutError("Synthetic primary outage")
    return handler(request)


def main() -> None:
    global PRIMARY
    settings = lesson_settings()
    PRIMARY = get_chat_model(settings=settings)
    backup = get_chat_model(
        settings=settings, responses=["Backup draft: review Brightwave policy before replying."]
    )
    # KEY IDEA: the outer fallback must wrap the failing model operation.
    agent = create_agent(
        PRIMARY, tools=[], middleware=[ModelFallbackMiddleware(backup), inject_primary_failure]
    )
    print_text(
        agent.invoke({"messages": [{"role": "user", "content": "Draft a support reply."}]})[
            "messages"
        ][-1].content
    )


if __name__ == "__main__":
    run_cli(main)
