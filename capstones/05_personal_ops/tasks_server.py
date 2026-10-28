"""Serve the owned tasks store through the official MCP SDK.

Run: uv run --extra agents python capstones/05_personal_ops/tasks_server.py --offline
Expected: finite empty-list check; --stdio starts the pipe server until the client exits.
Cost: none. Runtime storage is isolated from committed data. Requires: agents
"""

import argparse
import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory

from common.personal_ops import OpsRepository, ops_server
from common.pretty import print_text
from common.testing import offline_environment


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--stdio", action="store_true")
    parser.add_argument("--directory", type=Path)
    parser.add_argument("--owner", default="learner")
    args = parser.parse_args()
    with offline_environment():
        if args.stdio:
            if args.directory is None:
                parser.error("--stdio requires a host-owned --directory")
            # KEY IDEA: stdout is exclusively MCP protocol traffic in server mode.
            asyncio.run(
                ops_server(OpsRepository(args.directory, args.owner), "tasks").run_stdio_async()
            )
        else:
            with TemporaryDirectory() as directory:
                print_text(str(OpsRepository(Path(directory), args.owner).list_items("tasks")))


if __name__ == "__main__":
    main()
