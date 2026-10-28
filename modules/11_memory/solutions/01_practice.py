"""Customer thread scope.

Task: Return a config whose thread_id combines nonempty alphanumeric customer and conversation
IDs.

Run: uv run --extra agents python modules/11_memory/solutions/01_practice.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def config(customer: str, conversation: str) -> dict:
    # KEY IDEA: Customer thread scope.
    if not customer.isalnum() or not conversation.isalnum():
        raise ValueError("Use alphanumeric identifiers.")
    return {"configurable": {"thread_id": customer + ":" + conversation}}


def main() -> None:
    lesson_settings()
    print_text(str(config("C001", "morning")))


if __name__ == "__main__":
    run_cli(main)
