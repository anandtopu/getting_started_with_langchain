"""Compare a model tokenizer with an explicit offline token fixture and code-aware splitting.

Run: uv run --extra rag python modules/06_loaders_splitters/examples/07_token_code_chunks.py
--offline
Expected: Bounded token chunks and two small Python code sections.
Cost: No API fee; live tokenizer may download vocabulary once. Offline uses an explicit byte
fixture.
Requires: rag
"""

from langchain_text_splitters import Language, RecursiveCharacterTextSplitter, TokenTextSplitter
from langchain_text_splitters.base import Tokenizer, split_text_on_tokens

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    # KEY IDEA: Token limits depend on the tokenizer; a byte fixture is not provider accounting.
    settings = lesson_settings()
    text = "Brightwave returns need proof of purchase. Refunds over $100 need approval."
    if settings.course_offline:
        # ASCII byte IDs make an inspectable test tokenizer, NOT a provider token count.
        fixture = Tokenizer(
            chunk_overlap=4,
            tokens_per_chunk=24,
            encode=lambda value: list(value.encode("ascii")),
            decode=lambda ids: bytes(ids).decode("ascii"),
        )
        chunks = split_text_on_tokens(text=text, tokenizer=fixture)
        print_text("OFFLINE byte-token fixture; not model token accounting.")
    else:
        # First use may download tiktoken's vocabulary; subsequent runs use its local cache.
        chunks = TokenTextSplitter(
            encoding_name="cl100k_base", chunk_size=24, chunk_overlap=4
        ).split_text(text)
    print_text(str(chunks))
    code = (
        "def eligible(days):\n    return days <= 30\n\n"
        "def approval(amount):\n    return amount > 100\n"
    )
    splitter = RecursiveCharacterTextSplitter.from_language(
        Language.PYTHON, chunk_size=60, chunk_overlap=0
    )
    print_text(str(splitter.split_text(code)))


if __name__ == "__main__":
    run_cli(main)
