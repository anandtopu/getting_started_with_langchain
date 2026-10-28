"""Connect reviewed discovered MCP tools to create_agent inside a managed session.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/13_mcp/examples/04_agent_connection.py --offline
Expected: The agent calls inventory_stock and receives validated inventory data.
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
        async with inventory_adapter("memory") as adapter:
            checked_tools(await adapter.list_tools())

            @tool
            async def inventory_stock(sku: str) -> dict:
                """Read public inventory through the reviewed MCP server and validate the result."""
                return await call_inventory(adapter, sku)

            # KEY IDEA: a small wrapper validates untrusted server results before agent consumption.
            agent = create_agent(
                get_chat_model(
                    settings=settings,
                    responses=[
                        tool_request("inventory_stock", {"sku": "BW-001"}),
                        "Stock checked; no reservation created.",
                    ],
                ),
                [inventory_stock],
            )
            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": "Check BW-001 stock."}]},
                {"recursion_limit": 8},
            )
            print_text(str([(m.type, m.content) for m in result["messages"]]))

    asyncio.run(exchange())


if __name__ == "__main__":
    run_cli(main)
