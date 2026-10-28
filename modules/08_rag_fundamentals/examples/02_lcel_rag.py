"""Compose retrieval, evidence formatting and grounded generation using LCEL.

Run: uv run --extra rag python modules/08_rag_fundamentals/examples/02_lcel_rag.py --offline
Expected: A structured answer with validated citation metadata.
Cost: One short hosted generation plus local lexical retrieval; --offline is free.
Requires: rag
"""

from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.rag import answer_question
from common.retrieval import LexicalRetriever


def main() -> None:
    settings = lesson_settings()
    retriever = LexicalRetriever(chunk_documents(policy_documents()))
    # KEY IDEA: keep the original question next to the evidence it retrieved.
    pipeline = RunnablePassthrough.assign(
        documents=lambda row: retriever.search(row["question"])
    ) | RunnableLambda(lambda row: answer_question(row["question"], row["documents"], settings))
    print_text(str(pipeline.invoke({"question": "How many days does the warranty cover?"})))


if __name__ == "__main__":
    run_cli(main)
