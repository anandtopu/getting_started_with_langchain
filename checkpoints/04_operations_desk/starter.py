"""Runnable conservative baseline: ask for clarification without contacting specialists.

Run: uv run --extra agents python checkpoints/04_operations_desk/starter.py --offline
Expected: A clarification response. Complete the graph to satisfy checkpoint cases.
Cost: No model calls. Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def operations(question: str, customer: str) -> dict:
    # YOUR CODE HERE: validate routing, restrict each tool set, project context, then synthesize.
    return {"answer": "Please clarify the support request.", "reports": []}


def main() -> None:
    lesson_settings()
    print_text(str(operations("Check billing and shipping for BW1001", "C001")))


if __name__ == "__main__":
    run_cli(main)
