"""Reserve output tokens.

Task: Implement fits(input_tokens, reserve, window). Include the output reserve; reject
negative counts.
Run: uv run python modules/00_setup/solutions/01_practice.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def fits(input_tokens: int, reserve: int, window: int) -> bool:
    if min(input_tokens, reserve, window) < 0:
        raise ValueError("Token counts must be nonnegative.")
    return input_tokens + reserve <= window


def main() -> None:
    lesson_settings()
    print_text(str(fits(90, 20, 100)))


if __name__ == "__main__":
    run_cli(main)
