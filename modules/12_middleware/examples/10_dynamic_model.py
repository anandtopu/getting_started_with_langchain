"""Change the prompt and selected model without changing authenticated scope.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/12_middleware/examples/10_dynamic_model.py --offline
Expected: A runtime prompt and model override keep the same customer context.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from pathlib import Path
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, wrap_model_call

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text
from common.returns import SupportContext


@dynamic_prompt
def support_prompt(request: Any) -> str:
    return (
        f"Authenticated Brightwave customer: {request.runtime.context.customer_id}. "
        "Do not change this scope."
    )


def main() -> None:
    settings = lesson_settings()
    base = get_chat_model(settings=settings)
    review = get_chat_model(
        settings=settings,
        responses=["Review this complex request with the customer scope unchanged."],
    )

    @wrap_model_call
    def route(request: Any, handler: Any) -> Any:
        # KEY IDEA: model selection changes computation, not authorization context.
        selected = review if len(str(request.messages[-1].content)) > 80 else base
        return handler(request.override(model=selected))

    agent = create_agent(
        base, tools=[], context_schema=SupportContext, middleware=[support_prompt, route]
    )
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Review this Brightwave return with many exceptions. " * 2,
                }
            ]
        },
        context=SupportContext("C001", Path("unused")),
    )
    print_text(result["messages"][-1].content)
    print_text(
        "Both instances use the configured profile here; routing does not imply a stronger model."
    )


if __name__ == "__main__":
    run_cli(main)
