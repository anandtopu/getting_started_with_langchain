"""Bounded PDF ingestion, session-local hybrid retrieval and validated page citations."""

import hashlib
import io
import re

from langchain_core.documents import Document
from langsmith import tracing_context

from common.config import Settings
from common.knowledge import chunk_documents, identify
from common.rag import answer_question
from common.retrieval import LexicalRetriever, fuse, memory_index


def pdf_documents(payload: bytes, name: str) -> list[Document]:
    from pypdf import PdfReader

    if not payload.startswith(b"%PDF-") or len(payload) > 5_000_000:
        raise ValueError("Choose a PDF no larger than 5 MB.")
    filename = re.split(r"[/\\]", name)[-1][:100]
    if not filename or not filename.lower().endswith(".pdf"):
        raise ValueError("Use a PDF filename.")
    try:
        reader = PdfReader(io.BytesIO(payload))
        if reader.is_encrypted or not 1 <= len(reader.pages) <= 50:
            raise ValueError("Use an unencrypted PDF containing 1 through 50 pages.")
        documents, total = [], 0
        digest = hashlib.sha256(payload).hexdigest()
        for number, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            total += len(text)
            if total > 200_000:
                raise ValueError("Extracted text exceeds the 200,000-character limit.")
            if text.strip():
                documents.append(
                    identify(
                        Document(
                            page_content=text,
                            metadata={
                                "source": filename,
                                "page": number,
                                "pdf_sha256": digest,
                            },
                        )
                    )
                )
    except ValueError:
        raise
    except Exception:
        raise ValueError("PDF could not be read; use an unencrypted text PDF.") from None
    if not documents:
        raise ValueError("No extractable text; scanned PDFs need a separate OCR step.")
    return documents


class DocumentChat:
    """A fresh instance per uploaded corpus; never share private indexes in a global cache."""

    def __init__(self, documents: list[Document], settings: Settings) -> None:
        if not documents or len(documents) > 50:
            raise ValueError("Choose one nonempty PDF of at most 50 text pages.")
        self.settings = settings
        self.chunks = chunk_documents(documents, size=650, overlap=100)
        self.lexical = LexicalRetriever(self.chunks)
        with tracing_context(enabled=False):
            self.vector = memory_index(self.chunks, settings)

    def ask(self, question: str) -> dict:
        if not question.strip() or len(question) > 2000:
            raise ValueError("Use 1 through 2,000 question characters.")
        with tracing_context(enabled=False):
            lexical = self.lexical.search(question, k=4)
            vector = self.vector.similarity_search(question, k=4)
            # Fakes test both retrieval interfaces; they are not semantic ranking evidence.
            found = fuse([lexical, vector], k=4) if lexical else []
            answer = answer_question(question, found, self.settings)
        return {
            **answer,
            "retrieved": [d.metadata for d in found],
            "retrieval_mode": "hybrid-with-fake-vectors"
            if self.settings.course_offline
            else "hybrid",
            "lexical_overlap_required": True,
        }


def render_document_chat() -> None:
    import streamlit as st

    from common.config import get_settings
    from common.data import data_path

    st.title("DocuMind")
    st.caption("Ask about one PDF. Citations identify its page and exact supporting quote.")
    offline = st.checkbox("Use free scripted mode", value=True)
    if not offline:
        st.warning("Live mode sends document text to the configured embedding/model providers.")
    consent = offline or st.checkbox("I approve sending this document to my configured providers")
    uploaded = st.file_uploader(
        "Choose a text PDF (maximum 5 MB, 50 pages)", type=["pdf"], max_upload_size=5
    )
    sample = st.checkbox("Use the synthetic Brightwave handbook", value=uploaded is None)
    payload = (
        data_path("handbook/employee_handbook.pdf").read_bytes()
        if sample
        else (uploaded.getvalue() if uploaded is not None else None)
    )
    name = "employee_handbook.pdf" if sample else uploaded.name if uploaded is not None else ""
    if payload is None or not consent:
        st.info("Select a PDF and an approved execution mode.")
        return
    settings = get_settings().model_copy(update={"course_offline": offline})
    identity = (hashlib.sha256(payload).hexdigest(), name, offline)
    try:
        if st.session_state.get("document_identity") != identity:
            st.session_state.document_chat = DocumentChat(pdf_documents(payload, name), settings)
            st.session_state.document_identity = identity
            st.session_state.document_history = []
        if st.button("Clear chat"):
            st.session_state.document_history = []
        for role, text in st.session_state.document_history:
            with st.chat_message(role):
                st.write(text)
        if question := st.chat_input("Ask a self-contained question about this PDF"):
            answer = st.session_state.document_chat.ask(question)
            rendered = (
                answer["answer"]
                + "\n\n"
                + "\n".join(
                    f"{c['source']}, page {c['page']}: {c['quote']}" for c in answer["citations"]
                )
            )
            with st.chat_message("user"):
                st.write(question)
            with st.chat_message("assistant"):
                st.write(rendered)
            st.session_state.document_history.extend([("user", question), ("assistant", rendered)])
            st.session_state.document_history = st.session_state.document_history[-20:]
    except ValueError as error:
        st.error(str(error))
    except Exception:
        st.error("Request failed. Check the selected provider with scripts/check_env.py.")
