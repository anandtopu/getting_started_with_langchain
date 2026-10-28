"""Enforce product constraints. Task: Accept only waterproof four-person tents with price strictly
below 300.

Run: uv run --extra rag python modules/07_embeddings_retrievers/solutions/02_apply.py --offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def eligible(metadata: dict) -> bool:
    return (
        metadata["category"] == "tents"
        and metadata["capacity"] == 4
        and metadata["waterproof_mm"] > 0
        and metadata["price"] < 300
    )


def main() -> None:
    lesson_settings()
    print_text(
        str(eligible({"category": "tents", "capacity": 4, "waterproof_mm": 3000, "price": 299.99}))
    )


if __name__ == "__main__":
    run_cli(main)
