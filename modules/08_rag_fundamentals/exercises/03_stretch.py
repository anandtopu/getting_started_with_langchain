"""Wire retrieval to generation. Task: Call a supplied retriever, pass only returned documents to
answer_question, and return a validated result.

Run: uv run --extra rag python modules/08_rag_fundamentals/exercises/03_stretch.py --offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: Offline: no API fees. Live model calls apply only when this exercise uses generation.
Requires: rag
"""

from common.config import Settings
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.retrieval import LexicalRetriever


def respond(question: str, retriever: LexicalRetriever, settings: Settings) -> dict:
    return {"answer": "I do not know", "abstained": True, "citations": []}


# YOUR CODE HERE: improve the runnable baseline above to meet the target checks.


def main() -> None:
    settings = lesson_settings()
    from common.knowledge import LocalLoader

    print_text(
        str(
            respond(
                "What is the return window?",
                LexicalRetriever(LocalLoader("policies/returns.md").load()),
                settings,
            )
        )
    )


if __name__ == "__main__":
    run_cli(main)
