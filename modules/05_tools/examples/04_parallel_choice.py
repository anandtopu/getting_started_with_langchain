"""Dispatch independent read-only requests concurrently and examine tool_choice.

Run: uv run python modules/05_tools/examples/04_parallel_choice.py --offline
Expected: Two stock results with distinct call IDs in offline mode.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from concurrent.futures import ThreadPoolExecutor

from langchain_core.messages import AIMessage

from common.agent import dispatch
from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message, print_text
from common.tools import make_order_tools


def main() -> None:
    settings = lesson_settings()
    tools = make_order_tools("C001")
    fixture = AIMessage(
        content="",
        tool_calls=[
            {"name": "check_stock", "args": {"sku": sku}, "id": f"stock-{i}"}
            for i, sku in enumerate(["BW-001", "BW-002"])
        ],
    )
    model = get_chat_model(settings=settings, responses=[fixture])
    options = {} if settings.llm_provider == "ollama" else {"tool_choice": "check_stock"}
    if settings.llm_provider == "ollama":
        print_text("Ollama accepts but ignores tool_choice; the prompt requests stock explicitly.")
    reply = model.bind_tools(tools, **options).invoke(
        "Check stock for BW-001 and BW-002. Request both if supported."
    )
    # KEY IDEA: only independent reads are safe to execute concurrently here.
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(lambda call: dispatch(call, tools), reply.tool_calls):
            print_message(result)


if __name__ == "__main__":
    run_cli(main)
