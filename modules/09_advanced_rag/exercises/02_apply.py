"""Expand children to parents. Task: Return unique original parent Documents in first-hit order;
reject a missing parent.

Run: uv run --extra rag python modules/09_advanced_rag/exercises/02_apply.py --offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

from langchain_core.documents import Document

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def expand(children: list[Document], parents: list[Document]) -> list[Document]:
    return children


# YOUR CODE HERE: improve the runnable baseline above to meet the target checks.


def main() -> None:
    lesson_settings()
    parent = Document(id="p", page_content="Full policy", metadata={"source": "policy.md"})
    child = Document(id="c", page_content="policy", metadata={"parent_id": "p"})
    print_text(str(expand([child], [parent])))


if __name__ == "__main__":
    run_cli(main)
