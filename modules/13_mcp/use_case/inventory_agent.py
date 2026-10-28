"""Ask a stock question through a local MCP subprocess and a bounded agent.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/13_mcp/use_case/inventory_agent.py --offline
Expected: Reviewed server stock reaches the agent; the session and child process close.
Cost: Up to five short model calls; offline fixtures have no API fee.
Requires: agents
"""

import asyncio

from langchain.agents import create_agent
from langchain.tools import tool

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.mcp import call_inventory, checked_tools, inventory_adapter
from common.models import get_chat_model
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()

    async def exchange() -> None:
        async with inventory_adapter("stdio") as adapter:
            checked_tools(await adapter.list_tools())

            @tool
            async def inventory_stock(sku: str) -> dict:
                """Read validated stock from the reviewed local inventory service."""
                return await call_inventory(adapter, sku)

            # KEY IDEA: keep the adapter lifetime outside the agent's entire asynchronous run.
            agent = create_agent(
                get_chat_model(
                    settings=settings,
                    responses=[
                        tool_request("inventory_stock", {"sku": "BW-001"}),
                        "Inventory checked; stock is not reserved.",
                    ],
                ),
                [inventory_stock],
                system_prompt="Use inventory evidence; never claim a purchase or reservation.",
            )
            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": "Is BW-001 in stock?"}]},
                {"recursion_limit": 8},
            )
            for message in result["messages"]:
                print_text(f"{message.type}: {message.content}")

    asyncio.run(exchange())


if __name__ == "__main__":
    run_cli(main)
