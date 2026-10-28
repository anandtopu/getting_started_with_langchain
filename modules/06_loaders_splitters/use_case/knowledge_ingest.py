"""Compare three chunking strategies over policy files and a ten-page handbook.

Run: uv run --extra rag python modules/06_loaders_splitters/use_case/knowledge_ingest.py
--offline
Expected: A JSON summary with chunk counts, sizes and provenance for each strategy.
Cost: No model calls or API fees.
Requires: rag
"""

import json

from common.config import ROOT
from common.errors import run_cli
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    documents = policy_documents()
    report = {}
    for strategy in ("fixed", "recursive", "markdown"):
        chunks = chunk_documents(documents, strategy=strategy, size=450, overlap=80)
        report[strategy] = {
            "documents": len(documents),
            "chunks": len(chunks),
            "max_characters": max(len(d.page_content) for d in chunks),
            "indexed_characters": sum(len(d.page_content) for d in chunks),
            "sample_metadata": chunks[0].metadata,
        }
    output = ROOT / settings.runtime_dir / "ingest_comparison.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    run_cli(main)
