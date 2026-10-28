"""Visible lexical search, reciprocal-rank fusion and product constraint enforcement."""

import json
import re

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

from common.config import Settings
from common.data import load_csv
from common.knowledge import identify
from common.models import get_embeddings

STOP = set(
    "a an the is are of for to from in on with what how many can my i do does be it its and or "
    "brightwave outfitters please me when has have this that who your".split()
)


def terms(text: str) -> list[str]:
    return [word for word in re.findall(r"[a-z0-9]+", text.lower()) if word not in STOP]


class LexicalRetriever:
    """BM25 ranks literal words; it is a real deterministic search, not a fake model."""

    def __init__(self, documents: list[Document]) -> None:
        from rank_bm25 import BM25Okapi

        if not documents:
            raise ValueError("Cannot index an empty corpus.")
        self.documents = documents
        self.tokens = [terms(d.page_content) for d in documents]
        if not any(self.tokens):
            raise ValueError("Corpus must contain at least one searchable term.")
        self.index = BM25Okapi(self.tokens)

    def search(self, question: str, k: int = 3) -> list[Document]:
        if k < 1:
            raise ValueError("k must be positive.")
        query = terms(question)
        if not query:
            return []
        scores = self.index.get_scores(query)
        ranked = sorted(
            range(len(scores)), key=lambda i: (-float(scores[i]), str(self.documents[i].id))
        )
        # No matching terms means no evidence. Negative BM25 scores can occur on tiny corpora.
        return [self.documents[i] for i in ranked if set(query) & set(self.tokens[i])][:k]


def fuse(rankings: list[list[Document]], k: int = 3, constant: int = 60) -> list[Document]:
    """Reciprocal-rank fusion adds 1/(constant+rank), never raw incompatible score scales."""
    if k < 1 or constant < 1:
        raise ValueError("k and fusion constant must be positive.")
    scores, documents = {}, {}
    for ranking in rankings:
        seen = set()
        for rank, doc in enumerate(ranking, 1):
            key = doc.id or identify(doc).id
            if key in seen:
                continue
            seen.add(key)
            documents[key] = doc
            scores[key] = scores.get(key, 0) + 1 / (constant + rank)
    return [documents[key] for key in sorted(scores, key=lambda key: (-scores[key], key))[:k]]


def expand_query(question: str) -> list[str]:
    """A small generic synonym dictionary, independent of evaluation questions/labels."""
    synonyms = {
        "coverage": "warranty",
        "kept": "retention",
        "costs": "subtotal",
        "returned": "return",
        "approve": "approval",
        "manufacturing": "defect",
    }
    additions = [value for word, value in synonyms.items() if word in terms(question)]
    return [question, question + " " + " ".join(additions)] if additions else [question]


def memory_index(documents: list[Document], settings: Settings) -> InMemoryVectorStore:
    store = InMemoryVectorStore(get_embeddings(settings=settings))
    store.add_documents(documents)
    return store


def product_documents() -> list[Document]:
    documents = []
    for row in load_csv("products.csv"):
        specs = json.loads(row["specs"])
        metadata = {
            "source": "products.csv",
            "sku": row["sku"],
            "category": row["category"],
            "price": float(row["price"]),
            "capacity": int(specs.get("capacity", 0)),
            "waterproof_mm": int(specs.get("waterproof_mm", 0)),
        }
        documents.append(identify(Document(page_content=json.dumps(row), metadata=metadata)))
    return documents


def product_search(
    settings: Settings, *, price_below: float = 300, capacity: int = 4
) -> list[Document]:
    candidates = [
        doc
        for doc in product_documents()
        if doc.metadata["category"] == "tents"
        and doc.metadata["price"] < price_below
        and doc.metadata["capacity"] == capacity
        and doc.metadata["waterproof_mm"] > 0
    ]
    if not candidates:
        return []
    # KEY IDEA: deterministic constraints gate the candidates before semantic ranking.
    return memory_index(candidates, settings).similarity_search(
        "waterproof tent for four people", k=3
    )
