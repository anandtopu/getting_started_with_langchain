"""Compute cosine by hand. Task: Compute normalized cosine similarity; reject a zero vector.

Run: uv run --extra rag python modules/07_embeddings_retrievers/exercises/01_practice.py
--offline
Expected: A runnable demonstration; learner tests check the requested improvements.
Cost: No model calls or API fees.
Requires: rag
"""

import numpy as np

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


# YOUR CODE HERE: improve the runnable baseline above to meet the target checks.


def main() -> None:
    lesson_settings()
    print_text(str(cosine(np.array([2.0, 0.0]), np.array([3.0, 0.0]))))


if __name__ == "__main__":
    run_cli(main)
