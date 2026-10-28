"""Review decision schema.

Task: Allow only approve or reject; never accept an agent-supplied edit or respond decision.

Run: uv run --extra agents python modules/12_middleware/solutions/02_apply.py --offline
Expected: a runnable baseline; target tests check the required behavior.
Cost: no model calls or API fees.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def review_decision(value: str) -> dict:
    # KEY IDEA: Review decision schema.
    if value not in {"approve", "reject"}:
        raise ValueError("Choose approve or reject.")
    return {"decisions": [{"type": value}]}


def main() -> None:
    lesson_settings()
    print_text(str(review_decision("reject")))


if __name__ == "__main__":
    run_cli(main)
