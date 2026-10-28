"""Exercise Streamable HTTP with an ASGI transport and explicit endpoint validation.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/13_mcp/examples/03_http_client.py --offline
Expected: HTTP protocol discovery and call succeed without binding a network port.
Cost: No model calls; real HTTP handlers, no network sockets.
Requires: agents
"""

import asyncio

from common.errors import run_cli
from common.lesson import lesson_settings
from common.mcp import call_inventory, inventory_adapter, validate_endpoint
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    print_text(validate_endpoint("http://127.0.0.1:8765/mcp"))

    async def exchange() -> None:
        # KEY IDEA: ASGI drives the actual HTTP handlers in process; it is not a remote-server test.
        async with inventory_adapter("http") as adapter:
            print_text(str(await call_inventory(adapter, "BW-001")))

    asyncio.run(exchange())


if __name__ == "__main__":
    run_cli(main)
