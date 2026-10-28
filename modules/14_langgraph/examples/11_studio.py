"""Draw an account-free diagram and print the optional local-server command.

Run: uv run --extra agents python modules/14_langgraph/examples/11_studio.py --offline
Expected: Mermaid graph text; the example does not start a persistent service.
Cost: No model calls. Offline fixtures incur no API fee.
Requires: agents
"""

from common.errors import run_cli
from common.graphs import studio_graph
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    # KEY IDEA: draw_mermaid produces text locally; no rendering service is needed.
    print_text(studio_graph.get_graph().draw_mermaid())
    print_text(
        "Optional: uv run --extra deployment langgraph dev --config "
        "langgraph.json --no-browser --host 127.0.0.1"
    )


if __name__ == "__main__":
    run_cli(main)
