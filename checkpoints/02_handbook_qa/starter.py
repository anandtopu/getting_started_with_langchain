"""Runnable handbook baseline: safely abstain until retrieval and citations are added.

Run: uv run --extra rag python checkpoints/02_handbook_qa/starter.py --offline
Expected: a conservative no-evidence response; target tests guide the implementation.
Cost: no model calls in this baseline.
"""

from common.config import Settings
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def answer_handbook(question: str, settings: Settings) -> dict:
    # YOUR CODE HERE: load PDF pages, retrieve bounded evidence and validate every citation.
    return {
        "answer": "I do not know from the supplied evidence.",
        "abstained": True,
        "citations": [],
        "retrieved_pages": [],
        "mode": "extractive-fixture" if settings.course_offline else "live",
    }


def main() -> None:
    settings = lesson_settings()
    print_text(str(answer_handbook("What refund amount requires approval?", settings)))


if __name__ == "__main__":
    run_cli(main)
