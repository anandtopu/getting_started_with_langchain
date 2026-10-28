"""Execute the actual PDF UI and ensure session histories never share indexes."""

import pytest

pytest.importorskip("streamlit")
pytest.importorskip("pypdf")
pytest.importorskip("rank_bm25")
from streamlit.testing.v1 import AppTest

from common.config import ROOT
from common.document_chat import pdf_documents


def test_pdf_validation():
    with pytest.raises(ValueError):
        pdf_documents(b"not a pdf", "test.pdf")
    with pytest.raises(ValueError):
        pdf_documents(b"%PDF-" + b"x" * 5_000_000, "test.pdf")


def test_actual_chat_ui_and_session_isolation():
    app = AppTest.from_file(ROOT / "capstones/01_documind/app.py", default_timeout=15)
    AppTest.run(app)
    assert not app.exception
    app.chat_input[0].set_value(
        "Unused gear may be returned within how many calendar days after delivery?"
    )
    AppTest.run(app)
    assert "30" in app.session_state["document_history"][-1][1]
    assert "page 2" in app.session_state["document_history"][-1][1]
    other = AppTest.from_file(ROOT / "capstones/01_documind/app.py", default_timeout=15)
    AppTest.run(other)
    assert other.session_state["document_history"] == []
    assert other.session_state["document_chat"] is not app.session_state["document_chat"]
    next(button for button in app.button if button.label == "Clear chat").click()
    AppTest.run(app)
    assert app.session_state["document_history"] == []
