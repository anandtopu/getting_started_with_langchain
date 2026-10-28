"""Current BaseLoader adapters, stable provenance and visible chunking primitives."""

import csv
import hashlib
import json
from collections.abc import Iterator
from html.parser import HTMLParser
from typing import Literal

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from common.data import DATA_DIR, data_path


def identify(document: Document) -> Document:
    """Content and provenance determine identity, not an arbitrary list position."""
    metadata = {key: value for key, value in document.metadata.items() if key != "chunk_id"}
    identity = json.dumps([metadata, document.page_content], sort_keys=True)
    key = hashlib.sha256(identity.encode()).hexdigest()[:24]
    return Document(
        id=key, page_content=document.page_content, metadata={**document.metadata, "chunk_id": key}
    )


class LocalLoader(BaseLoader):
    """Load one allowed local text/Markdown/CSV/JSON/PDF file as Documents lazily.

    JSON expects the course FAQ list. PDF extraction is text-only; scanned pages
    need OCR, which this course loader deliberately does not claim to provide.
    """

    def __init__(self, relative: str) -> None:
        self.path = data_path(relative)
        self.source = self.path.relative_to(DATA_DIR).as_posix()

    def lazy_load(self) -> Iterator[Document]:
        metadata = {"source": self.source}
        if self.path.suffix == ".pdf":
            from pypdf import PdfReader

            with self.path.open("rb") as handle:
                reader = PdfReader(handle)
                for page, item in enumerate(reader.pages, 1):
                    yield identify(
                        Document(
                            page_content=item.extract_text() or "",
                            metadata={**metadata, "page": page},
                        )
                    )
        elif self.path.suffix == ".csv":
            with self.path.open(encoding="utf-8", newline="") as handle:
                for row, item in enumerate(csv.DictReader(handle), 1):
                    yield identify(
                        Document(page_content=json.dumps(item), metadata={**metadata, "row": row})
                    )
        elif self.path.suffix == ".json":
            for row, item in enumerate(json.loads(self.path.read_text(encoding="utf-8")), 1):
                yield identify(
                    Document(page_content=json.dumps(item), metadata={**metadata, "row": row})
                )
        elif self.path.suffix in {".md", ".txt"}:
            yield identify(
                Document(page_content=self.path.read_text(encoding="utf-8"), metadata=metadata)
            )
        else:
            raise ValueError("Supported local formats: Markdown, text, CSV, JSON and PDF.")


class VisibleHTML(HTMLParser):
    """Extract visible text, ignoring comments/scripts/styles; not a full HTML sanitizer."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.hidden = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in {"script", "style"}:
            self.hidden += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"}:
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data: str) -> None:
        if not self.hidden and data.strip():
            self.parts.append(data.strip())


def html_document(html: str, source: str) -> Document:
    parser = VisibleHTML()
    parser.feed(html)
    return identify(Document(page_content="\n".join(parser.parts), metadata={"source": source}))


def policy_documents(*, handbook: bool = True) -> list[Document]:
    """Only the explicit policy corpus; never ingest security fixtures via a broad glob."""
    documents = [
        doc
        for path in sorted((DATA_DIR / "policies").glob("*.md"))
        for doc in LocalLoader(path.relative_to(DATA_DIR).as_posix()).lazy_load()
    ]
    if handbook:
        documents.extend(LocalLoader("handbook/employee_handbook.pdf").lazy_load())
    return documents


def chunk_documents(
    documents: list[Document],
    *,
    size: int = 450,
    overlap: int = 80,
    strategy: Literal["recursive", "fixed", "markdown"] = "recursive",
) -> list[Document]:
    if size < 1 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size.")
    if strategy not in {"recursive", "fixed", "markdown"}:
        raise ValueError("Unknown chunking strategy.")
    prepared = []
    for document in documents:
        parent = document.id or identify(document).id
        pieces = [document]
        if strategy == "markdown" and document.metadata["source"].endswith(".md"):
            pieces = MarkdownHeaderTextSplitter(
                [("#", "heading"), ("##", "section")], strip_headers=False
            ).split_text(document.page_content)
        for piece in pieces:
            prepared.append(
                Document(
                    page_content=piece.page_content,
                    metadata={**document.metadata, **piece.metadata, "parent_id": parent},
                )
            )
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        separators=[""] if strategy == "fixed" else None,
        add_start_index=True,
    )
    # KEY IDEA: split_documents propagates metadata to every child; IDs must be recomputed.
    return [identify(doc) for doc in splitter.split_documents(prepared)]


def corpus_digest(documents: list[Document]) -> str:
    payload = sorted(json.dumps([d.metadata, d.page_content], sort_keys=True) for d in documents)
    return hashlib.sha256(json.dumps(payload).encode()).hexdigest()
