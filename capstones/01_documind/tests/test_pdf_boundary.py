"""Reject unsafe document shapes and retain the uploaded file's own provenance."""

import io

import pytest

pytest.importorskip("pypdf")
from pypdf import PdfWriter

from common.data import data_path
from common.document_chat import pdf_documents


@pytest.mark.parametrize("pages,encrypted", [(1, True), (51, False), (1, False)])
def test_encrypted_excessive_or_image_only_pdf_is_rejected(pages, encrypted):
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=100, height=100)
    if encrypted:
        writer.encrypt("synthetic-password")
    payload = io.BytesIO()
    writer.write(payload)
    with pytest.raises(ValueError):
        pdf_documents(payload.getvalue(), "upload.pdf")


def test_uploaded_name_is_basename_and_pages_keep_original_numbers():
    payload = data_path("handbook/employee_handbook.pdf").read_bytes()
    documents = pdf_documents(payload, r"C:\private\uploaded-handbook.pdf")
    assert {doc.metadata["source"] for doc in documents} == {"uploaded-handbook.pdf"}
    assert [doc.metadata["page"] for doc in documents] == list(range(1, 11))
    assert len({doc.metadata["pdf_sha256"] for doc in documents}) == 1
