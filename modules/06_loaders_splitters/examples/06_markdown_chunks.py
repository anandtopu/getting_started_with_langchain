"""Preserve Markdown heading and parent metadata while limiting child size.

Run: uv run --extra rag python modules/06_loaders_splitters/examples/06_markdown_chunks.py
--offline
Expected: Chunks with heading, source, parent_id and chunk_id.
Cost: No model calls or API fees.
Requires: rag
"""

from common.errors import run_cli
from common.knowledge import LocalLoader, chunk_documents
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    chunks = chunk_documents(
        LocalLoader("policies/returns.md").load(), strategy="markdown", size=350, overlap=50
    )
    # KEY IDEA: split headings first, then enforce size inside each logical section.
    for chunk in chunks:
        print_text(str(chunk.metadata))


if __name__ == "__main__":
    run_cli(main)
