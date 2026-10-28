"""Resolve a follow-up question from explicitly supplied conversation history.

Run: uv run --extra rag python modules/09_advanced_rag/examples/06_conversation.py --offline
Expected: Standalone warranty queries and a cited answer; no memory is stored automatically.
Cost: One rewrite and one answer call; offline fixtures have no API fee.
Requires: rag
"""

from common.advanced_rag import rewrite
from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.rag import answer_question
from common.retrieval import LexicalRetriever, fuse


def main() -> None:
    # KEY IDEA: Explicit history resolves references; retrieved evidence supplies the facts.
    settings = lesson_settings()
    history = [
        {"role": "user", "content": "I have a warranty question."},
        {
            "role": "assistant",
            "content": "What would you like to know about manufacturing defects?",
        },
    ]
    question = "How long does it last?"
    queries = rewrite(question, settings, history)
    print_text(str(queries))
    retriever = LexicalRetriever(chunk_documents(policy_documents()))
    evidence = fuse([retriever.search(query) for query in queries])
    # The standalone query supplies the subject that the latest question leaves implicit.
    print_text(str(answer_question(queries[-1], evidence, settings)))


if __name__ == "__main__":
    run_cli(main)
