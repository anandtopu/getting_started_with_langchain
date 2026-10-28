"""Answer a policy question with validated file/page citations and explicit abstention.

Run: uv run --extra rag python modules/08_rag_fundamentals/use_case/ask_brightwave.py --offline
Expected: A policy answer and a separate unknown-question abstention.
Cost: Two short hosted generations, usually under $0.01; offline/local no API fee.
Requires: rag
"""

from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.rag import answer_question
from common.retrieval import LexicalRetriever


def main() -> None:
    settings = lesson_settings()
    retriever = LexicalRetriever(chunk_documents(policy_documents()))
    for question in [
        "How many days does the warranty last?",
        "Who won the 2025 Brightwave design award?",
    ]:
        print_text(question)
        print_text(str(answer_question(question, retriever.search(question), settings)))


if __name__ == "__main__":
    run_cli(main)
