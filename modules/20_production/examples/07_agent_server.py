"""Read the server configuration and invoke its registered read-only graph locally.

Run: uv run --extra apps python modules/20_production/examples/07_agent_server.py --offline
Expected: Registered graph path and a read-only review result; no server starts.
Cost: No API calls; deterministic local checks. Requires: apps
"""

import json

from common.config import ROOT
from common.errors import run_cli
from common.graphs import studio_graph
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    config = json.loads((ROOT / "langgraph.json").read_text(encoding="utf-8"))
    print_text(str(config["graphs"]))
    # KEY IDEA: Agent Server is the serving API; LangSmith Deployment is a hosting option.
    print_text(str(studio_graph.invoke({"request": "refund"})))
    print_text("Optional: uv run --extra deployment langgraph dev --no-browser --host 127.0.0.1")


if __name__ == "__main__":
    run_cli(main)
