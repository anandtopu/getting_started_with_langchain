"""Safe review command: Accept exactly approve or reject, then construct Command(resume=...).

Run: uv run --extra agents python modules/14_langgraph/solutions/03_stretch.py --offline
Expected: Runnable reference result.
Cost: No model calls. Requires: agents
"""

from langgraph.types import Command

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def resume(decision: str) -> Command:
    if decision not in ("approve", "reject"):
        raise ValueError("Invalid decision")
    return Command(resume=decision)


def main() -> None:
    lesson_settings()
    print_text(str(resume("reject")))


if __name__ == "__main__":
    run_cli(main)
