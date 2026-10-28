"""Reject invented citations and demonstrate an explicit no-evidence abstention.

Run: uv run --extra rag python modules/08_rag_fundamentals/examples/03_grounding_citations.py
--offline
Expected: A rejected citation and an answer that says it does not know.
Cost: One generation for the no-evidence demonstration; offline/local no API fee.
Requires: rag
"""

from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.rag import Citation, GroundedAnswer, answer_question, validate_citations


def main() -> None:
    settings = lesson_settings()
    docs = chunk_documents(policy_documents())
    invented = GroundedAnswer(
        answer="Invented policy",
        abstained=False,
        citations=[Citation(chunk_id="not-retrieved", quote="Invented")],
    )
    try:
        validate_citations(invented, docs)
    except ValueError as error:
        print_text(str(error))
    # KEY IDEA: no source/page may be invented by the model; application code resolves them.
    print_text(str(answer_question("Who won the Brightwave design award?", [], settings)))


if __name__ == "__main__":
    run_cli(main)
