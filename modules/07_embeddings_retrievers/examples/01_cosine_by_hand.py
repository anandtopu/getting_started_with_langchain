"""Calculate cosine similarity and show a labelled two-dimensional projection.

Run: uv run --extra rag python modules/07_embeddings_retrievers/examples/01_cosine_by_hand.py
--offline
Expected: Cosine similarity near 1 for aligned vectors, and an illustrative projection PNG.
Cost: Offline: no API fees. Live embeddings depend on corpus size and the chosen provider.
Requires: rag
"""

import numpy as np

from common.config import ROOT
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        raise ValueError("Cosine is undefined for a zero vector.")
    return float(np.dot(a, b) / denominator)


def main() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    settings = lesson_settings()
    vectors = np.array([[1.0, 0.1, 0.0], [0.9, 0.2, 0.0], [0.0, 0.2, 1.0], [0.1, 0.0, 0.9]])
    print_text(f"Illustrative tent similarity: {cosine(vectors[0], vectors[1]):.3f}")
    centered = vectors - vectors.mean(axis=0)
    _, _, axes = np.linalg.svd(centered, full_matrices=False)
    projected = centered @ axes[:2].T
    # KEY IDEA: these vectors are invented teaching coordinates, not learned embeddings.
    figure, axis = plt.subplots(figsize=(7, 4))
    axis.scatter(projected[:, 0], projected[:, 1])
    axis.margins(0.2)
    for label, point in zip(["tent A", "tent B", "boot A", "boot B"], projected, strict=True):
        axis.annotate(label, point, xytext=(5, 5), textcoords="offset points")
    axis.set_title("Illustrative coordinates projected to 2D; distances can distort")
    output = ROOT / settings.runtime_dir / "embedding_projection.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(output, dpi=150)
    plt.close(figure)
    print_text(str(output))


if __name__ == "__main__":
    run_cli(main)
