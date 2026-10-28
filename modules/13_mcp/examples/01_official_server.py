"""Discover a real official-SDK inventory server over an in-process protocol connection.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/13_mcp/examples/01_official_server.py --offline
Expected: One reviewed inventory_stock tool and the BW-001 record.
Cost: No model calls; local protocol only.
Requires: agents
"""

import asyncio

from common.errors import run_cli
from common.lesson import lesson_settings
from common.mcp import call_inventory, inventory_adapter
from common.pretty import print_text


def main() -> None:
    lesson_settings()

    async def exchange() -> None:
        # KEY IDEA: this is an actual MCP handshake and call, with no external socket.
        async with inventory_adapter("memory") as adapter:
            print_text(str([t.name for t in await adapter.list_tools()]))
            print_text(str(await call_inventory(adapter, "BW-001")))

    asyncio.run(exchange())


if __name__ == "__main__":
    run_cli(main)
