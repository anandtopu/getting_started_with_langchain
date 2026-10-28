"""Keep text and source provenance together in a Document.

Run: uv run --extra rag python modules/06_loaders_splitters/examples/01_documents.py --offline
Expected: Return-policy text, a stable ID, and a relative source path.
Cost: No model calls or API fees.
Requires: rag
"""

from common.errors import run_cli
from common.knowledge import LocalLoader
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    doc = LocalLoader("policies/returns.md").load()[0]
    # KEY IDEA: page_content is evidence; metadata tells us where it came from.
    print_text(doc.page_content[:180])
    print_text(str({"id": doc.id, **doc.metadata}))


if __name__ == "__main__":
    run_cli(main)
