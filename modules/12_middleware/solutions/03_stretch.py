"""Narrow retry policy.

Task: Retry timeouts only; never retry permission or validation failures automatically.

Run: uv run --extra agents python modules/12_middleware/solutions/03_stretch.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def retryable(error: Exception) -> bool:
    # KEY IDEA: Narrow retry policy.
    return isinstance(error, TimeoutError)


def main() -> None:
    lesson_settings()
    print_text(str(retryable(PermissionError("not allowed"))))


if __name__ == "__main__":
    run_cli(main)
