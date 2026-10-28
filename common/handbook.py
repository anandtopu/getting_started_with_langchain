"""Handbook-only retrieval with page citations and a bounded retrieved context."""

from common.config import Settings
from common.knowledge import LocalLoader, chunk_documents
from common.rag import answer_question
from common.retrieval import LexicalRetriever


def answer_handbook(question: str, settings: Settings) -> dict:
    if not question.strip() or len(question) > 2000:
        raise ValueError("Supply a nonempty question of at most 2000 characters.")
    pages = LocalLoader("handbook/employee_handbook.pdf").load()
    chunks = chunk_documents(pages, size=550, overlap=80)
    evidence = LexicalRetriever(chunks).search(question, k=3)
    result = answer_question(question, evidence, settings)
    return {**result, "retrieved_pages": sorted({d.metadata["page"] for d in evidence})}
