"""Discover and call inventory tools over a managed child-process pipe.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/13_mcp/examples/02_stdio_client.py --offline
Expected: The official server responds over stdio and exits when the connection closes.
Cost: No model calls; local child process only.
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
        # KEY IDEA: the reviewed executable and arguments are fixed, never model-generated.
        async with inventory_adapter("stdio") as adapter:
            print_text(str(await call_inventory(adapter, "BW-001")))

    asyncio.run(exchange())


if __name__ == "__main__":
    run_cli(main)
