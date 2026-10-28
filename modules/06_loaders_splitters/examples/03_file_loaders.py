"""Load Markdown, CSV, JSON and an explicit policy directory.

Run: uv run --extra rag python modules/06_loaders_splitters/examples/03_file_loaders.py
--offline
Expected: Four policy files, 60 product rows, and 40 FAQ records.
Cost: No model calls or API fees.
Requires: rag
"""

from common.errors import run_cli
from common.knowledge import LocalLoader, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    for filename in ("policies/returns.md", "products.csv", "faq.json"):
        docs = LocalLoader(filename).load()
        print_text(f"{filename}: {len(docs)} Documents; first metadata={docs[0].metadata}")
    # KEY IDEA: whitelist the policies directory; security fixtures are not ordinary evidence.
    print_text(f"Policy directory: {len(policy_documents(handbook=False))} Documents")


if __name__ == "__main__":
    run_cli(main)
