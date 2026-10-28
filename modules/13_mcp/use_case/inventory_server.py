"""Official SDK server; --stdio serves until its client closes the pipe.

Run: uv run --extra agents python modules/13_mcp/use_case/inventory_server.py
Expected: the finite default prints a checked inventory record; --stdio serves MCP.
Cost: no model calls; synthetic read-only inventory only.
Requires: agents
"""

import argparse
import asyncio

from common.mcp import inventory, inventory_server
from common.pretty import print_text
from common.testing import offline_environment


async def serve_stdio() -> None:
    # KEY IDEA: stdout belongs to the protocol; never print diagnostic prose to it.
    await inventory_server().run_stdio_async()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--stdio", action="store_true")
    args = parser.parse_args()
    with offline_environment():
        if args.stdio:
            asyncio.run(serve_stdio())
        else:
            print_text(str(inventory("BW-001")))


if __name__ == "__main__":
    main()
