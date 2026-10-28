"""Compose prompt, model and text parser with the LCEL pipe operator.

Run: uv run python modules/04_lcel_runnables/examples/01_sequence.py --offline
Expected: A RunnableSequence and a brief Brightwave reply.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Write one Brightwave greeting."), ("human", "{customer}")]
    )
    # KEY IDEA: each stage's output becomes the next stage's input.
    pipeline = prompt | get_chat_model(settings=settings) | StrOutputParser()
    assert isinstance(pipeline, RunnableSequence)
    print_text(pipeline.invoke({"customer": "Avery Demo"}))


if __name__ == "__main__":
    run_cli(main)
