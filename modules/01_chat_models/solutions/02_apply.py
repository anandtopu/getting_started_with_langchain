"""Read usage without inventing zero.

Task: Return None for absent usage, otherwise (input, output, total). Do not add reasoning
tokens a second time.
Run: uv run python modules/01_chat_models/solutions/02_apply.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def token_counts(usage: dict | None) -> tuple | None:
    if not usage or "input_tokens" not in usage or "output_tokens" not in usage:
        return None
    return (
        usage["input_tokens"],
        usage["output_tokens"],
        usage["input_tokens"] + usage["output_tokens"],
    )


def main() -> None:
    lesson_settings()
    print_text(str(token_counts(None)))


if __name__ == "__main__":
    run_cli(main)
