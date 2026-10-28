"""Implement a JSON loader. Task: Create FAQDocuments(BaseLoader) with lazy_load yielding one
Document per supplied record and row/source metadata.

Run: uv run --extra rag python modules/06_loaders_splitters/solutions/03_stretch.py --offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

import json
from collections.abc import Iterator

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

from common.errors import run_cli
from common.knowledge import identify
from common.lesson import lesson_settings
from common.pretty import print_text


class FAQDocuments(BaseLoader):
    def __init__(self, records: list[dict]) -> None:
        self.records = records

    def lazy_load(self) -> Iterator[Document]:
        for index, record in enumerate(self.records, 1):
            yield identify(
                Document(
                    page_content=json.dumps(record), metadata={"source": "faq.json", "row": index}
                )
            )


def main() -> None:
    lesson_settings()
    print_text(str(FAQDocuments([{"question": "Returns?", "answer": "30 days"}]).load()))


if __name__ == "__main__":
    run_cli(main)
