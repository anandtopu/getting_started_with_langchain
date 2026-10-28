"""Chat with a PDF using hybrid retrieval and checked page/quote citations.

Run: uv run --extra apps python capstones/01_documind/solution.py --offline
Expected: a grounded return-window answer with page 2 of the synthetic handbook.
Cost: one embedding batch, query embedding and one model call live; zero offline. Requires: apps
"""

import argparse
from pathlib import Path

from common.config import get_settings
from common.data import data_path
from common.document_chat import DocumentChat, pdf_documents
from common.errors import run_cli
from common.pretty import print_text


def run_case(case: dict, settings, directory: Path) -> dict:
    chat = DocumentChat(
        pdf_documents(data_path("handbook/employee_handbook.pdf").read_bytes(), "handbook.pdf"),
        settings,
    )
    result = chat.ask(case["question"])
    correct = all(word.lower() in result["answer"].lower() for word in case["must_contain"])
    pages = {citation["page"] for citation in result["citations"]}
    passed = (
        correct
        and result["abstained"] == case["abstained"]
        and (case["page"] in pages if case["page"] else not pages)
    )
    return {"id": case["id"], "passed": passed, "answer": result}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--pdf", type=Path)
    parser.add_argument(
        "--question",
        default="Unused gear may be returned within how many calendar days after delivery?",
    )
    args = parser.parse_args()
    settings = get_settings()
    if args.offline:
        settings = settings.model_copy(update={"course_offline": True})
    path = args.pdf or data_path("handbook/employee_handbook.pdf")
    if path.stat().st_size > 5_000_000:
        raise ValueError("PDF exceeds 5 MB.")
    # KEY IDEA: page provenance is established before chunking and retained in citations.
    chat = DocumentChat(pdf_documents(path.read_bytes(), path.name), settings)
    print_text(str(chat.ask(args.question)))


if __name__ == "__main__":
    run_cli(main)
