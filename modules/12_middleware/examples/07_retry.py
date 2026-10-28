"""Retry one transient model failure and one read-tool failure with no delay.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/12_middleware/examples/07_retry.py --offline
Expected: Three model attempts and two read attempts; no write is retried.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware, wrap_model_call
from langchain.tools import tool

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    attempts = {"model": 0, "tool": 0}

    @wrap_model_call
    def flaky_model(request: Any, handler: Any) -> Any:
        attempts["model"] += 1
        if attempts["model"] == 1:
            raise TimeoutError("Synthetic transient model error")
        return handler(request)

    @tool
    def flaky_stock(sku: str) -> dict:
        """Synthetic read-only stock service fails on its first attempt."""
        attempts["tool"] += 1
        if attempts["tool"] == 1:
            raise TimeoutError("Synthetic transient read error")
        return {"sku": sku, "stock": 87}

    options = {"max_retries": 1, "initial_delay": 0, "jitter": False, "retry_on": (TimeoutError,)}
    # KEY IDEA: retry only selected transient errors and idempotent/read operations.
    agent = create_agent(
        get_chat_model(
            settings=settings,
            responses=[tool_request("flaky_stock", {"sku": "BW-001"}), "Stock checked."],
        ),
        [flaky_stock],
        middleware=[
            ModelRetryMiddleware(**options),
            flaky_model,
            ToolRetryMiddleware(tools=["flaky_stock"], **options),
        ],
    )
    agent.invoke({"messages": [{"role": "user", "content": "Check BW-001 stock."}]})
    print_text(str(attempts))


if __name__ == "__main__":
    run_cli(main)
