"""Use the correct evaluation denominator. Task: Compute retrieval hit rate excluding unanswerable
None entries; return None when no answerable cases exist.

Run: uv run --extra rag python modules/09_advanced_rag/solutions/03_stretch.py --offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def hit_rate(hits: list[bool | None]) -> float | None:
    answerable = [hit for hit in hits if hit is not None]
    return sum(answerable) / len(answerable) if answerable else None


def main() -> None:
    lesson_settings()
    print_text(str(hit_rate([True, False, None])))


if __name__ == "__main__":
    run_cli(main)
