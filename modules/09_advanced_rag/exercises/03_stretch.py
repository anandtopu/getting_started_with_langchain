"""Use the correct evaluation denominator. Task: Compute retrieval hit rate excluding unanswerable
None entries; return None when no answerable cases exist.

Run: uv run --extra rag python modules/09_advanced_rag/exercises/03_stretch.py --offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def hit_rate(hits: list[bool | None]) -> float | None:
    return sum(bool(hit) for hit in hits) / len(hits) if hits else None


# YOUR CODE HERE: improve the runnable baseline above to meet the target checks.


def main() -> None:
    lesson_settings()
    print_text(str(hit_rate([True, False, None])))


if __name__ == "__main__":
    run_cli(main)
