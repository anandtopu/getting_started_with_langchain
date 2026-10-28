"""Visualize recursive chunk boundaries and overlap on a policy.

Run: uv run --extra rag python modules/06_loaders_splitters/examples/05_recursive_chunks.py
--offline
Expected: Chunk sizes/start offsets and .runtime/chunk_overlap.png.
Cost: No model calls or API fees.
Requires: rag
"""

from common.config import ROOT
from common.errors import run_cli
from common.knowledge import LocalLoader, chunk_documents
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    settings = lesson_settings()
    source = LocalLoader("policies/returns.md").load()
    chunks = chunk_documents(source, size=300, overlap=60)
    figure, axis = plt.subplots(figsize=(9, 4))
    for i, chunk in enumerate(chunks):
        start = chunk.metadata["start_index"]
        axis.barh(i, len(chunk.page_content), left=start, color="#167d8d")
        print_text(f"chunk {i}: start={start}, characters={len(chunk.page_content)}")
    # KEY IDEA: overlap preserves nearby context but duplicates indexed text and tokens.
    axis.set(
        xlabel="Character position in the policy",
        ylabel="Chunk",
        title="Recursive boundaries: target overlap 60 characters",
    )
    output = ROOT / settings.runtime_dir / "chunk_overlap.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(output, dpi=150)
    plt.close(figure)
    print_text(str(output))


if __name__ == "__main__":
    run_cli(main)
