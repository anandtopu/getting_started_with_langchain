"""Extract PDF pages lazily through a current core BaseLoader adapter.

Run: uv run --extra rag python modules/06_loaders_splitters/examples/02_pdf_lazy.py --offline
Expected: Ten pages with one-based page citations and handbook source.
Cost: No model calls or API fees.
Requires: rag
"""

from common.errors import run_cli
from common.knowledge import LocalLoader
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    loader = LocalLoader("handbook/employee_handbook.pdf")
    # KEY IDEA: lazy_load yields documents; page numbers are normalized once at ingestion.
    for doc in loader.lazy_load():
        print_text(
            f"{doc.metadata['source']} page {doc.metadata['page']}: "
            f"{len(doc.page_content)} characters"
        )


if __name__ == "__main__":
    run_cli(main)
